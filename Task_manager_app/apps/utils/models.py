from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        "user.User",
        null=True,
        on_delete=models.CASCADE,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        "user.User",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="%(class)s_updated_by",
    )

    class Meta:
        abstract = True
