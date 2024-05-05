from machine import Pin, PWM, ADC, RTC
import network
import uasyncio
from time import sleep
import urequests
import json
# 18, 22 , 23, 19

class Encoder:
    def __init__(self,pin_un, pin_deux, pin_quatre, pin_huit):
        self.un = Pin(pin_un,Pin.IN)
        self.deux = Pin(pin_deux,Pin.IN)
        self.quatre = Pin(pin_quatre,Pin.IN)
        self.huit = Pin(pin_huit,Pin.IN)
        self.valeurs_encodeur_rotatifs = [
            [0, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 0],
            [1, 0, 1, 0],
            [0, 1, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 0, 1],
            [1, 1, 0, 1],
            [0, 0, 1, 1],
            [1, 0, 1, 1],
            [0, 1, 1, 1],
            [1, 1, 1, 1]
        ]

    def value(self):
        tab_releve_encodeur_rotatif = [
           self.un.value(),
           self.deux.value(),
           self.quatre.value(),
           self.huit.value()
        ]
        return self.valeurs_encodeur_rotatifs.index(tab_releve_encodeur_rotatif)
encoder = Encoder(18,22,23,19)


while True:
    
    print("valeur de l'encodeur rotatif :", encoder.value())
    
