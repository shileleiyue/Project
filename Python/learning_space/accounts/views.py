"""accounts 视图"""
from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from .models import Student, Teacher, Role, StudentCourse
from .serializers import (
    RegisterSerializer, UserPublicSerializer,
    StudentSerializer, TeacherSerializer, AdminStudentCreateSerializer,
    StudentCourseSerializer, StudentSerializerWithCourses,
)
from .permissions import IsAdmin, IsStudent, IsOwnerOrAdmin, IsTeacherOrAdmin


User = get_user_model()


class AuthViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """注册 + 查看/修改本人信息"""
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def get_permissions(self):
        if self.action == 'create':   # /api/auth/register/
            return [AllowAny()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request):
        """当前登录用户"""
        user = request.user
        if request.method in ('PUT', 'PATCH'):
            serializer = UserPublicSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.update(user, serializer.validated_data)
            return Response(UserPublicSerializer(user).data)
        return Response(UserPublicSerializer(user).data)


class StudentViewSet(viewsets.ModelViewSet):
    """
    学生管理：
    - 管理员：CRUD 所有学生
    - 学生：只读/修改本人资料
    """
    queryset = Student.objects.select_related('user').all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ('list', 'create'):
            return [IsAdmin()]
        if self.action == 'me':
            return [IsStudent()]
        # retrieve/update/destroy 目标对象走对象级权限
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'create':
            return AdminStudentCreateSerializer
        return StudentSerializer

    def get_queryset(self):
        u = self.request.user
        if getattr(u, 'is_admin', False):
            return Student.objects.select_related('user').all()
        if getattr(u, 'is_student', False):
            return Student.objects.filter(user=u).select_related('user')
        return Student.objects.none()

    def get_object(self):
        # 学生访问 /api/students/me/ 时固定返回本人
        if self.action == 'me':
            return self.request.user.student_profile
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request):
        """学生查看/修改自己的资料（含联系方式）"""
        student = request.user.student_profile
        if request.method in ('PUT', 'PATCH'):
            serializer = StudentSerializer(student, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(StudentSerializer(student).data)


class TeacherViewSet(viewsets.ReadOnlyModelViewSet):
    """教师列表（只读：教师/管理员可看）"""
    queryset = Teacher.objects.select_related('user').all()
    serializer_class = TeacherSerializer
    permission_classes = [IsTeacherOrAdmin]


# ─── 学生-课程-成绩 ──────────────────────────────────────────────────────────
class StudentCourseViewSet(viewsets.ModelViewSet):
    """学生成绩：admin 全权限 CRUD，student 只读自己的"""
    queryset = StudentCourse.objects.select_related('student', 'course').all()
    serializer_class = StudentCourseSerializer
    filterset_fields = ('student', 'course', 'semester')

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            return [IsAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        u = self.request.user
        if getattr(u, 'is_admin', False):
            return self.queryset
        if getattr(u, 'is_student', False) and hasattr(u, 'student_profile'):
            return self.queryset.filter(student=u.student_profile)
        return self.queryset.none()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'], url_path='my-scores')
    def my_scores(self, request):
        """学生：查看自己所有课程成绩"""
        if not getattr(request.user, 'is_student', False):
            return Response({'detail': '仅学生可查看'}, status=403)
        qs = StudentCourse.objects.filter(student=request.user.student_profile) \
            .select_related('course')
        return Response(StudentCourseSerializer(qs, many=True).data)
