from django.contrib import admin
from .models import Project, Activity, Task, BaselineIndicator, ProgressReport, ProgressIndicator, Objective, Goal

admin.site.register(Goal)
admin.site.register(Project)
admin.site.register(Objective)
admin.site.register(Activity)
admin.site.register(Task)
admin.site.register(BaselineIndicator)
admin.site.register(ProgressIndicator)
admin.site.register(ProgressReport)
