from machine import Pin, PWM, ADC, RTC
import network
import uasyncio
from time import sleep, sleep_ms
import urequests
import json
from ApiService import ApiService
import utime
from TimerManager import TimerManager


debounce_delay = 10000  # Délai de débouncing en millisecondes
last_button_change = 0
pin_button = Pin(23,Pin.IN, Pin.PULL_UP)
slider = ADC(Pin(36))
def get_current_datetime():
    rtc = RTC()
    year, month, day, weekday, hour, minute, second, _ = rtc.datetime()
    # Ajouter un zéro devant les valeurs inférieures à 10
    day_str = "0{}".format(day) if day < 10 else str(day)
    month_str = "0{}".format(month) if month < 10 else str(month)
    hour_str = "0{}".format(hour) if hour < 10 else str(hour)
    minute_str = "0{}".format(minute) if minute < 10 else str(minute)
    second_str = "0{}".format(second) if second < 10 else str(second)
    return "{}-{}-{} {}:{}:{}".format(day_str, month_str, year, hour_str, minute_str, second_str)

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect("", "") #mettre le nom et mot de passe de wifi
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    


        
async def send_data():
    value = slider.read()
    print(value)
    date = get_current_datetime()
    records = [
            {"level":value,"evaluation_date":date}
        ]
    api = ApiService()
    #print(records)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImlhdCI6MTcxNDY3MDc3OCwiZXhwIjoxNzE0Njc0Mzc4fQ.8qCnLa9SbBx2XcBSt_JJe_qBrRkPPnhFJsrGbARD0VM"
    #response = await api.add_streams(1,records,token)
    #print(response)



def pressed(btn):
    global last_button_change
    current_time = utime.ticks_ms()
    if current_time - last_button_change > debounce_delay:
        if btn.value() == 0:
            print(btn.value())
            last_button_change = current_time
            task = uasyncio.create_task(send_data())
            loop = uasyncio.get_event_loop()
            loop.run_until_complete(task)
def fire(e):
    print(e)
    print("TIMER FIRE !!")
    
pin_button.irq(trigger=Pin.IRQ_FALLING, handler=pressed)

tm = TimerManager()
tm.set_timer("first_timer",1,"m",fire)
tm.set_timer("second_timer",30,"s",fire)

while True:
    sleep(2)
    tm.get_timers()


