# tasks/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'content', 'due_datetime', 'importance']
        widgets = {
            'due_datetime': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control bg-dark text-success border-success'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-success border-success',
                'placeholder': 'Enter task title...'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-success border-success',
                'rows': 3,
                'placeholder': 'Optional details...'
            }),
            'importance': forms.Select(attrs={
                'class': 'form-select bg-dark text-success border-success'
            }),
        }

    def clean_due_datetime(self):
        due = self.cleaned_data.get('due_datetime')
        if not self.instance.pk and due and due <= timezone.now():
            raise forms.ValidationError("Due date must be in the future.")
        return due


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control bg-dark text-success border-success'
            })