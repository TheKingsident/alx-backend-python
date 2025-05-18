#!/usr/bin/python3
import sys
from importlib import import_module
lazy_paginator = import_module('2-lazy_paginate').lazy_paginate


try:
    for page in lazy_paginator(100):
        for user in page:
            print(user)

except BrokenPipeError:
    sys.stderr.close()