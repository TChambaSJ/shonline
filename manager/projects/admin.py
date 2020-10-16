from django.contrib import admin
from .models import Project, Task, BaselineIndicator, ProgressReport, ProgressIndicator, Objective, Goal

# Register your models here.

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(BaselineIndicator)
admin.site.register(ProgressReport)
admin.site.register(ProgressIndicator)
admin.site.register(Goal)
admin.site.register(Objective)
