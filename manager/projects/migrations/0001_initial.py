# Generated by Django 3.1.1 on 2020-10-14 09:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('expenses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BaselineIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('level', models.CharField(choices=[('Goal', 'Goal'), ('Objective', 'Objective'), ('Outcome', 'Outcome'), ('Output', 'Output'), ('Input', 'Input')], default='Output', max_length=100)),
                ('category', models.CharField(choices=[('Quantitative', 'Quantitative'), ('Qualitative', 'Qualitative'), ('Mixed', 'Mixed')], max_length=20)),
                ('baseline_value', models.FloatField(default=0.0)),
                ('baseline_date', models.DateField()),
                ('target_value', models.FloatField(default=0.0)),
                ('target_date', models.DateField()),
                ('baseline_comment', models.CharField(choices=[('0', 'Disaster'), ('1', 'Very Poor'), ('2', 'Poor'), ('3', 'Very Bad'), ('4', 'Bad'), ('5', 'Not Bad'), ('6', 'Okay'), ('7', 'Good'), ('8', 'Very Good'), ('9', 'Excellent'), ('10', 'Perfect')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Objective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, default=None, max_length=600, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('amount_allocated', models.DecimalField(decimal_places=2, default=0.0, max_digits=20)),
                ('status', models.CharField(choices=[('Pending Approval', 'Pending Approval'), ('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Finished', 'Finished')], default='Not Started', max_length=200)),
                ('charter', models.FileField(blank=True, null=True, upload_to='')),
                ('budget', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expenses.budget')),
                ('goal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.goal')),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=500)),
                ('start_date', models.DateField()),
                ('duration', models.IntegerField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Not Started', 'Not Started'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Not Started', max_length=30)),
                ('assigned_to', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('objective', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.objective')),
                ('project', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='ProgressReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Quarterly', 'Quarterly'), ('Midterm', 'Midterm'), ('Yearly', 'End of Year')], default='Weeky', max_length=30)),
                ('description', models.CharField(max_length=255)),
                ('narrative', models.TextField()),
                ('recommendations', models.TextField()),
                ('date_compiled', models.DateField(default=django.utils.timezone.now)),
                ('compiled_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('tasks', models.ManyToManyField(default=None, to='projects.Task')),
            ],
        ),
        migrations.CreateModel(
            name='ProgressIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_value', models.FloatField(default=0.0)),
                ('current_date', models.DateTimeField(auto_now_add=True)),
                ('comment', models.CharField(choices=[('0', 'Disaster'), ('1', 'Very Poor'), ('2', 'Poor'), ('3', 'Very Bad'), ('4', 'Bad'), ('5', 'Not Bad'), ('6', 'Okay'), ('7', 'Good'), ('8', 'Very Good'), ('9', 'Excellent'), ('10', 'Perfect')], default='Okay', max_length=20)),
                ('indicator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.baselineindicator')),
                ('objective', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projects.objective')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.task')),
            ],
        ),
        migrations.AddField(
            model_name='objective',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
        migrations.AddField(
            model_name='baselineindicator',
            name='objective',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projects.objective'),
        ),
        migrations.AddField(
            model_name='baselineindicator',
            name='project',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='projects.project'),
        ),
    ]
