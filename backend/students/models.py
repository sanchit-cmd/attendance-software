from django.db import models


class Student(models.Model):
    name = models.CharField(
        max_length=255,
    )
    date_of_birth = models.DateField()

    user = models.ForeignKey(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="students",
    )

    def __str__(self):
        return f"{self.name} ({self.user})"
