from covidapi.commons.parsing import CovidParser
from covidapi.extensions import celery


@celery.task
def run_covid_parser():
    print('Task <CovidParser> is started..')
    parser = CovidParser()
    parser.run()
    print('Task <CovidParser> is finished.')
