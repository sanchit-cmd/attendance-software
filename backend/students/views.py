from django.shortcuts import render, redirect
from django.contrib.messages import error
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Student


# Create your views here.
def is_student(user):
    return user.is_authenticated and user.students.exists()


@user_passes_test(is_student)
def dashboard(request):
    context = {}

    students = Student.objects.filter(user=request.user)
    context["students"] = students

    return render(request, "students/dashboard.html", context)


@user_passes_test(is_student)
def student_profile(request, student_id):
    context = {}
    student = Student.objects.get(id=student_id, user=request.user)

    if not student:
        error(request, "Student not found.")
        return redirect("dashboard")
    return render(request, "students/dashboard_profile.html", {"student": student})
