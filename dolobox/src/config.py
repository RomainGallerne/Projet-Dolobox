from Singleton import Singleton

class Config:
    config = {
        "TOKEN":"",
        "API_URL":"https://eriospainapi.onrender.com",
        "WIFI_NAME":"",
        "WIFI_PASSWORD":""
        }
    @staticmethod
    def get_config(name):
        return Config.config[name]
        
        
