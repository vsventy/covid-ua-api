from celery.schedules import crontab

from covidapi.app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ("covidapi.tasks.covid_parser",)

app.conf.beat_schedule = {
    'run-parser-everyday-at-7-00': {
        'task': 'covidapi.tasks.covid_parser.run_covid_parser',
        'schedule': crontab(hour=7, minute=0),
    },
}
app.conf.timezone = 'UTC'
