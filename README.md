# swirly

## Demostration for non-blocking high-speed Web API.

A collection of python scripts that make up high-speed non-blocking HTTP API.  

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
```


