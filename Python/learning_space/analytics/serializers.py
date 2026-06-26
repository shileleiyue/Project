from rest_framework import serializers
from .models import WeakKP, DailyStat, LearningPreference, Recommendation


class WeakKPSerializer(serializers.ModelSerializer):
    kp_title = serializers.CharField(source='kp.title', read_only=True)
    course_name = serializers.CharField(source='kp.course.name', read_only=True)

    class Meta:
        model = WeakKP
        fields = ('id', 'kp', 'kp_title', 'course_name', 'wrong_count', 'mastery_level', 'last_wrong_at')


class DailyStatSerializer(serializers.ModelSerializer):
    date = serializers.DateField(source='stat_date', read_only=True)
    duration_minutes = serializers.SerializerMethodField()

    class Meta:
        model = DailyStat
        fields = ('id', 'stat_date', 'date', 'total_duration_seconds', 'duration_minutes',
                  'materials_count', 'kps_count', 'avg_effective_rate')

    def get_duration_minutes(self, obj):
        return round(obj.total_duration_seconds / 60, 1)


class LearningPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPreference
        fields = ('id', 'preferred_material_type', 'active_hours', 'subject_weights', 'updated_at')


class RecommendationSerializer(serializers.ModelSerializer):
    material_title = serializers.CharField(source='material.title', read_only=True)
    material_type = serializers.CharField(source='material.material_type', read_only=True)
    material_url = serializers.SerializerMethodField()

    class Meta:
        model = Recommendation
        fields = ('id', 'material', 'material_title', 'material_type', 'material_url',
                  'reason', 'score', 'is_read', 'created_at')

    def get_material_url(self, obj):
        if obj.material.url:
            return obj.material.url
        if obj.material.file:
            try:
                from django.contrib.sites.models import Site
                scheme = 'http'
                return f'{scheme}://{obj.material.file.url}'
            except Exception:
                return obj.material.file.url
        return None
