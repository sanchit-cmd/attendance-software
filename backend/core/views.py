from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user = request.user
    if user.role == "ADMIN":
        return redirect("/admin/")
    elif user.role == "TEACHER":
        return redirect("/teachers/")
    elif user.role == "STUDENT":
        return redirect("/students/")
    
    return redirect("/accounts/login/")
