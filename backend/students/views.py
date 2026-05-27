from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.messages import error
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student


# Create your views here.
def is_student(user):
    return user.is_authenticated and user.role == "STUDENT"


@user_passes_test(is_student)
def dashboard(request):
    context = {}

    students = Student.objects.filter(user=request.user)
    context["students"] = students

    return render(request, "students/dashboard.html", context)


@user_passes_test(is_student)
def student_enrollments(request, student_id):
    student = get_object_or_404(Student, id=student_id, user=request.user)

    context = {
        "student": student,
        "active_enrollments": student.enrollments.filter(status="ACTIVE"),
        "inactive_enrollments": student.enrollments.filter(status="INACTIVE"),
    }

    return render(request, "students/student_enrollments.html", context)


@user_passes_test(is_student)
def enrollment_detail(request, student_id, enrollment_id):
    student = get_object_or_404(Student, id=student_id, user=request.user)
    enrollment = get_object_or_404(student.enrollments.all(), id=enrollment_id)
    attendance_records = enrollment.attendances.all().order_by("-attendance_date")

    context = {
        "student": student,
        "enrollment": enrollment,
        "attendance_records": attendance_records,
    }

    return render(request, "students/enrollments_details.html", context)
