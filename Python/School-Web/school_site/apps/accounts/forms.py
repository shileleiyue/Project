from django import forms
from django.contrib.auth import authenticate
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': ' ',
            'autocomplete': 'current-password'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError('用户名或密码错误')
            if not user.is_active:
                raise forms.ValidationError('该账户已被停用')
            cleaned_data['user'] = user 
        return cleaned_data


class ParentBindForm(forms.Form):
    """家长绑定学生"""
    student_id = forms.CharField(
        label='学生学号',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )
    student_name = forms.CharField(
        label='学生姓名',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': ' '})
    )

    def __init__(self, *args, **kwargs):
        self.parent_user = kwargs.pop('parent_user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        sid = cleaned_data.get('student_id')
        sname = cleaned_data.get('student_name')
        if sid and sname:
            try:
                student = User.objects.get(student_id=sid, role='student', real_name=sname)
                cleaned_data['student'] = student
            except User.DoesNotExist:
                raise forms.ValidationError('未找到该学生，请核实学号和姓名')
        return cleaned_data

    def save(self):
        student = self.cleaned_data['student']
        self.parent_user.children.add(student)
        return student