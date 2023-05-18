from django.db import models
from apps.utils.models import TimeStampModel
from apps.utils.enum import TaskStatus, TaskFeedback
from django.contrib.auth import get_user_model

# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

User = get_user_model()

choice_feedback = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5))


class TaskManager(TimeStampModel):
    title = models.CharField(max_length=150)
    description = RichTextUploadingField()
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=140, choices=TaskStatus.choices())
    estimated_time = models.IntegerField(null=True)

    def __str__(self):
        return self.title


class Comment(TimeStampModel):
    task = models.ForeignKey(
        TaskManager, on_delete=models.CASCADE, related_name="%(class)s"
    )
    parent_comment = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.CASCADE
    )
    body = RichTextUploadingField()

    def __str__(self):
        return self.body


class Feedback(TimeStampModel):
    task = models.ForeignKey(
        TaskManager, on_delete=models.CASCADE, related_name="%(class)s"
    )
    rating = models.IntegerField(choices=choice_feedback)


class AddContent(TimeStampModel):
    task = models.ForeignKey(
        TaskManager, on_delete=models.CASCADE, related_name="taskcontent"
    )
    content = RichTextUploadingField()
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.task.title} ({self.task.id}): {self.content}"
