from machine import Pin, PWM, ADC, RTC
import network
import uasyncio
from time import sleep
import urequests
import json


pin_button = Pin(15,Pin.IN, Pin.PULL_UP)
slider = ADC(Pin(35))
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
    

def Singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


@Singleton
class ApiService:
    def __init__(self):
        # Chargez les paramètres nécessaires
        self.base_url = "https://eriospainapi.onrender.com"
        
    async def login(self, username, password):
        url = f"{self.base_url}/api/login"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = "username={}&password={}".format(username, password)
        try:
            response = urequests.post(url, headers=headers, data=payload)
            return response.json()
        except Exception as e:
            print("Error in login request:", e)
            return None

    async def getUsers(self, token):
        url = f"{self.base_url}/api/users"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        try:
            response = urequests.get(url, headers=headers)
            return response.json()
        except Exception as e:
            print("Error in getUsers request:", e)
            return None

    async def add_streams(self, patient_id, records, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        url = f"{self.base_url}/api/patient/{patient_id}/streams"
        payload = json.dumps({"records": records})
        print(payload)

        try:
            response = urequests.post(url, headers=headers, data=payload)  # Utiliser data=payload au lieu de json=payload
            return response.json()
        except Exception as e:
            print("Error in add_streams request:", e)
            return None


        
async def send_data():
    value = slider.read()
    date = get_current_datetime()
    records = [
            {"level":value,"evaluation_date":date}
        ]
    api = ApiService()
    print(records)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjEsImlhdCI6MTcxNDY3MDc3OCwiZXhwIjoxNzE0Njc0Mzc4fQ.8qCnLa9SbBx2XcBSt_JJe_qBrRkPPnhFJsrGbARD0VM"
    response = await api.add_streams(1,records,token)
    print(response)

def pressed(btn):
    print("pressed")
    task = uasyncio.create_task(send_data())
    # Attendre que la tâche soit terminée
    loop = uasyncio.get_event_loop()
    loop.run_until_complete(task)
    
pin_button.irq(trigger=Pin.IRQ_FALLING, handler=pressed)

do_connect()

while True:
    pass
