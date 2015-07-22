#!env/bin/python
"""
Flow description

Phase 1: POST tasks into the swirly API and store the task id of each task
Phase 2: GET the task result back using the list of task ids.

Test the flow of the swirly API. POST N number of requests with a payload
(a json object) using N number of concurrent connections and store the list of task ids
that come out of celery. Then use the list of task ids to fetch the results of the tasks
using the same number of requests and concurrency settings as before.

This script id using:

1. grequests https://github.com/kennethreitz/grequests
2. resource https://docs.python.org/2/library/resource.html
3. requests 

Usage: python testflow-grequests.py

Prerequisites: Please make sure that the swirly API and the swirly worker 
"""

concurrent_connections = 100
total_requests = 10000
nofile_limit = 999999

import time
import json
import grequests
from requests.exceptions import ConnectionError
import resource
from requests.adapters import HTTPAdapter
import requests

session = requests.Session()
session.mount('http://', HTTPAdapter())

ids = list()
post_times = list()
get_times = list()
task_results = list()

URL = "http://sunflower:8080/payload"
payload = {"red":"#f00","green":"#0f0","blue":"#00f","cyan":"#0ff","magenta":"#f0f","yellow":"#ff0","black":"#000"}

# change maximum number of open file descriptors for the current process.
print "Setting RLIMIT_NOFILE to %s" % nofile_limit
# try, except does not work, developer of grequests knows this
try:
    resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))
except ValueError:
    print "Could not set the maximum number of file descriptors to 999999"
    
def handlePOSTEndRequest(response, verify, cert, proxies, timeout, stream):
    headers = response.headers
    swirly_task_id = headers.get('swirly-demotask-id', None)
    if swirly_task_id:
        # we got a task id back, store it
        ids.append(swirly_task_id)
        post_times.append(time.time())

def handleGETEndRequest(response, verify, cert, proxies, timeout, stream):
    status = response.status_code
    if status == 200:
        task_results.append(response.headers.get("swirly-demotask-result"))
    get_times.append(time.time())


print "Preparing POST requests..."

post_requests = (grequests.post(URL, params={'payload': json.dumps(payload)}, session=session,  hooks = {'response' : handlePOSTEndRequest}) for i in range(total_requests))

starttime = time.time()

print "Starting to push payloads into the API..."

# try, except does not work, developer of grequests knows this
try:
    responses = grequests.map(post_requests, size=concurrent_connections)
except ConnectionError as e:
    print "Connection error"
    
post_times[:] = [t - starttime for t in post_times]
push_total_time = time.time() - starttime
push_rate = len(ids)/push_total_time
print "Completed %s POST requests at %s concurrency in %.2f seconds at rate of %s requests/s." % (total_requests, concurrent_connections, push_total_time, int(push_rate))

print "Preparing pull (GET) requests..."

get_requests = (grequests.get(URL, params={'payloadid': task_id}, session=session,  hooks = {'response' : handleGETEndRequest}) for task_id in ids)

starttime = time.time()
print "Starting GET requests of completed tasks..."

# try, except does not work, developer of grequests knows this
try:
    responses = grequests.map(get_requests, size=concurrent_connections)
except ConnectionError as e:
    print "Connection error"
    
get_times[:] = [t - starttime for t in get_times]
get_total_time = time.time() - starttime
get_rate = len(get_times)/get_total_time
print "Completed %s GET requests at %s concurrency in %.2f seconds at rate of %s requests/s." % (len(get_times), concurrent_connections, get_total_time, int(get_rate))
