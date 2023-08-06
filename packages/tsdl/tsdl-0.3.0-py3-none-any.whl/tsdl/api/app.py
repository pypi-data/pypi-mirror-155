from tsdl.api import req


def send(url: str, data: dict):
    return req.post(url, jsons=data)

