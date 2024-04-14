from abc import ABC, abstractmethod
import time

class Event(ABC):
    def __init__(self):
        self.listeners = []

    def add_listener(self, callback):
        self.listeners.append(callback)
        return self

    def remove_listener(self, callback):
        self.listeners.remove(callback)
        return self

    async def trigger(self, *args, **kwargs):
        for listener in self.listeners:
            await listener(*args, **kwargs)

class OnClick(Event):
    pass

class OnChange(Event):
    pass

class EventFactory:
    @staticmethod
    def create_event(event_name):
        if event_name == "onclick":
            return OnClick()
        elif event_name == "onchange":
            return OnChange()
        else:
            raise NotImplementedError("Unknown event type: {}".format(event_name))

class EventManager:
    def __init__(self):
        self.events = {}

    def get_event(self, event_name):
        if event_name not in self.events:
            self.events[event_name] = self.create_event(event_name)
        return self.events[event_name]

    def add_event_listener(self, event_name, callback):
        return EventFactory.create_event(event_name).add_listener(callback)
       


                                    
