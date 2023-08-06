from .prospects import Prospects


def load_objects(client):
    client.prospects = Prospects(client)
