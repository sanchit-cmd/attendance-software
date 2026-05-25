from django.db import models


# Create your models here.
class Subject(models.Model):
    name = models.CharField(
        max_length=255,
    )

    def __str__(self):
        return self.name


class Teacher(models.Model):
    name = models.CharField(
        max_length=255,
    )
    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="teacher",
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="teacher",
    )

    def __str__(self):
        return self.name
