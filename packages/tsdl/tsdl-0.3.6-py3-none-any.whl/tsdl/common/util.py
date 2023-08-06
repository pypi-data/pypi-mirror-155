import sys
import os
import re

from pathlib import Path


def to_dict(**kwargs):
    """
    转化为dict类型数据
    :param kwargs:
    :return:
    """
    return kwargs


def to_list(*args):
    """
    转化为list类型数据
    :param args:
    :return:
    """
    return args


def extract_digit(s: str):
    """
    提取字符串中所有数字
    :param s:
    :return:
    """
    return "".join(list(filter(str.isdigit, s)))


def is_valid_url(url: str):
    """
    验证url有效性
    :param url:
    :return:
    """
    regex = r'http[s]?://(?:[a-zA-Z][0-9]|[$-@.&+]|[!*\(\),]|(?:%[0-9a-zA-F]))+'

    p = re.compile(regex)

    if url is None:
        return False

    if re.search(p, url):
        return True

    return False


def replace(content: dict, **kwargs):
    """
    替换字典中变量
    :param content:
    :return:
    """
    ds = str(content)

    for key, value in kwargs.items():
        if type(value) is str:
            ds = ds.replace('#{}'.format(key.upper()), value)
            ds = ds.replace('*{}'.format(key.upper()), value)
        else:
            ds = ds.replace('\'#{}\''.format(key.upper()), str(value))
            ds = ds.replace('\'*{}\''.format(key.upper()), str(value))

    return eval(ds)


class PathUtil(object):
    """
    路径处理工具类
    """

    def __init__(self):
        # 判断调试模式
        debug_vars = dict((a, b) for a, b in os.environ.items() if a.find('IPYTHONENABLE') >= 0)
        # 根据不同场景获取根目录
        if len(debug_vars) > 0:
            """当前为debug运行时"""
            self.root_path = sys.path[2]
        elif getattr(sys, 'frozen', False):
            """当前为exe运行时"""
            self.root_path = os.getcwd()
        else:
            """正常执行"""
            self.root_path = sys.path[1]
        # 替换斜杠
        self.root_path = self.root_path.replace("\\", "/")

    def getPathFromResources(self, file_name):
        """
        按照文件名拼接资源文件路径
        :param file_name:
        :return:
        """
        file_path = "%s/resources/%s" % (self.root_path, file_name)
        return file_path

    def exist(self, *args):
        file_path = os.path.join(self.root_path, *args)
        if os.path.exists(file_path):
            return True
        else:
            return False

    def makeDir(self, *args):
        dir_path = os.path.join(self.root_path, *args)
        if not os.path.exists(dir_path):
            Path(dir_path).mkdir(parents=True, exist_ok=True)

        return dir_path


pathUtil = PathUtil()


