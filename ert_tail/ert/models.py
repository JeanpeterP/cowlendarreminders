from django.db import models

class Appointment(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    email = models.EmailField()
    additional_info = models.TextField(null=True, blank=True)

class Reminder(models.Model):
    INTERVAL_CHOICES = (
        ('1_day', '1 day'),
        ('3_days', '3 days'),
        ('1_week', '1 week'),
    )
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    interval = models.CharField(max_length=10, choices=INTERVAL_CHOICES)

class ReminderTask(models.Model):
    reminder = models.ForeignKey(Reminder, on_delete=models.CASCADE)
    task_id = models.CharField(max_length=255)