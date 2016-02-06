import json
from celery import Celery

queue = Celery('swirly')
queue.config_from_object('celeryconfig')


@queue.task
def processPayload(payload):
    """
    Worker implemention. Assume a list of colors
    :param payload:
    :return:
    """
    result = {'success': None, 'numberofcolors': None, 'black': None}

    if payload:
        colors = json.loads(payload)
        numcolors = len(colors)
        numcolors = len(payload)
        result['success'] = True
        result['numberofcolors'] = numcolors
        
        return str(json.dumps(result))
    else:
        return result
