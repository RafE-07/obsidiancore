from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Case, When, Value, BooleanField, Q
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Task
from .forms import TaskForm, UserRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome to ObsidianCore. You are now logged in.")
            return redirect('task_list')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user)
    tasks = tasks.annotate(
        is_expired=Case(
            When(completed=False, due_datetime__lt=timezone.now(), then=Value(True)),
            default=Value(False),
            output_field=BooleanField()
        )
    )

    search_query = request.GET.get('search', '')
    importance_filter = request.GET.get('importance', '')
    if search_query:
        tasks = tasks.filter(title__icontains=search_query)
    if importance_filter:
        tasks = tasks.filter(importance=importance_filter)

   
    tasks = tasks.order_by('completed', 'is_expired', 'due_datetime')

    paginator = Paginator(tasks, 10)
    page = request.GET.get('page')
    try:
        tasks_page = paginator.page(page)
    except PageNotAnInteger:
        tasks_page = paginator.page(1)
    except EmptyPage:
        tasks_page = paginator.page(paginator.num_pages)

    
    title_suggestions = Task.objects.filter(user=request.user).values_list('title', flat=True).distinct()

    context = {
        'tasks': tasks_page,
        'search_query': search_query,
        'importance_filter': importance_filter,
        'title_suggestions': title_suggestions,
        'importance_choices': Task.IMPORTANCE_CHOICES,
    }
    return render(request, 'tasks/task_list.html', context)


@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, "Task created successfully.")
            if 'save_add_another' in request.POST:
                return redirect('task_create')
            return redirect('task_list')
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'action': 'Create'
    })


@login_required
def task_update(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated.")
            return redirect('task_list')
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {
        'form': form,
        'action': 'Edit'
    })


@login_required
def task_delete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.delete()
        messages.success(request, "Task deleted.")
    return redirect('task_list')


@login_required
def task_complete(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
        task.completed = True
        task.save()
        messages.success(request, "Task marked as completed.")
    return redirect('task_list')

