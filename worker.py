import os
from decouple import config
from urllib.parse import urlparse
from redis import Redis
from rq import Worker, Queue, Connection

listen = ['high', 'default', 'low']

redis_url = config('REDIS__URL')
if not redis_url:
    raise RuntimeError('Set up Redis To Go first.')

redis_url = os.getenv('REDISTOGO_URL')

urlparse.uses_netloc.append('redis')
url = urlparse.urlparse(redis_url)
conn = Redis(host=url.hostname, port=url.port, db=0, password=url.password)

if __name__ == '__main__':
	with Connection(conn):
		worker = Worker(map(Queue, listen))
		worker.work()
