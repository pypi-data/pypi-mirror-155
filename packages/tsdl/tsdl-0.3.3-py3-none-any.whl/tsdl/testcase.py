from tsdl.logger.log import logger
from tsdl.core import interpret
from tsdl.core.context import Context


def run(script_path: str, app_url: str, *loops, **meters):
    """
    运行测试脚本
    :param script_path: 脚本代码文件存放包路径和脚本文件名[例如: script.test]
    :param app_url: app访问url
    :param loops: 循环定义
    :param meters 测试电表
    :return:
    """
    logger.info('TEST CASE START...')
    logger.info('~ init parameter -script "{}" -app_url "{}" -loops "{}" -meters "{}"'.
                format(script_path, app_url, loops, meters))
    interpret.handle(Context(script_path, app_url, *loops, **meters))
    logger.info('TEST CASE END.')



