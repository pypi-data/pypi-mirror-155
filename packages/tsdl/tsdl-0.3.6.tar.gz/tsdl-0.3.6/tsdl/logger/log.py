import logging

from logging.handlers import RotatingFileHandler
from tsdl.common.util import pathUtil

logger = logging.getLogger()
logger.setLevel(logging.INFO)  # Log等级总开关

log_colors_config = {
    # 终端输出日志颜色配置
    'DEBUG': 'white',
    'INFO': 'cyan',
    'WARNING': 'yellow',
    'ERROR': 'red',
    'CRITICAL': 'bold_red',
}

# 第二步，创建一个handler，用于写入日志文件
logPath = pathUtil.makeDir('log')
logfile = "%s/%s" % (logPath, 'case.log')
fh = RotatingFileHandler(filename=logfile, mode='a', maxBytes=5*1024*1024, backupCount=10, encoding='utf-8')
# fh = logging.FileHandler(logfile, mode='a')  # open的打开模式这里可以进行参考
fh.setLevel(logging.DEBUG)  # 输出到file的log等级的开关

# 第三步，再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)  # 输出到console的log等级的开关

# 第四步，定义handler的输出格式
# formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
formatter = logging.Formatter("[%(asctime)s] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 第五步，将logger添加到handler里面
logger.addHandler(fh)
logger.addHandler(ch)

