from Singleton import Singleton
from time import sleep
from utime import ticks_ms

@Singleton
class LedManager:

    def __init__(self):
        self.leds = {}
    
    def add_led(self, identifier, led):
        self.leds[identifier] = led
        
    def remove_led(self, identifier):
        del self.leds[identifier]
 
    def on(self, identifier):
        self.leds[identifier].on()
        
    def off(self, identifier):
        self.leds[identifier].off()
    
    def blink(self, identifier, time, freq):
        current = ticks_ms()
        end = time + current
        while(current < end):
            self.on(identifier)
            sleep(freq)
            self.off(identifier)
            sleep(freq)
            current = ticks_ms()
    def off_all(self):
        for identifier, led in self.leds.items():
            led.off()
        
    
        
        
