from rest_framework import viewsets, status, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import F

from .models import Material, MaterialView
from .serializers import (
    MaterialSerializer, MaterialViewSerializer, MaterialViewCreateSerializer,
)
from accounts.permissions import IsTeacherOrAdmin, IsStudent


class MaterialViewSet(viewsets.ModelViewSet):
    """资料：登录可看；教师/管理员可增改；只能删自己的"""
    queryset = Material.objects.select_related('course', 'kp', 'uploader').all()
    serializer_class = MaterialSerializer
    filterset_fields = ('course', 'kp', 'material_type', 'uploader')
    search_fields = ('title',)

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'record_view'):
            return [IsAuthenticated()]
        return [IsTeacherOrAdmin()]

    def perform_create(self, serializer):
        serializer.save(uploader=self.request.user)

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if self.action in ('update', 'partial_update', 'destroy'):
            if not getattr(request.user, 'is_admin', False) and obj.uploader_id != request.user.id:
                from rest_framework.exceptions import PermissionDenied
                raise PermissionDenied('只能修改自己上传的资料')

    def retrieve(self, request, *args, **kwargs):
        # 查看即 +1 浏览量
        obj = self.get_object()
        Material.objects.filter(pk=obj.pk).update(view_count=F('view_count') + 1)
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='view')
    def record_view(self, request, pk=None):
        """学生上报一次学习行为（用于统计和学习记录）"""
        if not getattr(request.user, 'is_student', False):
            return Response({'detail': '仅学生可记录学习'}, status=status.HTTP_403_FORBIDDEN)
        material = self.get_object()
        serializer = MaterialViewCreateSerializer(data={'material_id': pk, **request.data})
        serializer.is_valid(raise_exception=True)
        record = MaterialView.objects.create(
            material=material,
            student=request.user,
            progress_percent=serializer.validated_data['progress_percent'],
            duration_seconds=serializer.validated_data['duration_seconds'],
            finished=serializer.validated_data['finished'],
        )
        return Response({'id': record.id}, status=status.HTTP_201_CREATED)


class MaterialViewHistoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """我的学习记录"""
    serializer_class = MaterialViewSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        return MaterialView.objects.filter(student=self.request.user).select_related('material')
