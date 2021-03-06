# coding:utf-8
from logging.config import dictConfig
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文件目录，存储用户信息相关配置
DB_Users = os.path.join(BASE_DIR, "db", "Users")
if not os.path.exists(DB_Users):
    os.mkdir(DB_Users)

# 用户FTP文件仓库
DB_Storage = os.path.join(BASE_DIR, "db", "Storage")
if not os.path.exists(DB_Storage):
    os.mkdir(DB_Storage)

# 用于暂时存放上传文件的临时文件
DB_Temp = os.path.join(BASE_DIR, "db", "Temp")
if not os.path.exists(DB_Temp):
    os.mkdir(DB_Temp)

# 标示字符串，用于发送文件与接收文件数据时的结束标示
Label_Byte_String = b"---send file data has finished---"

# 账户登录认证状态标示
AUTH_FLAG = {"username": None, "is_authenticated": False}

# log日志相关设置
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(filename)s:%(lineno)d(%(module)s:%(funcName)s) - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'logging.handlers.SysLogHandler.LOG_LOCAL7',
            'formatter': 'standard',
        },
        'user': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'user.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'auth': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'auth.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'ftp_server': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'ftp_server.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'ftp_client': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'ftp_client.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },

    },
    'loggers': {
        'ftp': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'ftp.auth': {
            'handlers': ['auth'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ftp.user': {
            'handlers': ['user'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ftp.ftp_server': {
            'handlers': ['ftp_server'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'ftp.ftp_client': {
            'handlers': ['ftp_client'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


def init_logging():
    """
    initial logging
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    dictConfig(LOGGING)
