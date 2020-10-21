from django.forms import ModelForm
from .models import Goal, Project, Activity, Task, BaselineIndicator, ProgressIndicator, ProgressReport


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = '__all__'

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = '__all__'

class ProgressReportForm(ModelForm):
    class Meta:
        model = ProgressReport
        fields = '__all__'

class ProgressIndicatorForm(ModelForm):
    class Meta:
        model = ProgressIndicator
        fields = '__all__'

class ActivityForm(ModelForm):
    class Meta: 
        model = Activity
        fields = '__all__'


