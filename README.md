# swirly

## Demostration for non-blocking high-speed Web API with asynchronous job handling.

This is work in progress. Incomplete code warning.

A collection of python scripts that make up high-speed non-blocking HTTP API with asynchronous job handling.  

## Requirements

1. celery
2. falcon
3. grequests
4. python 2.7+
5. redis
6. gunicorn


### Setup

Create a virtual enviroment with virtualenv.

```
$ virtualenv  env
Running virtualenv with interpreter /usr/bin/python2
New python executable in env/bin/python2
Also creating executable in env/bin/python
Installing setuptools, pip...done.

$ env/bin/pip install celery falcon grequests redis 
```


### Start up worker and API

```
$ celery worker -A swirly -l info
```

```
$ gunicorn -c gunicornconfig.py swirly:webapp
```


### Run benchmark

```
$ ab -n 10000 -c 100 -p postdata/postdata.txt -T 'application/x-www-form-urlencoded' http://localhost:8080/payload 
Benchmarking sunflower (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        gunicorn/19.3.0
Server Hostname:        sunflower
Server Port:            8080

Document Path:          /payload
Document Length:        0 bytes

Concurrency Level:      100
Time taken for tests:   0.337 seconds
Complete requests:      1000
Failed requests:        0
Total transferred:      183000 bytes
Total body sent:        611000
HTML transferred:       0 bytes
Requests per second:    2965.41 [#/sec] (mean)
Time per request:       33.722 [ms] (mean)
Time per request:       0.337 [ms] (mean, across all concurrent requests)
Transfer rate:          529.95 [Kbytes/sec] received
                        1769.40 kb/s sent
                        2299.35 kb/s total

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.7      0       3
Processing:     2   31  23.7     26     204
Waiting:        1   31  23.6     25     204
Total:          3   32  23.7     26     205

Percentage of the requests served within a certain time (ms)
  50%     26
  66%     33
  75%     38
  80%     43
  90%     59
  95%     70
  98%    113
  99%    133
 100%    205 (longest request)

```


