import shelve


class Cache:
    def __init__(self, db_path):
        self._db = shelve.open(str(db_path))

    def get(self, key):
        return self._db[key]

    def set(self, key, value):
        self._db[key] = value

    def close(self):
        self._db.close()

