from Singleton import Singleton

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
