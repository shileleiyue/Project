from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Course, KnowledgePoint
from .serializers import CourseSerializer, KnowledgePointSerializer, KnowledgePointFlatSerializer
from accounts.permissions import IsTeacherOrAdmin, IsTeacher, IsAdmin


class CourseViewSet(viewsets.ModelViewSet):
    """课程：登录可看；教师/管理员可增改删；教师只能改自己的"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    filterset_fields = ('teacher', 'is_active', 'code', 'name')
    search_fields = ('code', 'name')

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'knowledge_tree'):
            return [IsAuthenticated()]
        return [IsTeacherOrAdmin()]

    def perform_create(self, serializer):
        # 教师新建课程默认设为自己
        user = self.request.user
        if getattr(user, 'is_teacher', False) and not serializer.validated_data.get('teacher'):
            serializer.save(teacher=user)
        else:
            serializer.save()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        # 非管理员教师不能改别人的课
        if self.action in ('update', 'partial_update', 'destroy'):
            if not getattr(request.user, 'is_admin', False) and obj.teacher_id != request.user.id:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('你没有权限修改他人的课程')

    @action(detail=True, methods=['get'], url_path='knowledge')
    def knowledge_tree(self, request, pk=None):
        """返回该课程的知识点树"""
        course = self.get_object()
        roots = course.knowledge_points.filter(parent__isnull=True).order_by('order_no', 'id')
        data = KnowledgePointSerializer(roots, many=True).data
        return Response({'course_id': course.id, 'course_name': course.name, 'points': data})


class KnowledgePointViewSet(viewsets.ModelViewSet):
    """知识点：教师/管理员可增改，学生只读"""
    queryset = KnowledgePoint.objects.all()
    serializer_class = KnowledgePointFlatSerializer
    filterset_fields = ('course', 'parent')
    search_fields = ('title',)

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return [IsAuthenticated()]
        return [IsTeacherOrAdmin()]
