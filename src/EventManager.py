from abc import ABC, abstractmethod

class Event(ABC):
    def __init__(self):
        self.listeners = []
        

    def add_listener(self, callback):
        self.listeners.append(callback)
        return self

    def remove_listener(self, callback):
        self.listeners.remove(callback)
        return self

    @abstractmethod
    def trigger(self, *args, **kwargs):
        pass

class OnClick(Event):
    def trigger(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

class OnChange(Event):
    def trigger(self, *args, **kwargs):
        for listener in self.listeners:
            listener(*args, **kwargs)

class EventManager:
    def __init__(self):
        self.events = {}

    def get_event(self, event_name):
        if event_name not in self.events:
            self.events[event_name] = self.create_event(event_name)
        return self.events[event_name]

    def add_event_listener(self, event_name, callback):
        if event_name == "onclick":
            return OnClick().add_listener(callback)
        elif event_name == "onchange":
            return OnChange().add_listener(callback)
        else:
            raise NotImplementedError("Unknown event type: {}".format(event_name))
em = EventManager()

#btn: Event = em.add_event_listener("onclick", lambda elem: (
#    print("Button clicked"),
#    print(elem)
#))

#btn.trigger("Button test")
                                    
