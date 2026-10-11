from django.contrib.auth import views as auth_views
from django.urls import path

from . import views
from .forms import EmailOrUsernameAuthenticationForm

urlpatterns = [
    path("", views.home, name="home"),

    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=EmailOrUsernameAuthenticationForm,
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),

    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile, name="profile"),

    path("tasks/new/", views.task_create, name="task_create"),
    path("tasks/<int:task_id>/edit/", views.task_edit, name="task_edit"),
    path("tasks/<int:task_id>/delete/", views.task_delete, name="task_delete"),
    path(
        "tasks/<int:task_id>/status/",
        views.task_status_update,
        name="task_status_update",
    ),

    path("members/", views.member_list, name="members"),
    path("members/new/", views.member_create, name="member_create"),
]