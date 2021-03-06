# coding:utf-8
from core.resource_pool import init_resources_pool
from logging.config import dictConfig
import os

# 初始化管理员账号
USERNAME = "admin"
PASSWORD = "admin"

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文件存储信息相关配置
DB_Users = os.path.join(BASE_DIR, "db", "Users")
DB_Flows_History = os.path.join(BASE_DIR, "db", "Flows_History")
if not os.path.exists(DB_Users):
    os.mkdir(DB_Users)
if not os.path.exists(DB_Flows_History):
    os.mkdir(DB_Flows_History)

# 存放学校、班级等相关的资源的pkl文件目录
ResourcePoolDir = os.path.join(BASE_DIR, "db", "ResourcePool")
if not os.path.exists(ResourcePoolDir):
    os.mkdir(ResourcePoolDir)

# 初始化系统中的教学资源池,用于保存学校、班级、课程、学员、讲师等资源对象信息
RP = init_resources_pool(ResourcePoolDir)

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
        'base_view': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'base_view.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'manager_view': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'manager_view.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'student_view': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'student_view.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'teacher_view': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'teacher_view.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'db.log'),
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
        'main': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'main.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },

    },
    'loggers': {
        'system': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'system.base_view': {
            'handlers': ['base_view'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'system.manager_view': {
            'handlers': ['manager_view'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'system.student_view': {
            'handlers': ['student_view'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'system.teacher_view': {
            'handlers': ['teacher_view'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'system.auth': {
            'handlers': ['auth'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'system.db': {
            'handlers': ['db'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'system.main': {
            'handlers': ['main'],
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
