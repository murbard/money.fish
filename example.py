import requests
import time

url = 'http://localhost:5000' # 'https://money.fish'

key = 'db1579c949d0ff926571fb87fde937b1f93f4085'
# Register the player
r = requests.post(url + '/register', {'name': 'Robinson', 'key': key})
print(r.content)

# Poll until start

day = 0

def place_orders(info):
    fish = info[key]['fish']
    last_price = info['last_price']
    last_price = last_price if last_price else 100

    # Naive strategy
    if fish > 2:
        for i in range(0, fish - 2):
            requests.post(url + '/order/%s' % key, {'shells': last_price})
    if fish < 2 :
        for i in range(0, 2 - fish):
            requests.post(url + '/order/%s' % key, {'shells': -int(last_price * 1.2)})

while True:
    try:
        info = requests.get(url + '/info/%s' % key)
        if info.status_code == 404:
            # had to leave the island
            print("bye bye")
            exit(0)
        info = info.json()
        if info['day'] > day:
            place_orders(info)
    except Exception as e:
        print(e)
    # wait
    time.sleep(1)


