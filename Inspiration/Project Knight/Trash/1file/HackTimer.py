class HackTimer:
    def __init__(self):
        self.fake_id_to_callback = {}
        self.fake_id = 0
        self.max_fake_id = 0x7FFFFFFF  # Maximum fake ID, similar to the JS version

    def get_fake_id(self):
        self.fake_id += 1
        if self.fake_id >= self.max_fake_id:
            self.fake_id = 0
        return self.fake_id

    def set_interval(self, callback, interval, *args):
        fake_id = self.get_fake_id()
        self.fake_id_to_callback[fake_id] = callback
        while True:
            # Blocking loop to simulate interval behavior
            for _ in range(int(interval * 1e7)):  # Loop simulating the delay
                pass
            callback(*args)

    def clear_interval(self, fake_id):
        if fake_id in self.fake_id_to_callback:
            del self.fake_id_to_callback[fake_id]

    def set_timeout(self, callback, timeout, *args):
        fake_id = self.get_fake_id()
        self.fake_id_to_callback[fake_id] = callback
        for _ in range(int(timeout * 1e7)):  # Blocking loop to simulate timeout
            pass
        callback(*args)

    def clear_timeout(self, fake_id):
        if fake_id in self.fake_id_to_callback:
            del self.fake_id_to_callback[fake_id]
