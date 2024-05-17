import utime
from machine import Pin
class Button:
    def __init__(self,pin,debounce=10000):
        self.btn = Pin(pin,Pin.IN, Pin.PULL_UP)
        self.last_button_change = 0
        self.debounce_delay=debounce
    def is_pressed(self):
        current_time = utime.ticks_ms()
        if current_time - self.last_button_change > self.debounce_delay:
            value = self.btn.value()
            if(value == 0):
                self.last_button_change = current_time
            return  value == 0
        return False
    def getButton(self):
        return self.btn
        
        

