from tsdl.api import req, url
from tsdl.config.config import CONFIG
from tsdl.common.util import to_dict


def get(name: str, key: str):
    return req.get(url.get(CONFIG.get('API', 'mm')), params=to_dict(name=name, key=key))


def put(name: str, key: str, data):
    if type(data) is dict:
        return req.post(url.get(CONFIG.get('API', 'mm')), params=to_dict(name=name, key=key), jsons=data)
    else:
        return req.post(url.get(CONFIG.get('API', 'mm')), params=to_dict(name=name, key=key, data=data))


def delete(name: str, key: str):
    return req.delete(url.get(CONFIG.get('API', 'mm')), params=to_dict(name=name, key=key))
