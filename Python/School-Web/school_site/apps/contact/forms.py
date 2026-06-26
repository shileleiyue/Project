from django import forms
from .models import Message, PrincipalMail


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['sender_name', 'email', 'content']
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'rows': 4
            }),
        }


class PrincipalMailForm(forms.ModelForm):
    class Meta:
        model = PrincipalMail
        fields = ['sender_name', 'email', 'subject', 'content']
        widgets = {
            'sender_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': ' '
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': ' ',
                'rows': 4
            }),
        }