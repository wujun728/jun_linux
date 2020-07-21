
import requests
from redis import Redis
from rq import Queue
from some import count_words_at_url

# create a RQ queue:
q = Queue(connection=Redis())

# enqueue the function call:
job = q.enqueue(count_words_at_url, 'http://nvie.com')
print job