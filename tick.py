import requests
import os
import time
from datetime import datetime

secret = os.environ['FISH_SECRET']
url = 'http://localhost:5000'

requests.post(url + '/run',
              {'secret': secret, 'action': 'reset'})

time.sleep(180)

for i in range(0, 365):
    requests.post(url + '/run',
                  {'secret': secret, 'action': 'tick'})
    time.sleep(4)

stats = requests.post('http://localhost:5000/stats', {'secret' : secret}).json()

time = datetime.now().strftime('%Y-%m-%dZ%H:%M:%S')
json.dumpf(stats, open('stats_%s' % time,'w'))
