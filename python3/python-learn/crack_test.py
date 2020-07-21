import requests
import time

'''
tech stack
bootstrap
fancyBox
Wookmark 
http://github.com/tkem/jquery-image
https://github.com/jnordberg/gif.js
'''

def crack():
    url = "http://115.29.97.139:88/reg"
    data = {
        "m":"reg", 
        "e":"faker@faker.com", 
        "p":"faker123",
        "p1":"faker123",
        "n": "test123", 
        "t":str(time.time())
    }
    print url
    print data
    resp = requests.post(url, data)
    print resp.text


if __name__ == '__main__':
    crack()
