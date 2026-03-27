from pathlib import Path
from typing import Any

LOG_FORMAT = (
    '[%(asctime)s] #%(levelname)-8s %(filename)s:'
    '%(lineno)d - %(name)s - %(message)s'
)

LOG_FILE_NAME = 'app.log'
LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 2
LOG_ENCODING = 'utf-8'


def get_logging_config(
        *,
        base_dir: Path,
        log_level: str = 'DEBUG',
        log_to_file: bool = True,
        log_file_name: str = LOG_FILE_NAME,
        include_test_loggers: bool = False,
        log_backup_count: int = LOG_BACKUP_COUNT,
        log_max_bytes: int = LOG_MAX_BYTES,
) -> dict[str, Any]:

    common_handlers = ['console']

    handlers: dict[str, Any] = {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default',
            'level': log_level,
        },
    }
    if log_to_file:
        log_dir = base_dir / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)

        handlers['file'] = {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(log_dir / log_file_name),
            'maxBytes': log_max_bytes,
            'backupCount': log_backup_count,
            'encoding': LOG_ENCODING,
            'formatter': 'default',
            'level': log_level,
        }

        common_handlers.append('file')

    loggers = {
        'django': {
            'handlers': common_handlers,
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': common_handlers,
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': common_handlers,
            'level': log_level,
            'propagate': False,
        },
    }

    if include_test_loggers:
        loggers.update({
            'faker': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'factory': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        })

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': LOG_FORMAT,
            },
        },
        'handlers': handlers,
        'loggers': loggers,
        'root': {
            'handlers': common_handlers,
            'level': log_level,
        },
    }
