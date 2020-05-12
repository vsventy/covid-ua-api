from celery import task

from covidapi.commons.parsing import CovidParser
from covidapi.extensions import celery


@celery.task
def run_covid_parser():
    parser = CovidParser()
    parser.run()
