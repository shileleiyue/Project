"""accounts 序列化器"""
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Student, Teacher, Role

User = get_user_model()


class UserPublicSerializer(serializers.ModelSerializer):
    """公开用户信息（不含密码）"""
    class Meta:
        model = User
        fields = ('id', 'username', 'role', 'email', 'phone', 'first_name', 'last_name', 'avatar', 'date_joined')
        read_only_fields = ('id', 'date_joined')


class RegisterSerializer(serializers.ModelSerializer):
    """注册"""
    password = serializers.CharField(write_only=True, min_length=6, required=True)
    role = serializers.ChoiceField(choices=Role.choices, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'role', 'email', 'phone', 'first_name', 'last_name')

    def create(self, validated_data):
        password = validated_data.pop('password')
        role = validated_data.pop('role', Role.STUDENT)
        user = User.objects.create_user(password=password, role=role, **validated_data)
        return user


class StudentSerializer(serializers.ModelSerializer):
    """学生资料"""
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)
    email = serializers.CharField(source='user.email', required=False)
    phone = serializers.CharField(source='user.phone', required=False)

    class Meta:
        model = Student
        fields = ('id', 'username', 'role', 'student_no', 'name', 'college', 'major',
                  'grade', 'contact', 'email', 'phone')

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        # 学生允许修改联系方式 + 邮箱 + 手机号
        if 'contact' in validated_data:
            instance.contact = validated_data['contact']
        instance.name = validated_data.get('name', instance.name)
        instance.college = validated_data.get('college', instance.college)
        instance.major = validated_data.get('major', instance.major)
        instance.grade = validated_data.get('grade', instance.grade)
        instance.student_no = validated_data.get('student_no', instance.student_no)
        instance.save()
        if user_data:
            for k, v in user_data.items():
                setattr(instance.user, k, v)
            instance.user.save()
        return instance


class TeacherSerializer(serializers.ModelSerializer):
    """教师资料"""
    username = serializers.CharField(source='user.username', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'username', 'role', 'teacher_no', 'name', 'title', 'department', 'contact')


class AdminStudentCreateSerializer(serializers.Serializer):
    """管理员一键创建学生（同时建 User + Student）"""
    username = serializers.CharField(max_length=64)
    password = serializers.CharField(max_length=64, write_only=True, default='123456')
    student_no = serializers.CharField(max_length=32)
    name = serializers.CharField(max_length=64)
    college = serializers.CharField(max_length=128, required=False, default='')
    major = serializers.CharField(max_length=128, required=False, default='')
    grade = serializers.CharField(max_length=16, required=False, default='')
    contact = serializers.CharField(max_length=128, required=False, default='')
    email = serializers.EmailField(required=False, default='')
    phone = serializers.CharField(max_length=32, required=False, default='')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('用户名已存在')
        return value

    def validate_student_no(self, value):
        if Student.objects.filter(student_no=value).exists():
            raise serializers.ValidationError('学号已存在')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create_user(
            username=validated_data['username'],
            password=password,
            role=Role.STUDENT,
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            first_name=validated_data.get('name', ''),
        )
        student = Student.objects.create(
            user=user,
            student_no=validated_data['student_no'],
            name=validated_data['name'],
            college=validated_data.get('college', ''),
            major=validated_data.get('major', ''),
            grade=validated_data.get('grade', ''),
            contact=validated_data.get('contact', ''),
        )
        return student


# ─── 学生-课程-成绩 ──────────────────────────────────────────────────────────
class StudentCourseSerializer(serializers.ModelSerializer):
    course_name = serializers.CharField(source='course.name', read_only=True)
    course_code = serializers.CharField(source='course.code', read_only=True)
    student_name = serializers.CharField(source='student.name', read_only=True)
    student_no = serializers.CharField(source='student.student_no', read_only=True)

    class Meta:
        from .models import StudentCourse
        model = StudentCourse
        fields = ('id', 'student', 'student_no', 'student_name',
                  'course', 'course_code', 'course_name',
                  'score', 'semester', 'enrolled_at')
        read_only_fields = ('enrolled_at', 'student_no', 'student_name', 'course_code', 'course_name')


class StudentSerializerWithCourses(StudentSerializer):
    """学生 + 嵌套成绩列表（用于 admin 查看完整信息）"""
    courses = serializers.SerializerMethodField()

    class Meta(StudentSerializer.Meta):
        fields = StudentSerializer.Meta.fields + ('courses',)

    def get_courses(self, obj):
        from .models import StudentCourse
        return StudentCourseSerializer(
            obj.course_scores.select_related('course'), many=True
        ).data
