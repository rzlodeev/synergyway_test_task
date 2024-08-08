from celery import Celery

celery_app = Celery(
    'tasks',
    broker='amqp://myuser:mypassword@rabbitmq:5672/vhost',
    backend='rpc://'
)

celery_app.conf.beat_schedule = {
    'update_user_info': {
        'task': 'src.tasks.update_user_info',
        'schedule': 30 * 60,  # Every 30 minutes
    },
    'update_credit_card_info': {
        'task': 'src.tasks.update_credit_card_info',
        'schedule': 40 * 60,  # Every 40 minutes
    },
    'update_addresses_info': {
        'task': 'src.tasks.update_user_info',
        'schedule': 60 * 60,  # Every 60 minutes
    },
}

celery_app.conf.timezone = 'UTC'
