#!/usr/bin/python3
from itertools import islice
from importlib import import_module
stream_users = import_module('0-stream_users').stream_users

for user in islice(stream_users(), 6):
    print(user)