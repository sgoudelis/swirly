#!env/bin/python
"""
Issues

1. When using gunicorn and bombarding this web api with requests, gunicorn
with complain with:

[2454] [ERROR] Error handling request
Traceback (most recent call last):
  File "/usr/lib/python2.7/dist-packages/gunicorn/workers/async.py", line 116, in handle_request
    raise StopIteration()


According to https://github.com/benoitc/gunicorn/issues/65 this can be safely ignored.
"""

import falcon
#import json
from celery import Celery
from celery.exceptions import TimeoutError
from worker import processPayload
#from gevent.pywsgi import WSGIServer

class HandlePayload:
    def on_get(self, request, response):
        """
        Handle GET /payload
        """
        
        payloadid = request.get_param("payloadid", default=None)
        if payloadid:
            result = processPayload.AsyncResult(payloadid)
            response.status = falcon.HTTP_200
            response.append_header('swirly-demotask-result', str(result.get()))
        else:
            response.status = falcon.HTTP_404
        
    def on_post(self, request, response):
        """
        Handle POST /payload
        """
        
        payload = request.get_param("payload", default=None)
        timeout = request.get_param_as_int('timeout') or 0   # is seconds
        
        if payload:
            # payload exists, push task into queue
            task = processPayload.delay(payload)
            if timeout > 0:
                # user requested a blocking call, wait until timeout in case the task is complete
                try:
                    task_result = task.get(timeout=timeout)
                    response.status = falcon.HTTP_200
                    response.append_header('swirly-demotask-result', task_result)
                except TimeoutError:
                    # task timed-out, handle it
                    response.status = falcon.HTTP_408
                    response.append_header('swirly-message', "Request timed-out. Task is pending.")
                    
            else:
                # issue a 202 Accepted code
                response.status = falcon.HTTP_202
                response.append_header('swirly-demotask-id', str(task.id))

        else:
            # issue a 400 HTTP error code in case of a POST without a payload
            response.status = falcon.HTTP_400
            response.append_header('swirly-message', "No payload")
        
# create Celery queue
queue = Celery('swirly')

# load configuration
queue.config_from_object('celeryconfig')

# create Falcon WSGI object
webapp = falcon.API()

# create route for path /payload
webapp.add_route('/payload', HandlePayload())

'''
# start the Gevent WSGI server
WSGIServer(('', 8080), webapp).serve_forever()
'''
