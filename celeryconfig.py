#BROKER_URL = 'amqp://swirly:swirly@localhost:5672//'
#CELERY_RESULT_BACKEND = 'amqp://swirly:swirly@localhost:5672//'

BROKER_URL = 'redis://localhost/0'
CELERY_RESULT_BACKEND = 'redis://localhost/0'

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Europe/Athens'
CELERY_ENABLE_UTC = True

