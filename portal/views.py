from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .decorators import admin_required, is_admin_user
from .forms import MemberCreationForm, StatusUpdateForm, TaskForm
from .models import Task, UserProfile


def register(request):
    """
    Allow new users to register for TeamSpace.
    Newly registered users receive the Member role.
    """
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = MemberCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        messages.success(
            request,
            "Your account has been created successfully. Please sign in.",
        )

        return redirect("login")

    return render(
        request,
        "registration/register.html",
        {"form": form},
    )


def home(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    return redirect("login")


@login_required
def dashboard(request):
    admin_mode = is_admin_user(request.user)

    tasks = Task.objects.select_related("assigned_to", "created_by")

    if not admin_mode:
        tasks = tasks.filter(assigned_to=request.user)

    search = request.GET.get("q", "").strip()
    status = request.GET.get("status", "").strip()
    priority = request.GET.get("priority", "").strip()

    if search:
        tasks = tasks.filter(
            Q(title__icontains=search)
            | Q(description__icontains=search)
        )

    valid_statuses = {
        choice[0] for choice in Task.Status.choices
    }

    valid_priorities = {
        choice[0] for choice in Task.Priority.choices
    }

    if status in valid_statuses:
        tasks = tasks.filter(status=status)

    if priority in valid_priorities:
        tasks = tasks.filter(priority=priority)

    base_tasks = (
        Task.objects.all()
        if admin_mode
        else Task.objects.filter(assigned_to=request.user)
    )

    context = {
        "is_admin": admin_mode,
        "tasks": tasks,
        "search": search,
        "selected_status": status,
        "selected_priority": priority,
        "total_count": base_tasks.count(),
        "todo_count": base_tasks.filter(
            status=Task.Status.TODO
        ).count(),
        "progress_count": base_tasks.filter(
            status=Task.Status.IN_PROGRESS
        ).count(),
        "completed_count": base_tasks.filter(
            status=Task.Status.COMPLETED
        ).count(),
        "overdue_count": base_tasks.filter(
            due_date__lt=timezone.localdate()
        ).exclude(
            status=Task.Status.COMPLETED
        ).count(),
        "status_choices": Task.Status.choices,
        "priority_choices": Task.Priority.choices,
    }

    return render(
        request,
        "portal/dashboard.html",
        context,
    )


@admin_required
def task_create(request):
    form = TaskForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.created_by = request.user
        task.save()

        messages.success(
            request,
            f'Task "{task.title}" was created.',
        )

        return redirect("dashboard")

    return render(
        request,
        "portal/task_form.html",
        {
            "form": form,
            "page_title": "Create task",
            "is_admin": True,
        },
    )


@admin_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    form = TaskForm(
        request.POST or None,
        instance=task,
    )

    if request.method == "POST" and form.is_valid():
        form.save()

        messages.success(
            request,
            "Task updated successfully.",
        )

        return redirect("dashboard")

    return render(
        request,
        "portal/task_form.html",
        {
            "form": form,
            "page_title": "Edit task",
            "is_admin": True,
            "task": task,
        },
    )


@admin_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == "POST":
        title = task.title
        task.delete()

        messages.success(
            request,
            f'Task "{title}" was deleted.',
        )

        return redirect("dashboard")

    return render(
        request,
        "portal/task_confirm_delete.html",
        {
            "task": task,
            "is_admin": True,
        },
    )


@login_required
def task_status_update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    admin_mode = is_admin_user(request.user)

    if not admin_mode and task.assigned_to_id != request.user.id:
        messages.error(
            request,
            "You can update only tasks assigned to you.",
        )
        return redirect("dashboard")

    if request.method == "POST":
        form = StatusUpdateForm(request.POST)

        if form.is_valid():
            task.status = form.cleaned_data["status"]
            task.save(update_fields=["status", "updated_at"])

            messages.success(
                request,
                "Task status updated.",
            )
        else:
            messages.error(
                request,
                "Please select a valid task status.",
            )

    return redirect("dashboard")


@admin_required
def member_list(request):
    members = (
        UserProfile.objects.select_related("user")
        .filter(
            role=UserProfile.Role.MEMBER,
            user__is_active=True,
        )
        .order_by(
            "user__first_name",
            "user__username",
        )
    )

    return render(
        request,
        "portal/members.html",
        {
            "members": members,
            "is_admin": True,
        },
    )


@admin_required
def member_create(request):
    form = MemberCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()

        messages.success(
            request,
            f"Member account created for {user.username}.",
        )

        return redirect("members")

    return render(
        request,
        "portal/member_form.html",
        {
            "form": form,
            "is_admin": True,
        },
    )


@login_required
def profile(request):
    return render(
        request,
        "portal/profile.html",
        {
            "is_admin": is_admin_user(request.user),
        },
    )