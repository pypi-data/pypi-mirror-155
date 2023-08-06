
import json
import os.path


class Memcached:
    def __init__(self):
        self.data = dict()

    def set(self, key, value):
        self.data[key] = value
        with open(os.path.join(os.path.dirname(__file__), 'memcached.tmp'), 'w') as f:
            f.write(json.dumps(self.data))

    def get(self, key):
        if not os.path.exists(os.path.join(os.path.dirname(__file__), 'memcached.tmp')): return None
        with open(os.path.join(os.path.dirname(__file__), 'memcached.tmp'), 'r') as f:
            return json.loads(f.read()).get(key)


memcached = Memcached()
