from django.db import models

# Create your models here.


class BatchChoices(models.TextChoices):
    BATCH_4PM_5PM = "4pm - 5pm"
    BATCH_5PM_6PM = "5pm - 6pm"
    BATCH_6PM_7PM = "6pm - 7pm"
    BATCH_7PM_8PM = "7pm - 8pm"
    BATCH_11AM_12PM = "11am - 12pm"
    BATCH_12PM_1PM = "12pm - 1pm"
    BATCH_1PM_2PM = "1pm - 2pm"
    BATCH_2PM_3PM = "2pm - 3pm"


class Attendance(models.Model):
    enrollment = models.ForeignKey(
        "enrollments.Enrollment",
        on_delete=models.CASCADE,
        related_name="attendances",
    )

    attendance_date = models.DateField()
    attendance_batch = models.CharField(
        max_length=20,
        choices=BatchChoices.choices,
        default=BatchChoices.BATCH_5PM_6PM,
    )

    is_present = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["enrollment", "attendance_date", "attendance_batch"],
                name="unique_enrollment_date_batch",
            )
        ]
        ordering = ["attendance_date"]

    def __str__(self):
        return f"{self.enrollment} - {self.attendance_date} - {self.attendance_batch}"
