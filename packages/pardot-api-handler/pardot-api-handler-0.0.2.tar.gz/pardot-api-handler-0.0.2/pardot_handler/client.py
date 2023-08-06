from .errors import PardotAPIError
from .objects import load_objects
from .parameters import auth_url
from .parameters import base_url

import requests


class PardotAPI(object):
    def __init__(self,
                 grant_type,
                 client_id,
                 client_secret,
                 username,
                 password,
                 business_unit_id,
                 access_token=None,
                 version=5):
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.access_token = access_token
        self.business_unit_id = business_unit_id
        self.version = version
        self._load_objects()

    def _load_objects(self):
        load_objects(self)

    def authenticate(self, url):
        path = '{}{}'.format(url, auth_url)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        body = {
            'grant_type': self.grant_type,
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'username': self.username,
            'password': self.password
        }
        try:
            request = requests.post(path, headers=headers, params=body)
        except requests.exceptions.ConnectionError:
            return None
        try:
            self._check_response(request)
            self.access_token = request.json().get('access_token')
            return request
        except PardotAPIError:
            return None

    def build_header(self):
        header = {
            'Content-type': 'application/json',
            'Authorization': 'Bearer {}'.format(self.access_token),
            'Pardot-Business-Unit-Id': self.business_unit_id
        }
        return header

    def post(self, object_name, path=None, params=None, json=None):
        if params is None:
            params = {}
        request = requests.post(self._full_path(object_name,
                                                self.version,
                                                path),
                                headers=self.build_header(),
                                params=params,
                                json=json)
        try:
            self._check_response(request)
            return request
        except PardotAPIError:
            return None

    @staticmethod
    def _check_response(response):
        if response.headers.get('content-type') == 'application/json':
            json = response.json()
            error = json.get('err')
            if error:
                return PardotAPIError(json_response=json)
            return json
        else:
            return response.status_code

    @staticmethod
    def _full_path(object_name, version, path=None):
        full = '{0}/api/v{1}/objects/{2}'.format(base_url,
                                                         version,
                                                         object_name)
        if path:
            return full + '{0}'.format(path)
        return full


