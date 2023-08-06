import time

import requests

from tsdl.core.context import Context
from tsdl.api import app, acc, em, pro
from tsdl.logger.log import logger

"""
    常用操作命令
"""


def send(context: Context, data: dict, retry_times: int = 3):
    """
    发送操作命令 - 向测试端app
    :param context:         上下文
    :param data:            发送数据
    :param retry_times:     失败重试次数（默认：3次）
    :return:
    """
    result = None

    try:
        data['step_id'] = int("".join(list(filter(str.isdigit, context.runtime.step))))
        logger.info('~ @SEND-> client:{} data:{}'.format(context.url, data))
        result = app.send(context.url, data)
        logger.info('~ @SEND<- result:{}'.format(result))
    except requests.exceptions.MissingSchema as me:
        logger.error(str(me))
        raise AssertionError(str(me))
    except Exception as ce:
        logger.error(str(ce))
        sleep(context, 5)
        retry_times -= 1
        if retry_times <= 0:
            raise AssertionError(str(ce))
        else:
            send(context, data, retry_times)

    return result


def sleep(context: Context, seconds: int):
    """
    休眠
    :param context:     上下文
    :param seconds:     秒
    :return:
    """
    logger.info('~ @SLEEP {}secs'.format(seconds))
    time.sleep(seconds)


def encode(context: Context, parse: dict, cache: str = None):
    """
    协议组帧
    :param context:     上下文
    :param parse:       组帧数据
    :param cache:       缓存
    :return:
    """
    logger.info('~ @ENCODE-> parse:{} cache:{}'.format(parse, cache))
    frame = pro.encode(parse, cache)
    logger.info('~ @ENCODE<- frame:{}'.format(frame))

    return frame


def decode(context: Context, frame: str, session: dict = None, part_frame: str = None, cache: str = None):
    """
    协议解帧
    :param context:     上下文
    :param frame:       数据帧
    :param session:     会话 - 加解密信息
    :param part_frame:  分帧 - 部分帧
    :param cache:       缓存
    :return:
    """
    logger.info('~ @DECODE-> frame:{} session:{} part frame:{} cache:{}'.format(frame, session, part_frame, cache))
    parse = pro.decode(frame, session, part_frame, cache)
    logger.info('~ @DECODE<- parse:{}'.format(parse))

    return parse
    # __framing_handle(context, parse)


def compare(context: Context, name: str, data: dict):
    """
    比对、计算和验证数据
    :param context:     上下文
    :param name:        比对关键字
    :param data:        比对数据
    :return:
    """
    logger.info('~ @COMPARE-> name:{} data:{}'.format(name, data))
    result = acc.accept(name, data)
    logger.info('~ @COMPARE<- result:{}'.format(result))
    return result


def execute(context: Context, **args):
    """
    执行语句
    语句类型:
        1. 赋值
        2. 判断或处理逻辑等
    :param context:     上下文
    :param args:        执行语句
    :return:
    """
    for expr in args:
        exec(expr)


def api(context: Context, service_key: str, **kwargs):
    """
    调用用户自定义服务api
    :param context:
    :param service_key:
    :param kwargs:
    :return:
    """
    pass


"""
    结果判断命令
"""


def diagnose(context: Context, expression: str, *args, **kwargs):
    """
    断言 - 失败，程序会停止运行
    :param context:         上下文
    :param expression:      表达式
    :param args:            表达式中的参数
    :param kwargs:          返回信息
    :return:
    """
    if len(args) > 0:
        expression = expression.format(*args)
    if eval(expression):
        logger.info('~ @DIAGNOSE expression:{} result:{}'.format(expression, True))
        send(context, {'todo': {'app:show': {
            'msg': 'DIAGNOSE Condition[{}], execute success.'.format(expression) if kwargs.get(
                'success') is None else kwargs.get('success')}}})
    else:
        logger.info('~ @DIAGNOSE expression:{} result:{}'.format(expression, False))
        send(context, {'todo': {'app:show': {
            'msg': 'DIAGNOSE Condition[{}], execute fail.'.format(expression) if kwargs.get(
                'fail') is None else kwargs.get('fail')}}})
        raise AssertionError(kwargs.get('fail'))


def presume(context: Context, expression: str, *args, **kwargs):
    """
    假定 - 失败，程序不会停止运行
    :param context:         上下文
    :param expression:      表达式
    :param args:            表达式中的参数
    :param kwargs:          返回信息
    :return:
    """
    if len(args) > 0:
        expression = expression.format(*args)
    if eval(expression):
        logger.info('~ @PRESUME expression:{} result:{}'.format(expression, True))
        send(context, {'todo': {'app:show': {
            'msg': 'PRESUME Condition[{}], execute success.'.format(expression) if kwargs.get(
                'success') is None else kwargs.get('success')}}})
    else:
        logger.info('~ @PRESUME expression:{} result:{}'.format(expression, False))
        send(context, {'todo': {'app:show': {
            'msg': 'PRESUME Condition[{}], execute fail.'.format(expression) if kwargs.get(
                'fail') is None else kwargs.get('fail')}}})


"""
    调用加密机命令
"""


def negotiate(context: Context, meter_esam_sn: str, meter_esam_counter: int):
    """
    协商
    :param context:                 上下文
    :param meter_esam_sn:           电表ESAM序列号
    :param meter_esam_counter:      电表ESAM计数器
    :return:
    """
    logger.info('~ @NEGOTIATE-> esam_sn:{} esam_counter:{}'.format(meter_esam_sn, meter_esam_counter))
    result = em.negotiate(meter_esam_sn, meter_esam_counter)
    logger.info('~ @NEGOTIATE<- result:{}'.format(result))

    return result


def verify(context: Context, em_rn: str, meter_esam_sn: str, meter_esam_rn: str, meter_esam_mac: str):
    """
    验证
    :param context:                 上下文
    :param em_rn:                   加密机随机数
    :param meter_esam_sn:           电表ESAM序列号
    :param meter_esam_rn:           电表ESAM随机数
    :param meter_esam_mac:          电表ESAM MAC
    :return:
    """
    logger.info('~ @VERIFY-> em_rn:{} esam_sn:{} esam_rn:{} esam_mac:{}'.format(em_rn, meter_esam_sn, meter_esam_rn,
                                                                                 meter_esam_mac))
    result = em.verify_session(em_rn, meter_esam_sn, meter_esam_rn, meter_esam_mac)
    logger.info('~ @VERIFY<- result:{}'.format(result))

    return result
