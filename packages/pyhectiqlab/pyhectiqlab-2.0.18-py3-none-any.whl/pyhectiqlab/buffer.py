from collections import defaultdict
from pyhectiqlab.timer import RepeatedTimer

class Buffer():

    def __init__(self, 
        max_cache_timeout=5,  # seconds
        max_cache_length=100, # Number of elements
        extra_args={},
        push_method=None):

        self.extra_args = extra_args
        self.cache = defaultdict(list)
        self.new_entries = defaultdict(int)
        self.can_record = defaultdict(lambda: True)

        self.max_cache_length = max_cache_length
        self.push_method = push_method

        self.timer = RepeatedTimer(self.flush_cache, max_cache_timeout)
        self.timer.start()
        return

    def pause_all(self):
        for key in self.can_record:
            self.can_record[key] = False

    def resume_all(self):
        for key in self.can_record:
            self.can_record[key] = True

    def stop(self, key):
        self.can_record[key] = False

    def start(self, key):
        self.can_record[key] = True

    def add(self, value, key):
        if self.can_record[key]==False:
            return

        self.new_entries[key] += 1
        self.cache[key].append(value)
        if len(self.cache[key])>self.max_cache_length:
            self.push_data(key)

    def push_data(self, key):
        if self.new_entries[key]>0:
            self.push_method(key, self.cache[key])
            
        self.new_entries[key] = 0 
        self.cache[key] = []

    def __delete__(self):
        self.stop_flag.set()
        self.timer.cancel()
        self.flush_cache()

    def flush_cache(self):
        for key in self.cache:
            self.push_data(key)
