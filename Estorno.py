import requests
from Pix import Token
import json
import certifi
class Estorno:
    def __init__(self):
        self.token = Token().obter_token()

    def gerar_estorno(self, end_to_end, valor):

        header = {
            "Authorization": f"Bearer {self.token}"
        }

        data = {
            "valor": valor
        }
        url = f"https:suaurl/{end_to_end}/suaurl"
        res = requests.put(url, headers=header, json=data, verify=True)
        response = res.json()

        return response
    
    def validar_estorno(self, txid):
        header = {

            "Authorization": f"Bearer {self.token}"
        }
        url = f"https:suaurl/{txid}/suaurl"
        res = requests.get(url, headers=header, verify=True)
        response = res.json()

        if "pix" in response and len(response["pix"]) > 0:
            pix_info = response["pix"][0]
            
            if "devolucoes" in pix_info and len(pix_info["devolucoes"]) > 0:
                status  = pix_info["devolucoes"][0]["status"]
                print(f"Favor validar , pois o Status:{status}")
                return False
            else:
                return True
        else:
            print("Não foi possível encontrar informações sobre este PIX.")
            return False
        