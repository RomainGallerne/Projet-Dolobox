from machine import Timer
from Singleton import Singleton

@Singleton
class TimerManager:
    def __init__(self):
        self.timers = {}  # Dictionnaire pour stocker les timers actifs
        self.id_timers = set()
    def set_timer(self, identifier, period, units, callback):
        if identifier in self.timers:
            self.timers[identifier].deinit()  # Arrêter le timer si un timer avec le même identifiant existe déjà
            timer = Timer(timers[identifier]['id'])
            period_ms = self.convert_to_milliseconds(period, units)
            timer.init(period=period_ms, mode=Timer.PERIODIC, callback=callback)
            self.timers[identifier]['timer'] = timer
            return
        
        period_ms = self.convert_to_milliseconds(period, units)
        print(period_ms)
        id = self.find_available_timer_id()
        self.id_timers.add(id)
        timer = Timer(id)
        timer.init(period=period_ms, mode=Timer.PERIODIC, callback=callback)
        self.timers[identifier] = {'timer':timer,'id':id}

    def remove_timer(self, identifier):
        if identifier in self.timers:
            self.timers[identifier]['timer'].deinit()
            
            del self.timers[identifier]
    def find_available_timer_id(self):
        timer_id = 0
        while timer_id in self.id_timers:
            timer_id += 1
        return timer_id

    def convert_to_milliseconds(self, period, units):
        if units == "s":
            return period * 1000
        elif units == "m":
            return period * 1000 * 60
        elif units == "h":
            return period * 1000 * 60 * 60
        else:
            raise ValueError("Invalid units. Please use 's', 'm', or 'h'.")
    def get_timers(self):
        print(self.timers)
        print(self.id_timers)
