#!/home/arthurb/.local/share/virtualenvs/fishisland-mOMQ3Mer/bin/python
import requests


assert requests.post('http://localhost:5000/tick', {'secret' : 'notright'}).status_code = 401
assert requests.post('http://localhost:5000/tick', {'secret' : 'soopersecret'}).status_code = 200

key = requests.post('http://localhost:5000/register', {'name' : : 'tutur'}).json()['key']
