LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'default_handler': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default_formatter'
        }
    },

    'loggers': {
        'vk_parsing': {
            'handlers': ['default_handler'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}

SILENT_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'handlers': {
        'default_handler': {
            'class': 'logging.NullHandler',
            'level': 'DEBUG',
        }
    },

    'loggers': {
        'vk_parsing': {
            'handlers': ['default_handler'],
            'level': 'DEBUG',
            'propagate': False
        }
    }
}
