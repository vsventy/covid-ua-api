import requests

from covidapi.models.postman import ServiceType


class PostmanAPIException(Exception):
    pass


class PostmanAPIClient():

    def __init__(self, api_token):
        self.headers = {
            'Authorization': 'Token {}'.format(api_token),
            'Content-Type': 'application/json',
        }

        self.base_url = 'https://postman.org.ua/api/v1/{}/'
        self.details_url = 'https://postman.org.ua/api/v1/details/{}/'

    def _get_notify_url(self, service_type):
        try:
            service_name = ['email', 'sms', 'telegram', 'viber'][service_type]
            url = self.base_url.format(service_name)
        except IndexError:
            raise PostmanAPIException('Unknown type of service.')
        else:
            return url

    def _post_notify(self, service_type, payload):
        url = self._get_notify_url(service_type)
        result = requests.post(url, headers=self.headers, json=payload)
        return result.json()

    def send_message(self, recipient, text, service_type=int(ServiceType.TELEGRAM)):
        payload = {
            'recipient': recipient,
            'text': text
        }
        return self._post_notify(service_type, payload)

    def send_email(self, recipient, subject, text):
        payload = {
            'recipient': recipient,
            'subject': subject,
            'text': text
        }
        return self._post_notify(int(ServiceType.EMAIL), payload)

    def send_notify_by_template(self, recipient, template_key, service_type):
        payload = {
            'recipient': recipient,
            'template': template_key
        }
        return self._post_notify(service_type, payload)

    def get_notify_details(self, notify_id):
        url = self.details_url.format(notify_id)
        result = requests.get(url, headers=self.headers)
        return result.json()
