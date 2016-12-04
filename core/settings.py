UDP_GROUP_ADDRESS = '239.255.255.250'
UDP_GROUP_PORT = '14141'

SERVER_CONFIG = {
    1: {
        "neighbor": [2],
        "port": 9001,
        "host": "127.0.0.1"
    },
    2: {
        "neighbor": [1, 3],
        "port": 9002,
        "host": "127.0.0.1"
    },
    3: {
        "neighbor": [2, 4],
        "port": 9003,
        "host": "127.0.0.1"
    },
    4: {
        "neighbor": [3, 5, 6],
        "port": 9004,
        "host": "127.0.0.1"
    },
    5: {
        "neighbor": [4],
        "port": 9005,
        "host": "127.0.0.1"
    },
    6: {
        "neighbor": [4],
        "port": 9006,
        "host": "127.0.0.1"
    }
}

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s | %(asctime)s | %(name)s:%(funcName)s | %(process)d | %(thread)d | %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'client': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
        'server': {
            'level': 'DEBUG',
            'handlers': ['console']
        },
    }
}
