from machine import ADC, Pin
from time import sleep
import uasyncio

btn = Pin(23, Pin.IN, Pin.PULL_UP)
slider = ADC(Pin(36))
slider.atten(ADC.ATTN_11DB)

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('ssid', 'key') # Id et mot de passe wifi
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
        load_dotenv()
        self.base_url = os.getenv("API_URL")
        
    async def login(self, username, password):
        url = f"{self.base_url}/api/login"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        payload = f"username={username}&password={password}"

        response = requests.post(url, headers=headers, data=payload)
        if response.ok:
            return response.json()
        return None

    async def add_streams(self, patient_id, records, token):
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"  # Utilisez 'application/json' pour envoyer des données JSON
        }
        url = f"{self.base_url}/api/patient/{patient_id}/streams"
        payload = {"records": records}  # Construisez la charge utile comme un objet JSON
        response = requests.post(url, headers=headers, json=payload)  # Utilisez 'json=payload' pour envoyer des données JSON
        if response.ok:
            return response.json()
        return None

async def press():
    while True:
        if(btn.value() == 0):
            print("Mesure de douleur: "+str(slider.read()))
            sleep(1)
        


uasyncio.run(press())
