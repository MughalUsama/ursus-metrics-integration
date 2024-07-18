# JobDiva to 15Five Metrics Uploader

## Project Overview

This project contains APIs to upload metrics from JobDiva to 15Five using Celery for task scheduling and execution. The tasks are managed and executed using Docker containers to ensure consistency across different environments. The project includes components for handling 15Five and JobDiva related code.

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Setup

1. **Clone the repository:**

   ```sh
   git clone https://your-repo-url.git
   cd project_root
   ```

2. **Create and configure the `.env` file:**

   Create a `.env` file in the project root with the following variables:

   ```
   JOBDIVA_CLIENTID="1747"
   JOBDIVA_USERNAME="email_here"
   JOBDIVA_PASSWORD="password_here"

   _15FIVE_API_KEY="api_key_here"
   ```

### Building and Running with Docker Compose

3. **Build the Docker images:**

   ```sh
   docker-compose build
   ```

4. **Start the services:**

   ```sh
   docker-compose up
   ```

   This command will start the following services:
   - **Redis**: Message broker for Celery.
   - **Celery Worker**: Executes the tasks defined in the project.
   - **Celery Beat**: Scheduler for periodic tasks.

### Stopping the Services

5. **Stop the services:**

   ```sh
   docker-compose down
   ```

### Rebuilding the Docker Images

If you make changes to the Dockerfile or dependencies, you may need to rebuild the images:

```sh
docker-compose build
```

### Troubleshooting

Check the logs of the services for any issues:

```sh
docker-compose logs
```

For detailed logs, you can adjust the log level in `Dockerfile`:

```sh
CMD ["celery", "-A", "celery_app", "worker", "--loglevel=DEBUG"]
```


1. **Define your tasks in the `tasks` module:**

   Create task definitions in the `tasks` module. For example, you can define tasks in `tasks/t1.py` and `tasks/t2.py`:

   ```python
   # tasks/t1.py
    class SomeTask(Task):
        def run(self):
           print("Task One executed")
   
    some_task = app.register_task(SomeTask())

   ```

2. **Import the task in task/__init__.py**

   ```python
    from .new_job_records_task import create_new_job_records_task
    
    __all__ = ["create_new_job_records_task"]
   ```


3. **Update the beat schedule if needed:**

   If you want the tasks to run periodically, update the `beat_schedule` configuration in `celery_app.py`.

   ```python
   app.conf.beat_schedule = {
       "task-one-every-2-minutes": {
           "task": "tasks.t1.task_one",
           "schedule": crontab(minute="*/2"),  # Run every 2 minutes
       },
       "task-two-every-monday-midnight": {
           "task": "tasks.t2.task_two",
           "schedule": crontab(minute=0, hour=0, day_of_week='monday'),  # Run every Monday at midnight
       }
   }
   ```
    Note: Change crontab to crontab(minute="*/2") and rebuild docker to test immediately.

