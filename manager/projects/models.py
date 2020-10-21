from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from expenses.models import Budget
from django.urls import reverse


class Goal(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Project(models.Model):
    STATUS = (
            ('Pending Approval', 'Pending Approval'),
            ('Not Started', 'Not Started'),
            ('In Progress', 'In Progress'),
            ('Finished', 'Finished'),
            )

    title = models.CharField(max_length=255)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount_allocated = models.DecimalField(max_digits=20, decimal_places=2, default=0.0)
    status = models.CharField(max_length=200, choices=STATUS, default='Not Started')
    charter = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.title


class Objective(models.Model):
    name = models.CharField(max_length=300)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    description = models.TextField(max_length=600, default=None, null=True, blank=True)

    def __str__(self):
        return self.name

class Activity(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    activity = models.CharField(max_length=150, default=None)
    description = models.TextField(max_length=500, default=None, null=True, blank=True)


class Task(models.Model):

    STATUS = (
            ('Not Started', 'Not Started'),
            ('In Progress', 'In Progress'),
            ('Completed', 'Completed'),
            )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, default=None, null=True, blank=True)
    title = models.CharField(max_length=255)
    location = models.CharField(max_length=150, default=None, null=True, blank=True)
    description = models.TextField(max_length=500)
    start_date = models.DateField(default=timezone.now)
    duration = models.IntegerField()
    end_date = models.DateField(default=timezone.now, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS, default='Not Started')

    def __str__(self):
        return self.title


class BaselineIndicator(models.Model):
    TYPE = (
            ('Quantitative', 'Quantitative'),
            ('Qualitative', 'Qualitative'),
            ('Mixed', 'Mixed'),
            )
    LEVEL = (
            ('Goal', 'Goal'),
            ('Objective', 'Objective'),
            ('Outcome', 'Outcome'),
            ('Output', 'Output'),
            ('Input', 'Input'),
    )
    COMMENT = (
            ('0', 'Disaster'),
            ('1', 'Very Poor'),
            ('2', 'Poor'),
            ('3', 'Very Bad'),
            ('4', 'Bad'),
            ('5', 'Not Bad'),
            ('6', 'Okay'),
            ('7', 'Good'),
            ('8', 'Very Good'),
            ('9', 'Excellent'),
            ('10', 'Perfect')
        )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    level = models.CharField(max_length=100, choices=LEVEL, default='Output')
    category = models.CharField(max_length=20, choices=TYPE)
    baseline_value = models.FloatField(default=0.0)
    baseline_date = models.DateField()
    target_value = models.FloatField(default=0.0)
    target_date = models.DateField()
    baseline_comment = models.CharField(max_length=50, choices=COMMENT)

    def __str__(self):
        return self.name


class ProgressIndicator(models.Model):
    COMMENT = (
            ('0', 'Disaster'),
            ('1', 'Very Poor'),
            ('2', 'Poor'),
            ('3', 'Very Bad'),
            ('4', 'Bad'),
            ('5', 'Not Bad'),
            ('6', 'Okay'),
            ('7', 'Good'),
            ('8', 'Very Good'),
            ('9', 'Excellent'),
            ('10', 'Perfect')
            )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    objective = models.ForeignKey(Objective, on_delete=models.CASCADE, default=None)
    indicator = models.ForeignKey(BaselineIndicator, on_delete=models.CASCADE)
    current_value = models.FloatField(default=0.0)
    date_recorded = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    official = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    comment = models.CharField(max_length=20, choices=COMMENT, default='Okay')

    def get_absolute_url(self):
        return reverse("monitoringDashboard", kwargs={"id": self.id})

    def __str__(self):
        return str(self.id)


class ProgressReport(models.Model):
    CATEGORY = (
            ('Weekly', 'Weekly'),
            ('Monthly', 'Monthly'),
            ('Quarterly', 'Quarterly'),
            ('Midterm', 'Midterm'),
            ('Yearly', 'End of Year'),
    )

    category = models.CharField(max_length=30, choices=CATEGORY, default='Weeky')
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    tasks = models.ManyToManyField(Task, default=None)
    description = models.CharField(max_length=255)
    narrative = models.TextField()
    recommendations = models.TextField()
    compiled_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date_compiled = models.DateField(default=timezone.now)

    def __str__(self):
        return self.description
