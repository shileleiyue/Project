from rest_framework import serializers
from .models import Material, MaterialView


class MaterialSerializer(serializers.ModelSerializer):
    uploader_name = serializers.SerializerMethodField()
    course_name = serializers.CharField(source='course.name', read_only=True)
    kp_title = serializers.CharField(source='kp.title', read_only=True, default=None)

    class Meta:
        model = Material
        fields = ('id', 'course', 'course_name', 'kp', 'kp_title', 'title', 'material_type',
                  'file', 'url', 'duration', 'description', 'uploader', 'uploader_name',
                  'view_count', 'created_at')
        read_only_fields = ('uploader', 'view_count', 'created_at')

    def get_uploader_name(self, obj):
        return obj.uploader.username if obj.uploader else None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # file 字段返回完整前端可用 URL
        if instance.file:
            data['file'] = self.context['request'].build_absolute_uri(instance.file.url)
        return data


class MaterialViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialView
        fields = ('id', 'material', 'progress_percent', 'duration_seconds',
                  'started_at', 'ended_at', 'finished')


class MaterialViewCreateSerializer(serializers.Serializer):
    material_id = serializers.IntegerField()
    progress_percent = serializers.FloatField(default=0)
    duration_seconds = serializers.IntegerField(default=0)
    finished = serializers.BooleanField(default=False)
