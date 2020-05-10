import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium.common.exceptions import ErrorInResponseException, WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

from covidapi.commons.utils import safe_int
from covidapi.extensions import db
from covidapi.models.covid import CovidItem

SITE_URL = 'https://www.pravda.com.ua/cdn/covid-19/cpa/'


class CovidParser():
    def __init__(self):
        self.covid_dict = {
            'total': {},
            'per_day': {}
        }

        opts = Options()
        opts.add_argument("--headless")
        try:
            self.browser = Firefox(options=opts)
        except WebDriverException:
            print('Error when initializing web browser driver.')

    def run(self):
        try:
            self.browser.get(SITE_URL)
        except ErrorInResponseException:
            print('Error on the server side.')

        time.sleep(1)

        soup = BeautifulSoup(self.browser.page_source, 'html.parser')

        total_containers = soup.find_all('div', class_='world-item-num')
        if total_containers:
            self.covid_dict['total'] = {
                'confirmed': safe_int(total_containers[0].find('span').text),
                'active': safe_int(total_containers[1].find('span').text),
                'recovered': safe_int(total_containers[2].find('span').text),
                'deaths': safe_int(total_containers[3].find('span').text)
            }

        daily_containers = soup.find_all('div', class_='world-item-change')
        if daily_containers:
            self.covid_dict['per_day'] = {
                'confirmed': safe_int(daily_containers[0].find('span').text),
                'active': safe_int(daily_containers[1].find('span').text),
                'recovered': safe_int(daily_containers[2].find('span').text),
                'deaths': safe_int(daily_containers[3].find('span').text)
            }

        general_containers = soup.find_all('div', class_='block__title block__title_extrasmall')
        if general_containers:
            info_text = general_containers[1].find('span').text
            updated_at_str = ' '.join(info_text.split(' ')[-2:])
            self.covid_dict['updated_at'] = datetime.strptime(updated_at_str, '%d.%m.%Y %H:%M')

        self._save_db()

    def _save_db(self):
        existing_item = (
            CovidItem.query
            .filter(CovidItem.updated_at == self.covid_dict['updated_at'])
            .first()
        )
        if existing_item:
            return

        try:
            new_item = CovidItem(
                confirmed=self.covid_dict['per_day']['confirmed'],
                active=self.covid_dict['per_day']['active'],
                recovered=self.covid_dict['per_day']['recovered'],
                deaths=self.covid_dict['per_day']['deaths'],
                total_confirmed=self.covid_dict['total']['confirmed'],
                total_active=self.covid_dict['total']['active'],
                total_recovered=self.covid_dict['total']['recovered'],
                total_deaths=self.covid_dict['total']['deaths'],
                updated_at=self.covid_dict['updated_at'],
            )
            db.session.add(new_item)
            db.session.commit()
        except KeyError:
            print('Error when get data from dict with parsed data.')