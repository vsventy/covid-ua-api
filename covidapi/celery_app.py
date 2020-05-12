from celery.schedules import crontab

from covidapi.app import init_celery
from covidapi.tasks.covid_parser import run_covid_parser

app = init_celery()
app.conf.imports = app.conf.imports + ("covidapi.tasks.covid_parser",)


@app.on_after_configure.connect()
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_tasks(
        crontab(hour=7, minute=0),
        run_covid_parser,
        name='run covid parser at 07:00 (UTC) everyday'
    )
