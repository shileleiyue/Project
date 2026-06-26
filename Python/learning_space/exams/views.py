"""exams 视图 —— 题库管理、试卷、考试、自动评分、错题推荐"""
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import json

from .models import Question, Exam, ExamQuestion, ExamRecord, ExamAnswer
from .serializers import (
    QuestionSerializer, ExamSerializer, ExamCreateSerializer,
    ExamRecordSerializer, ExamRecordDetailSerializer,
    ExamAnswerSubmitSerializer, ExamQuestionSerializer,
)
from accounts.permissions import IsTeacherOrAdmin, IsStudent


# ──────────────────────────────────────────────────────────────────────────────
# 自动评分核心函数
# ──────────────────────────────────────────────────────────────────────────────
def _answer_equal(qtype, correct, student):
    """判定答案是否正确"""
    if qtype == Question.Type.SINGLE:
        return str(correct).upper() == str(student).upper()
    if qtype == Question.Type.JUDGE:
        # correct 可能是 true/false 或 "正确"/"错误"
        def _to_bool(v):
            if isinstance(v, bool):
                return v
            s = str(v).strip().lower()
            return s in ('true', '1', 'yes', '正确', '对', 't')
        return _to_bool(correct) == _to_bool(student)
    if qtype == Question.Type.MULTI:
        # 多选：集合比较（排序后 list）
        if not isinstance(correct, list):
            correct = [correct]
        if not isinstance(student, list):
            student = [student]
        return sorted([str(x).upper() for x in correct]) == sorted([str(x).upper() for x in student])
    return False


# ──────────────────────────────────────────────────────────────────────────────
# 题库（教师/管理员可增改，学生只读）
# ──────────────────────────────────────────────────────────────────────────────
class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filterset_fields = ('course', 'kp', 'question_type', 'difficulty')
    search_fields = ('title',)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsTeacherOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


