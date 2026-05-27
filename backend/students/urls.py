from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "<int:student_id>/enrollments/",
        views.student_enrollments,
        name="student_enrollments",
    ),
    path(
        "<int:student_id>/enrollments/<int:enrollment_id>/",
        views.enrollment_detail,
        name="enrollment_detail",
    ),
]
