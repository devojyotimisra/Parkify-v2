from application.middlewares.init_celery import initialize_celery
from application.helpers.tasks import BackgroundJobs


def initialize_bg_jobs(app):
    celery = initialize_celery(app)
    bg_jobs = BackgroundJobs(celery, app)
    bg_jobs.setup_periodic_tasks()
    app.bg_jobs = bg_jobs
    app.celery = celery
