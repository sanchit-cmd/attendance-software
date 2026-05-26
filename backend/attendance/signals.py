from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Attendance
from enrollments.models import EnrollmentStatus


@receiver(post_save, sender=Attendance)
def update_enrollment_dates(sender, instance, created, **kwargs):
    """
    Auto-update enrollment start_date and end_date based on attendance records.
    - start_date: Always set to the earliest attendance date
    - end_date: Set to the latest attendance date when count equals total_classes
    - status: Changed to INACTIVE when end_date is set
    """
    if created:
        enrollment = instance.enrollment
        attendances = enrollment.attendances.all().order_by("attendance_date")
        attendance_count = attendances.count()

        # Always set start_date to the earliest attendance date
        earliest_attendance = attendances.first()
        should_save = False

        if enrollment.start_date != earliest_attendance.attendance_date:
            enrollment.start_date = earliest_attendance.attendance_date
            should_save = True

        # Set end_date and change status to INACTIVE when total attendances equal total_classes
        if attendance_count == enrollment.total_classes:
            latest_attendance = attendances.last()
            enrollment.end_date = latest_attendance.attendance_date
            enrollment.status = EnrollmentStatus.INACTIVE
            enrollment.save(update_fields=["end_date", "status"])
        elif should_save:
            enrollment.save(update_fields=["start_date"])
