from celery import Celery
from celery.schedules import crontab

# Define Celery app
app = Celery('tasks',
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/0',
             include=['tasks'])  # Include tasks module

app.conf.update(task_always_eager=True)
app.conf.task_track_started = True


app.conf.beat_schedule = {
        "week-new-job-orders-task": {
            "task": "tasks.new_job_records_task.CreateNewJobRecords",
            # change to crontab(minute="*/2") to run every 2 minutes
            # every start of monday at 01:00 AM utc
            'schedule': crontab(hour=1, minute=0, day_of_week=1),
        },
        "week-ring-central-dials-task": {
            "task": "tasks.ring_central_dials_task.CreateRingCentralDials",
            # change to crontab(minute="*/2") to run every 2 minutes
            'schedule': crontab(hour=12, minute=0, day_of_week=1),
        },
        "week-msa-task": {
            "task": "tasks.new_msa_sent_task.CreateNewMSAsSent",
            # change to crontab(minute="*/2") to run every 2 minutes
            'schedule': crontab(hour=12, minute=0, day_of_week=1),
        },
        "week-meetings-task": {
            "task":  "tasks.client_meetings_conducted_task.CreateClientMeetingsConducted",
            # change to crontab(minute="*/2") to run every 2 minutes
            'schedule': crontab(hour=12, minute=0, day_of_week=1),
        }
    }

app.conf.timezone = "UTC"

if __name__ == '__main__':
    # Start the Celery worker if this file is executed directly
    app.start()
