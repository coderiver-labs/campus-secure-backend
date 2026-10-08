from decouple import config


# configure celery or rabbitmq hare


CELERY_BROKER_URL = str(config("CELERY_BROKER_URL"))

# CELERY_RESULT_BACKEND = 'django-db'   # celery kono kon kajj ses korlo tar log db te save korte ata use kora hoy
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Dhaka'
CELERY_WORKER_HIJACK_ROOT_LOGGER = False

# server cresh korle data save rakhbe , abar start hole sei data diyei abar celery suru hobe
CELERY_TASK_ACKS_LATE = True 
CELERY_TASK_REJECT_ON_WORKER_LOST = True

# automatic (Retry) config
CELERY_TASK_AUTORETRY_FOR = (Exception,) # Jekono Error asle auto retry korbe
CELERY_TASK_RETRY_BACKOFF = True         # biroti niye retry korbe
CELERY_TASK_RETRY_BACKOFF_MAX = 600      # shorbosso 10 time niye retry korbe
CELERY_TASK_MAX_RETRIES = 3              # shorbosso 3bar retry korbe ar pore theme jabe


"""Celery Beat"""
CELERY_BEAT_SCHEDULE = {
    "cleanup-invalid-ied-users-every-hour": {
        "task": "celery_task.task.clean_JWT_tokens",
        "schedule": 86400,  # one day
    },
    "cleanup-onetime-expired-token": {
        "task": "celery_task.task.clean_one_time_token",
        "schedule": 86400,
    },
    "delete-unverified-users-every": {        
        "task": "celery_task.task.delete_unverified_users",
        "schedule": 86400,
    }
}

