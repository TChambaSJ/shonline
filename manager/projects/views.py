from django.shortcuts import render, redirect
from .models import Task, Project
from .forms import TaskForm, ProjectForm

from django.contrib.auth.decorators import login_required

# ******************* Create Views ***********************

@login_required(login_url='login')
def taskCreate(request, pk):
    project = Project.objects.get(id=pk)
    form = TaskForm(initial={'project': project})
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')

    context = {'form': form}
    return render(request, 'projects/task_form.html', context)

@login_required(login_url='login')
def projectCreate(request):
    form = ProjectForm()
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    context = {'form':form}
    return render(request, 'projects/project_form.html', context)

######################## List Views ####################################

@login_required(login_url='login')
def dashboard(request):
    projects = Project.objects.all()
    tasks = Task.objects.all()

    total_tasks = tasks.count()

    total_projects = projects.count()
    not_started = tasks.filter(status='Not Started').count()
    in_progress = tasks.filter(status='In Progress').count()
    completed = tasks.filter(status='Completed').count()

    context = {'projects':projects,'tasks': tasks, 'total_projects':total_projects,
    'total_tasks': total_tasks, 'not_started': not_started, 'in_progress': in_progress, 'completed': completed}

    return render(request, 'projects/dashboard.html', context)

@login_required(login_url='login')
def tasks(request):
    tasks = Task.objects.all()
    return render(request, 'projects/tasks.html', {'tasks': tasks})

################## Detail or Read Views ##########################

@login_required(login_url='login')
def project(request, pk):
    project = Project.objects.get(id=pk)
    tasks = project.task_set.all()

    task_count = tasks.count()
    context = {'project': project, 'tasks': tasks, 'task_count': task_count}
    return render(request, 'projects/project.html', context)

@login_required(login_url='login')
def projectDetail(request):
    return render(request, 'projects/project_detail.html')


######################## Update Views ##################################

@login_required(login_url='login')
def updateTask(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/dashboard/')

    context = {'form': form, 'task': task}
    return render(request, 'projects/task_form.html', context)


############################# Delete Views ###########################

@login_required(login_url='login')
def deleteTask(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == "POST":
        task.delete()
        return redirect('/dashboard/')


    context = {'item': task}
    return render(request, 'projects/delete.html', context)
