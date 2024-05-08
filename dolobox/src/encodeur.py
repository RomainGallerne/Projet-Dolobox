from machine import Pin, PWM, ADC, RTC
import network
import uasyncio
from time import sleep
import urequests
import json


un = Pin(18,Pin.IN)
deux = Pin(22,Pin.IN)
quatre = Pin(23,Pin.IN)
huit = Pin(19,Pin.IN)

valeurs_encodeur_rotatifs = [
        [0,0,0,0],
        [1,0,0,0],
        [0,1,0,0],
        [1,1,0,0],
        [0,0,1,0],
        [1,0,1,0],
        [0,1,1,0],
        [1,1,1,0],
        [0,0,0,1],
        [1,0,0,1],
        [0,1,0,1],
        [1,1,0,1],
        [0,0,1,1],
        [1,0,1,1],
        [0,1,1,1],
        [1,1,1,1]
    ]

while True:
    tab_releve_encodeur_rotatif = [
           un.value(),
           deux.value(),
           quatre.value(),
           huit.value()
        ]
    valeur_encodeur_rotatif = valeurs_encodeur_rotatifs.index(tab_releve_encodeur_rotatif)
    print("valeur de l'encodeur rotatif :", valeur_encodeur_rotatif)