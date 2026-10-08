import os
from pathlib import Path



# logger configuration

LOG_DIR = Path("/var/log/campus-secure")
LOG_DIR = LOG_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "json": {
            "()": "pythonjsonlogger.json.JsonFormatter",
            "format": "%(asctime)s %(levelname)s %(name)s %(message)s %(pathname)s %(lineno)d %(request_id)s %(user_id)s %(ip)s",
        },
        "console": {
            "format": "[%(asctime)s] %(levelname)s [%(name)s] - %(message)s",
        },
    },

    "filters": {
        "request_context": {
            "()": "utils.logging_filters.RequestContextFilter",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "console",
        },
        "app_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "app.log",
            "maxBytes": 10 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "json",
            "filters": ["request_context"],
        },
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "error.log",
            "level": "ERROR",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "json",
            "filters": ["request_context"],
        },
        "celery_file": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": LOG_DIR / "celery.log",
            "maxBytes": 5 * 1024 * 1024,
            "backupCount": 5,
            "formatter": "json",
            "filters": ["request_context"],
        },
    },

    "loggers": {
        "django": {
            "handlers": ["console", "app_file"],
            "level": "INFO",
            "propagate": False,
        },
        "django.request": {
            "handlers": ["error_file"],
            "level": "ERROR",
            "propagate": False,
        },
        "celery": {
            "handlers": ["celery_file"],
            "level": "INFO",
            "propagate": True,
        },
        "performance": {
            "handlers": ["app_file"],
            "level": "INFO",
            "propagate": False,
        },
    },

    "root": {
        "handlers": ["console", "app_file", "error_file"],
        "level": "INFO",
    },
}



"""
     Next Project Ar Moddhe Arokhom Korbo

                    LogRecord
                       │
          ┌────────────┼────────────┐
          │            │            │
        INFO        WARNING       ERROR+
          │            │            │
          ▼            ▼            ▼
       app_file     app_file     error_file
          │            │            │
          ▼            ▼            ▼
       app.log      app.log     error.log

"""