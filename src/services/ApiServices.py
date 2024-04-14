import requests
from dotenv import load_dotenv
import os
import asyncio
from Singleton import Singleton



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


async def main():
    api = ApiService()
    login_response = await api.login("test", "1234")
    token = login_response["accessToken"]
    records = [
        {
            "level": 5,
            "evaluation_date": "01-09-2022 00:01:02"
        },
        {
            "level": 6,
            "evaluation_date": "01-09-2022 0:01:01"
        }
    ]
    patient_id = 6
    add_streams_response = await api.add_streams(patient_id, records, token)
    print(add_streams_response)
        
    
    

asyncio.run(main())
