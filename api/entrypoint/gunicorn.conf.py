# gunicorn.conf.py
import os
import multiprocessing


# Logging configuration
DEBUG = os.environ.get("DEBUG", "").lower() == "true"
loglevel = "DEBUG" if DEBUG else "INFO"


# Basic server configuration
workers = (
    multiprocessing.cpu_count() * 2 + 1
)  # Formula for workers is (2 x $num_cores) + 1

# Configure logging
accesslog = "-"
errorlog = "-"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "gunicorn.error": {
            "level": "INFO",
            "handlers": ["console"],
            "propagate": True,
        },
        "gunicorn.access": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
