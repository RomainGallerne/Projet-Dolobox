from machine import Pin, PWM, ADC, RTC
import network
import uasyncio
from time import sleep, sleep_ms
from ApiService import ApiService
import utime
from TimerManager import TimerManager



pin_button = Pin(23,Pin.IN, Pin.PULL_UP)
slider = ADC(Pin(36))
led_1 = Pin(12,Pin.OUT)
led_1.off()
timer_launched = False
last_button_change = 0
debounce_delay = 10000
response_time = 10000

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
        wlan.connect("Livebox-C094", "A3312A63FF2F7947C712D43F64")
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())
    


        
async def send_data():
    value = slider.read()
    date = get_current_datetime()
    records = [
            {"level":value,"evaluation_date":date}
        ]
    api = ApiService()
    print(records)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjksImlhdCI6MTcxNDc3MzQ1OCwiZXhwIjoxNzE0Nzc3MDU4fQ.6Atfj_Sq1RbEy7Bb3yecbBYV9OngT_kdlX7Odysk0U0"
    response = await api.add_streams(6,records,token)
    print(response)


def on_submit(btn):
    global last_button_change
    current_time = utime.ticks_ms()
    if current_time - last_button_change > debounce_delay:
        if btn.value() == 0:
            print(btn.value())
            last_button_change = current_time
            task = uasyncio.create_task(send_data())
            loop = uasyncio.get_event_loop()
            loop.run_until_complete(task)

def on_timer_submit(timer):
    print("You can start to submit")
    led_1.on()
    print("LED IS ON")

    start_time = utime.ticks_ms()
    current_time = start_time
    while(current_time-start_time<response_time):
        global last_button_change
        current_time = utime.ticks_ms()
        if current_time - last_button_change > debounce_delay:
            if pin_button.value() == 0:
                last_button_change = current_time
                task = uasyncio.create_task(send_data())
                loop = uasyncio.get_event_loop()
                loop.run_until_complete(task)
                print("LED IS OFF")
                led_1.off()
                return
    led_1.off()
    print("LED IS OFF")
    return
pin_button.irq(trigger=Pin.IRQ_FALLING, handler=on_submit)

tm = TimerManager()
do_connect()

tm.set_timer('submit_timer',30,'s',on_timer_submit)

while True:
    pass



