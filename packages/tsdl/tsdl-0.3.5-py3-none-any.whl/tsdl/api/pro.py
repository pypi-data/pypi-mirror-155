from tsdl.api import req, url
from tsdl.config.config import CONFIG
from tsdl.common.util import to_dict


def manual(protocol: str, operation: str, mode: str = None, security: str = None):
    return req.get(url.get(CONFIG.get('API', 'pro') + ':manual'),
                   params=to_dict(protocol=protocol, operation=operation, mode=mode, security=security))


def encode(parse: dict, cache: str = None):
    parse.update(to_dict(cache=cache))
    return req.post(url.get(CONFIG.get('API', 'pro') + ':encode'), jsons=parse)


def decode(frame: str, session: dict = None, part_frame: str = None, cache: str = None):
    return req.post(url.get(CONFIG.get('API', 'pro') + ':decode'),
                    jsons=to_dict(frame=frame, session=session, part_frame=part_frame, cache=cache))
