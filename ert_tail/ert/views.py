from django.shortcuts import render, redirect
from .forms import AppointmentForm, ReminderForm
from .models import Reminder, ReminderTask
from .tasks import send_reminder_email
from datetime import timedelta
from django.conf import settings
from celery import uuid
from django.utils import timezone as dj_timezone
from datetime import datetime
from pytz import timezone

time_zone = settings.TIME_ZONE


def home(request):
    # Your home view logic here
    return render(request, 'home.html', {})

def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        print("FORM", form)
        if form.is_valid():
            # Save appointment and set reminders, etc.
            appointment = form.save()

            tz = timezone('America/New_York')

            # Handle intervals here (request.POST.getlist('intervals'))
            intervals = form.cleaned_data.get('intervals', [])  # This is the MultipleChoiceField for reminders
            for interval in intervals:
                reminder = Reminder.objects.create(appointment=appointment, interval=interval)

                # calculate when the email should be sent
                delta = None
                if interval == '1_day':
                    delta = timedelta(days=1)
                elif interval == '3_days':
                    delta = timedelta(days=3)
                elif interval == '1_week':
                    delta = timedelta(weeks=1)

                # Convert date and time to a single datetime object
                appointment_datetime = tz.localize(datetime.combine(appointment.date, appointment.time))
                
                send_at = appointment_datetime - delta

                print(f"Scheduled send time: {send_at}")

                # Schedule email task
                task_id = uuid()
                subject = "Your appointment reminder"
                message = f"""Dear {appointment.name},
                You have an appointment scheduled on {appointment.date} at {appointment.time}.
                Additional Info:
                {appointment.additional_info}
                """

                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [form.cleaned_data['email']]
                print(f"Generated Task ID: {task_id}")
                send_reminder_email.apply_async(
                    args=[subject, message, from_email, recipient_list], #subject, message, from_email, recipient_list
                    eta=send_at,
                    task_id=task_id
                )

                # Save task ID in databse
                ReminderTask.objects.create(reminder=reminder, task_id=task_id)
            return redirect('home')
        else: 
            return HttpResponse("Form is not valid. Please try again.")  # Basic error message for now
    else:
        form = AppointmentForm()
    return render(request, 'create_appointment.html', {'form': form})
