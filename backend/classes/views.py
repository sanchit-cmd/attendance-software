from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.contrib import messages
from enrollments.models import Enrollment
from attendance.models import Attendance, BatchChoices
from accounts.models import User

# Create your views here.


def is_teacher(user):
    return user.is_authenticated and user.role == "TEACHER"


@user_passes_test(is_teacher)
def dashboard(request):
    context = {}

    if request.method == "POST":
        pass

    teacher = request.user.teacher.first()
    subject = teacher.subject
    context["subject"] = subject

    enrollments = subject.enrollments.all().order_by("-created_at")
    context["enrollments"] = enrollments

    return render(request, "classes/dashboard.html", context)


@user_passes_test(is_teacher)
def search_student_for_attendance(request):
    teacher = request.user.teacher.first()
    subject = teacher.subject

    context = {
        "subject": subject,
        "search_results": [],
    }

    if request.method == "GET":
        query = request.GET.get("query", "").strip()
        if query:
            # Search for students enrolled in the teacher's subject
            context["search_results"] = subject.enrollments.filter(
                Q(student__name__icontains=query)
                | Q(student__user__name__icontains=query),
            ).distinct()

    return render(request, "classes/search_student.html", context)


@user_passes_test(is_teacher)
def mark_attendance(request, enrollment_id):
    teacher = request.user.teacher.first()
    enrollment = get_object_or_404(
        Enrollment, id=enrollment_id, subject=teacher.subject
    )

    if request.method == "POST":
        attendance_date = request.POST.get("attendance_date")
        attendance_batch = request.POST.get("attendance_batch")
        is_present = request.POST.get("is_present") == "on"

        if attendance_date and attendance_batch:
            attendance, created = Attendance.objects.get_or_create(
                enrollment=enrollment,
                attendance_date=attendance_date,
                attendance_batch=attendance_batch,
                defaults={"is_present": is_present},
            )

            if not created:
                attendance.is_present = is_present
                attendance.save()
                messages.success(request, "Attendance updated successfully.")
            else:
                messages.success(request, "Attendance marked successfully.")

            return redirect("search_student_for_attendance")
        else:
            messages.error(request, "Please provide all required fields.")

    context = {
        "enrollment": enrollment,
        "batch_choices": BatchChoices.choices,
    }

    return render(request, "classes/mark_attendance.html", context)
