from tsdl.api import req
from tsdl.config.config import CONFIG
from tsdl.common.util import to_dict


def get(name: str):
    result = req.get(CONFIG.get('API', 'url'), params=to_dict(key=name))

    if result is None or result == 'NULL':
        raise Exception("Can't find {} in API service.".format(name))

    return result.get('url')
