from django import forms
from apps.todo.models import TaskManager, Comment, AddContent
from ckeditor.fields import RichTextField


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["parent_comment", "body"]
        widgets = {"parent_comment": forms.HiddenInput(), "body": RichTextField()}


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = TaskManager
        fields = ["title", "description", "assigned_to", "status", "estimated_time"]


class AddContentform(forms.ModelForm):
    is_draft = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = AddContent
        fields = ["content", "is_draft"]
