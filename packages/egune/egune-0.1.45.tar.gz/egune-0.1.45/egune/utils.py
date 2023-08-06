import redis
from json import dumps, loads
import requests


def normalize_user_id(user_id):
    return user_id.split(":")[0]


class Cache(object):
    def __init__(self, config):
        self.redis = redis.Redis(host=config["host"], port=config["port"], db=0)
        self.ttl = config["ttl"]
        self.prefix = config["prefix"] + ":"

    def has(self, key):
        return self.redis.exists(self.prefix + str(key))

    def get(self, key):
        return loads(self.redis.get(self.prefix + str(key)))

    def put(self, key, value):
        self.redis.set(self.prefix + str(key), dumps(value), ex=self.ttl)

    def rm(self, key):
        return self.redis.delete(self.prefix + str(key))


class Module():
    def __init__(self, config):
        self.name = config["name"]
        if "cache" in config:
            self.cache = Cache(config["cache"])
        self.use_cache = "cache" in config
        self.address = f"http://{config['host']}:{config['port']}/"
        self.config = config

    def post(self, endpoint, *args):
        try:
            if self.use_cache:
                key = self.cache_key(endpoint, args)
                if self.cache.has(key):
                    return self.get(key)
            resp = requests.post(self.address + endpoint, json={
                "__args__": args
            })
            result = resp.json()["data"]
            if self.use_cache:
                key = self.cache_key(endpoint, args)
                self.cache.put(key, result)
            return result
        except Exception as e:
            print(f"ERROR: {self.name}", e, flush=True)

    def cache_key(self, endpoint, args):
        return ":".join([endpoint] + args)
