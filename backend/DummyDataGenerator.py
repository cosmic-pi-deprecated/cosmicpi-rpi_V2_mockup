from EventEmitter import EventEmitter
import time
import random
import threading


"""
This module only generates events. `EventEmitter.get()` should be implemented into the core
of Cosmic Pi application.

Idea behind EventEmitter is to push event (call on_something() method) every time some event
happened. Once method is called event is propagated to rest of the system.
"""
class DummyDataGeneratorHandler(object):
    def run(self):
        while True:
            time.sleep(0.2)
            EventEmitter.get().on_temperature(round(random.uniform(20, 30), 2))
            EventEmitter.get().on_pressure(round(random.uniform(950, 1100), 2))
            EventEmitter.get().on_magnetism(round(random.uniform(0, 1), 2))

class DummyDataGenerator(object):
    @staticmethod
    def async_start():
        dummy_data_generator_handler = DummyDataGeneratorHandler()
        thread = threading.Thread(target=dummy_data_generator_handler.run)
        thread.start()