class Prospects(object):

    def __init__(self, client):
        self.client = client

    def upsert_latest_by_email(self, body):
        response = self._post(
            path='/do/upsertLatestByEmail', json=body)
        return response

    def _post(self, object_name='prospects', path=None, params=None, json=None):
        response = self.client.post(object_name=object_name,
                                    path=path,
                                    params=params,
                                    json=json)
        return response