# ──────────────────────────────────────────────────────────────────────────────
# 试卷
# ──────────────────────────────────────────────────────────────────────────────
class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    filterset_fields = ('course', 'status', 'creator')
    search_fields = ('title',)

    def get_permissions(self):
        public_read = ('list', 'retrieve')
        teacher_actions = ('create', 'update', 'partial_update', 'destroy', 'publish')
        student_actions = ('start', 'submit')
        if self.action in public_read:
            return [IsAuthenticated()]
        if self.action in teacher_actions:
            return [IsTeacherOrAdmin()]
        if self.action in student_actions:
            return [IsStudent()]
        # records 等：至少登录，下面还会再按用户角色过滤
        return [IsAuthenticated()]

    def get_queryset(self):
        u = self.request.user
        qs = Exam.objects.all()
        # 学生只能看到已发布试卷
        if getattr(u, 'is_student', False):
            qs = qs.filter(status=Exam.Status.PUBLISHED)
        return qs

    def create(self, request, *args, **kwargs):
        """创建试卷（带 items）"""
        serializer = ExamCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        with transaction.atomic():
            exam = Exam.objects.create(
                course_id=data['course'],
                title=data['title'],
                description=data.get('description', ''),
                duration_minutes=data.get('duration_minutes', 30),
                passing_score=data.get('passing_score', 60),
                total_score=data.get('total_score', 100),
                status=data.get('status', Exam.Status.DRAFT),
                creator=request.user,
            )
            for item in data.get('items', []):
                ExamQuestion.objects.create(
                    exam=exam,
                    question_id=item['question_id'],
                    score=item.get('score', 5),
                    order_no=item.get('order_no', 0),
                )
            total = sum(i.score for i in exam.items.all())
            Exam.objects.filter(pk=exam.pk).update(total_score=total or exam.total_score)
        return Response(ExamSerializer(exam).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'], url_path='publish')
    def publish(self, request, pk=None):
        """发布试卷"""
        exam = self.get_object()
        if not exam.items.exists():
            return Response({'detail': '试卷没有题目'}, status=status.HTTP_400_BAD_REQUEST)
        exam.status = Exam.Status.PUBLISHED
        exam.save()
        return Response(ExamSerializer(exam).data)

    @action(detail=True, methods=['post'], url_path='start')
    def start(self, request, pk=None):
        """学生开考：生成 ExamRecord 并下发题目（隐藏正确答案）"""
        if not getattr(request.user, 'is_student', False):
            return Response({'detail': '仅学生可开考'}, status=status.HTTP_403_FORBIDDEN)
        exam = self.get_object()
        if exam.status != Exam.Status.PUBLISHED:
            return Response({'detail': '试卷未发布'}, status=status.HTTP_400_BAD_REQUEST)
        if exam.items.count() == 0:
            return Response({'detail': '试卷没有题目'}, status=status.HTTP_400_BAD_REQUEST)
        # 未提交的记录复用（防重复开考）
        pending = ExamRecord.objects.filter(exam=exam, student=request.user, submitted_at__isnull=True).first()
        if pending:
            record = pending
        else:
            record = ExamRecord.objects.create(exam=exam, student=request.user)
        # 下发题目
        items = []
        for i, ei in enumerate(exam.items.all()):
            q = ei.question
            items.append({
                'exam_question_id': ei.id,
                'question_id': q.id,
                'question_type': q.question_type,
                'title': q.title,
                'options': q.options,
                'score': ei.score,
                'kp_id': q.kp_id,
            })
        return Response({
            'record_id': record.id,
            'exam_id': exam.id,
            'title': exam.title,
            'duration_minutes': exam.duration_minutes,
            'total_score': exam.total_score,
            'passing_score': exam.passing_score,
            'started_at': record.started_at.isoformat(),
            'items': items,
        })

    @action(detail=True, methods=['post'], url_path='submit')
    def submit(self, request, pk=None):
        """交卷 + 自动评分"""
        if not getattr(request.user, 'is_student', False):
            return Response({'detail': '仅学生可交卷'}, status=status.HTTP_403_FORBIDDEN)
        exam = self.get_object()
        serializer = ExamAnswerSubmitSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            # 找/建一条未完成的 record
            record = ExamRecord.objects.filter(
                exam=exam, student=request.user, submitted_at__isnull=True
            ).first()
            if not record:
                # 可能超时，仍允许新建并评
                record = ExamRecord.objects.create(exam=exam, student=request.user)

            # 清空旧作答（同一条 record 不能重复提交）
            if record.submitted_at:
                return Response({'detail': '已提交过'}, status=status.HTTP_400_BAD_REQUEST)

            total_score_obtained = 0.0
            submissions = {a.get('exam_question_id'): a.get('answer')
                           for a in serializer.validated_data['answers']}

            correct_kp_ids = set()
            wrong_kp_ids = set()

            for ei in exam.items.all():
                question = ei.question
                student_ans = submissions.get(ei.id)
                is_correct = _answer_equal(question.question_type, question.correct_answer, student_ans)
                score_obtained = ei.score if is_correct else 0.0
                total_score_obtained += score_obtained
                ExamAnswer.objects.create(
                    record=record,
                    question=question,
                    student_answer=student_ans,
                    is_correct=is_correct,
                    score_obtained=score_obtained,
                )
                if question.kp_id:
                    (correct_kp_ids if is_correct else wrong_kp_ids).add(question.kp_id)

            record.submitted_at = timezone.now()
            record.score = round(total_score_obtained, 2)
            record.is_passed = record.score >= exam.passing_score
            record.save()

        # 更新 analytics：薄弱知识点计数
        try:
            from analytics.models import WeakKP
            for kp_id in wrong_kp_ids:
                wk, _ = WeakKP.objects.get_or_create(student=request.user, kp_id=kp_id)
                wk.wrong_count += 1
                wk.last_wrong_at = record.submitted_at
                wk.mastery_level = max(0, wk.mastery_level - 10)
                wk.save()
            for kp_id in correct_kp_ids:
                wk = WeakKP.objects.filter(student=request.user, kp_id=kp_id).first()
                if wk:
                    wk.mastery_level = min(100, wk.mastery_level + 5)
                    wk.save()
        except Exception:
            pass

        return Response({
            'record_id': record.id,
            'score': record.score,
            'total_score': exam.total_score,
            'passing_score': exam.passing_score,
            'is_passed': record.is_passed,
            'submitted_at': record.submitted_at.isoformat(),
            'wrong_kp_ids': list(wrong_kp_ids),
        })

    @action(detail=True, methods=['get'], url_path='records')
    def records(self, request, pk=None):
        """该试卷的考试记录（教师/管理员看全班，学生看本人）"""
        exam = self.get_object()
        u = request.user
        if getattr(u, 'is_student', False):
            qs = exam.records.filter(student=u).order_by('-submitted_at')
        else:
            qs = exam.records.filter(submitted_at__isnull=False).order_by('-submitted_at')
        return Response(ExamRecordSerializer(qs, many=True).data)


# ──────────────────────────────────────────────────────────────────────────────
# 考试记录 & 错题
# ──────────────────────────────────────────────────────────────────────────────
class ExamRecordViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    queryset = ExamRecord.objects.all()
    serializer_class = ExamRecordDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        u = self.request.user
        qs = ExamRecord.objects.filter(submitted_at__isnull=False)
        if getattr(u, 'is_student', False):
            qs = qs.filter(student=u)
        return qs

    def get_object(self):
        obj = super().get_object()
        u = self.request.user
        if getattr(u, 'is_student', False) and obj.student_id != u.id:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied('无权查看他人记录')
        return obj

    @action(detail=True, methods=['get'], url_path='wrong')
    def wrong_topics(self, request, pk=None):
        """错题 + 相关学习资料推荐"""
        record = self.get_object()
        wrong = record.answers.filter(is_correct=False).select_related('question')
        result = []
        for ans in wrong:
            q = ans.question
            related_materials = []
            if q.kp_id:
                from materials.models import Material
                mats = Material.objects.filter(kp_id=q.kp_id).order_by('-view_count')[:5]
                related_materials = [
                    {
                        'id': m.id, 'title': m.title,
                        'type': m.material_type, 'url': m.url,
                    } for m in mats
                ]
            result.append({
                'exam_answer_id': ans.id,
                'question_id': q.id,
                'question_type': q.question_type,
                'title': q.title,
                'options': q.options,
                'correct_answer': q.correct_answer,
                'student_answer': ans.student_answer,
                'analysis': q.analysis,
                'kp_id': q.kp_id,
                'score_obtained': ans.score_obtained,
                'score_total': next((ei.score for ei in q.exam_items.filter(exam=record.exam)), None),
                'related_materials': related_materials,
            })
        return Response({'record_id': record.id, 'wrong_count': len(result), 'items': result})
