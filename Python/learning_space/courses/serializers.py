from rest_framework import serializers
from .models import Course, KnowledgePoint


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'code', 'name', 'description', 'cover', 'teacher', 'teacher_name',
                  'is_active', 'created_at')
        read_only_fields = ('created_at',)

    def get_teacher_name(self, obj):
        if obj.teacher_id:
            from accounts.models import Teacher
            t = Teacher.objects.filter(user=obj.teacher).first()
            return t.name if t else obj.teacher.username
        return None


class KnowledgePointSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = KnowledgePoint
        fields = ('id', 'course', 'parent', 'title', 'description', 'order_no', 'children')

    def get_children(self, obj):
        return KnowledgePointSerializer(obj.children.all().order_by('order_no', 'id'), many=True).data


class KnowledgePointFlatSerializer(serializers.ModelSerializer):
    """扁平版本，不递归"""
    class Meta:
        model = KnowledgePoint
        fields = ('id', 'course', 'parent', 'title', 'description', 'order_no')
