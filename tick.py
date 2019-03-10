import requests
import os
import time

secret = os.environ['FISH_SECRET']

for i in range(0, 365):
    print(i)
    requests.post('http://localhost:5000/tick', {'secret': secret})
    time.sleep(5)