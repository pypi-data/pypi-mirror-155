import requests
import json

from tsdl.common.util import to_dict

_timeout_ = 60
_method_ = 'get'


def get(url, params: dict = None):
    try:
        res = requests.get(url=url, params=params, timeout=_timeout_)
        try:
            return json.loads(res.text)
        except Exception as e:
            return res.text
    except Exception as e:
        raise e


def post(url, params: dict = None, jsons: dict = None):
    try:
        res = requests.post(url=url, params=params, json=jsons, timeout=_timeout_)
        try:
            return json.loads(res.text)
        except Exception as e:
            return res.text
    except Exception as e:
        raise e


def put(url, params: dict = None):
    try:
        res = requests.put(url=url, params=params, timeout=_timeout_)
        try:
            return json.loads(res.text)
        except Exception as e:
            return res.text
    except Exception as e:
        raise e


def delete(url, params: dict = None):
    try:
        res = requests.delete(url=url, params=params, timeout=_timeout_)
        try:
            return json.loads(res.text)
        except Exception as e:
            return res.text
    except Exception as e:
        raise e


if __name__ == '__main__':
    # 添加服务及其对应的参数
    # post('http://10.157.1.248:8000/api', params=to_dict(key='pro:manual'),
    #      jsons=to_dict(url='http://10.157.1.248:9020/pro/manual'))
    # post('http://10.157.1.248:8000/api', params=to_dict(key='pro:encode'),
    #      jsons=to_dict(url='http://10.157.1.248:9020/pro/encode'))
    # post('http://10.157.1.248:8000/api', params=to_dict(key='pro:decode'),
    #      jsons=to_dict(url='http://10.157.1.248:9020/pro/decode'))
    # post('http://10.157.1.248:8000/api', params=to_dict(key='gw698:manual'),
    #      jsons=to_dict(url='http://10.157.1.248:8021/pro/gw698/manual'))
    # post('http://10.157.1.248:8000/api', params=to_dict(key='gw698:encode'),
    #      jsons=to_dict(url='http://10.157.1.248:8021/pro/gw698/encode'))
    # post('http://10.157.1.248:8000/api', params=to_dict(key='gw698:decode'),
    #      jsons=to_dict(url='http://10.157.1.248:8021/pro/gw698/decode'))
    #
    # post('http://10.157.1.248:8000/api', params=to_dict(key='mm:dict'),
    #      jsons=to_dict(url='http://10.157.1.248:8000/mm/dict'))
    #
    # post('http://10.157.1.248:8000/api', params=to_dict(key='acc:accept'),
    #      jsons=to_dict(url='http://10.157.1.248:9030/acc/accept'))

    # 获取验证
    data = get('http://10.157.1.248:8000/api', params=to_dict(key='mm:dict'))
    print(type(data))
    print(data)

    parse = {
        'meta': {'name': 'GW698', 'version': '1.0.0'},
        'parse': {
            'control': {'direction': 'C2S', 'starter': 'CLIENT', 'frames ': 'NO', 'function': 'DATA'},
            'address': {'server': {'type': 'COMMON', 'logic': 0, 'value': '000000000001'}, 'client': 'A1'},
            'link_data': {
                'command': {'name': 'GET', 'sub': 'NORMAL'},
                'oad': {'name': '表号.数值', 'index': 0}
            }
        },
        'cache': 'zhangyue010:cache#pos_1'
    }

    data = post('http://127.0.0.1:9020/pro/encode', jsons=parse)
