from machine import Pin, PWM, ADC, RTC, unique_id
import network
import uasyncio
from time import sleep, sleep_ms
from ApiService import ApiService
import utime
from TimerManager import TimerManager
from Button import Button
from LedManager import LedManager
from json import load
from config import Config
import ubinascii
lm = LedManager()

submit_btn = Button(22)
timer_btn = Button(23,debounce=3000)
slider = ADC(Pin(36))
interruptor = ADC(Pin(34))
interruptor.atten(ADC.ATTN_11DB)
slider.atten(ADC.ATTN_11DB)

def read_switch_position():
    value = interruptor.read()
    if value < 1500:  
        return "Aidant"
    elif 1500 <= value < 3500:
        return "Soignant"
    elif value >= 3500: 
        return "Patient"
    else:
        return "Valeur inconnue"

lm.add_led("submit", Pin(27,Pin.OUT))
lm.add_led("mode1", Pin(13,Pin.OUT))
lm.add_led("mode2", Pin(12,Pin.OUT))
lm.add_led("mode3", Pin(14,Pin.OUT))



time_repetitions = [2,4,6]
mode = 0


lm.off("submit")
lm.off("mode1")
lm.off("mode2")
lm.off("mode3")

response_time = 10000
def get_slider_value(value):
    if value<0 or value>4095:
        return None
    f = open('FuzzyLogicModel.json')
    data = load(f)
    f.close()
    value = 4095-value

    return data["fonction_douleur"][value]

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

def turn_off_all():
    lm = LedManager()
    for i in range(1,len(time_repetitions)+1):
        lm.off("mode"+str(i))

async def send_data():
    value = slider.read()
    date = get_current_datetime()
    value = get_slider_value(value)
    lm = LedManager()
    if(value == None):
        lm.blink("submit",20000,0.75)
        return 
    records = [
            {"level":value,"evaluation_date":date}
        ]
    api = ApiService()
    print(records)
    print("Rôle: "+read_switch_position())
    token = Config.get_config("TOKEN")
    try:
        response = await api.add_streams(9,records,token)
        print(response)
        if response["message"] == 'Fail':
            lm.blink("submit",20000,0.75)
            return        
    except Exception as e:
        print(e)
        lm.blink("submit",20000,0.75)
        return

def on_submit(btn):

    if submit_btn.is_pressed():
        lm.on("submit")
        task = uasyncio.create_task(send_data())
        loop = uasyncio.get_event_loop()
        loop.run_until_complete(task)
        lm.off("submit")

def on_timer_submit(timer):
    print("You can start to submit")
    lm = LedManager()
    lm.on("submit")
    print("LED IS ON")

    start_time = utime.ticks_ms()
    current_time = start_time
    while(current_time-start_time<response_time):
        if submit_btn.is_pressed():
            last_button_change = current_time
            task = uasyncio.create_task(send_data())
            loop = uasyncio.get_event_loop()
            loop.run_until_complete(task)
            print("LED IS OFF")
            lm.off("submit")
            return
    lm.off("submit")
    print("LED IS OFF")
    return

def timer_setup(btn):
    if timer_btn.is_pressed():
        tm = TimerManager()
        lm = LedManager()
        global mode
        global time_repetitions
        mode = (mode + 1) % (len(time_repetitions)+1)
        print("Mode: "+str(mode))
        turn_off_all()
        if mode == 0:
            tm.remove_timer("submit_timer")
            tm.get_timers()
            submit_btn.getButton().irq(trigger=Pin.IRQ_FALLING, handler=on_submit)
            return
        lm.on("mode"+str(mode))
        tm.set_timer("submit_timer",time_repetitions[mode-1],'m',on_timer_submit)
        tm.get_timers()
        submit_btn.getButton().irq(trigger=0, handler=on_submit)       


submit_btn.getButton().irq(trigger=Pin.IRQ_FALLING, handler=on_submit)
timer_btn.getButton().irq(trigger=Pin.IRQ_FALLING, handler=timer_setup)

   

while True:
    pass




