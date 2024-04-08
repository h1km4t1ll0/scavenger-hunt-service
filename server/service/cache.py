import time


class Cache:
    def __init__(self, timeout: int, get_new_data: callable):
        self.timeout = timeout
        self.data = get_new_data()
        self.get_new_data = get_new_data
        self.last_modified = int(time.time())

    def _invalidate(self):
        self.last_modified = int(time.time())
        self.data = self.get_new_data()

    def get(self):
        if int(time.time()) - self.last_modified >= self.timeout:
            self._invalidate()
            return self.data
        return self.data
