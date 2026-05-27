from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(
        "search-student/",
        views.search_student_for_attendance,
        name="search_student_for_attendance",
    ),
    path(
        "mark-attendance/<int:enrollment_id>/",
        views.mark_attendance,
        name="mark_attendance",
    ),
]
