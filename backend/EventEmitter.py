from events import Events
from Constants import Constants


class EventEmitter(Events):
    """
    Put all valid events here! Added to check misspelling.
    """
    __events__ = Constants.allowed_events

    """
    Instance of EventEmitter
    """
    instance = None

    """
    Anti-pattern alert!
    """
    @staticmethod
    def get():
        if EventEmitter.instance is None:
            EventEmitter.instance = EventEmitter()
        return EventEmitter.instance
