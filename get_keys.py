import sys
import os
import hashlib

secret = os.environ['FISH_SECRET']

def get_key(name):
    key = hashlib.blake2b(
        name.encode('ascii'),
        key=secret.encode('ascii'), digest_size=20).hexdigest()
    return key

for line in sys.stdin:
    print(line.rstrip(), get_key(line.rstrip()))
