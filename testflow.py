"""
import unirest
from gevent import monkey;
monkey.patch_all()

# Make a pool of greenlets to make your requests
from gevent.pool import Pool
pool = Pool(10)

mylist = []

def makeRequest():
    response = unirest.post("http://sunflower:8080/payload", headers={ "Content-Type": "application/x-www-form-urlencoded" }, params={ "payload": "sdfasdfsdf" })
    print response

pool.imap_unordered(makeRequest, mylist)
"""


"""
import gevent.pool
import json

from geventhttpclient import HTTPClient
from geventhttpclient.url import URL

url = URL('http://sunflower:8080/payload')
http = HTTPClient.from_url(url, concurrency=10)

def sendPayload():
    
    response = http.post(url.request_uri, 'payload=sadfadfs')
    print response


pool = gevent.pool.Pool(1)
pool.spawn(sendPayload)

pool.join()
http.close()

"""

"""
# This will make requests compatible
from gevent import monkey; 
monkey.patch_all()

import requests

concurrent_connections = 10
total_requests = 10000
payload = {'payload': "5B%7Bcolor%3A%22red%22%2Cvalue%3A%22%23f00%22%7D%2C%7Bcolor%3A%22green%22%2Cvalue%3A%22%230f0%22%7D%2C%7Bcolor%3A%22blue%22%2Cvalue%3A%22%2300f%22%7D%2C%7Bcolor%3A%22cyan%22%2Cvalue%3A%22%230ff%22%7D%2C%7Bcolor%3A%22magenta%22%2Cvalue%3A%22%23f0f%22%7D%2C%7Bcolor%3A%22yellow%22%2Cvalue%3A%22%23ff0%22%7D%2C%7Bcolor%3A%22black%22%2Cvalue%3A%22%23000%22%7D%5D%0A"}
from gevent.pool import Pool
pool = Pool(concurrent_connections)

urls = ["http://sunflower:8080/payload" for i in range(total_requests)]

pool.map(requests.post, urls)
"""
