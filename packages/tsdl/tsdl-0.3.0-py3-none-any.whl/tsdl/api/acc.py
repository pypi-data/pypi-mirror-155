from tsdl.api import req, url
from tsdl.config.config import CONFIG
from tsdl.common.util import to_dict


def accept(name: str, data):
    return req.post(url.get(CONFIG.get('API', 'acc')), params=to_dict(key=name), jsons=data)
