from rest_framework import serializers
from .models import Question, Exam, ExamQuestion, ExamRecord, ExamAnswer


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('id', 'course', 'kp', 'question_type', 'title', 'options',
                  'correct_answer', 'analysis', 'difficulty', 'creator', 'created_at')
        read_only_fields = ('creator', 'created_at')


class QuestionPublicSerializer(serializers.ModelSerializer):
    """用于考试下发（隐藏正确答案）"""
    class Meta:
        model = Question
        fields = ('id', 'question_type', 'title', 'options', 'analysis', 'difficulty', 'kp')
        read_only_fields = fields


class ExamQuestionSerializer(serializers.ModelSerializer):
    question = QuestionSerializer(read_only=True)
    question_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = ExamQuestion
        fields = ('id', 'exam', 'question', 'question_id', 'score', 'order_no')


class ExamSerializer(serializers.ModelSerializer):
    items = ExamQuestionSerializer(many=True, read_only=True)
    question_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Exam
        fields = ('id', 'course', 'title', 'description', 'duration_minutes',
                  'passing_score', 'total_score', 'status', 'creator', 'created_at',
                  'items', 'question_count')
        read_only_fields = ('creator', 'created_at')


class ExamCreateSerializer(serializers.Serializer):
    """创建试卷（带题目列表）"""
    course = serializers.IntegerField()
    title = serializers.CharField(max_length=200)
    description = serializers.CharField(required=False, default='')
    duration_minutes = serializers.IntegerField(default=30)
    passing_score = serializers.FloatField(default=60)
    total_score = serializers.FloatField(default=100)
    status = serializers.ChoiceField(choices=Exam.Status.choices, default=Exam.Status.DRAFT)
    items = serializers.ListField(child=serializers.DictField(), required=True)
    # items 每项: {"question_id": 1, "score": 5, "order_no": 1}


class ExamAnswerSubmitSerializer(serializers.Serializer):
    """学生提交答案"""
    answers = serializers.ListField(child=serializers.DictField(), required=True)
    # answers: [{"exam_question_id": 1, "answer": "A" 或 ["A","C"] 或 true}, ...]


class ExamRecordSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title', read_only=True)

    class Meta:
        model = ExamRecord
        fields = ('id', 'exam', 'exam_title', 'started_at', 'submitted_at',
                  'score', 'is_passed')


class ExamAnswerSerializer(serializers.ModelSerializer):
    question = QuestionPublicSerializer(read_only=True)

    class Meta:
        model = ExamAnswer
        fields = ('id', 'question', 'student_answer', 'is_correct', 'score_obtained')


class ExamRecordDetailSerializer(serializers.ModelSerializer):
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    answers = ExamAnswerSerializer(many=True, read_only=True)

    class Meta:
        model = ExamRecord
        fields = ('id', 'exam', 'exam_title', 'started_at', 'submitted_at',
                  'score', 'is_passed', 'answers')
