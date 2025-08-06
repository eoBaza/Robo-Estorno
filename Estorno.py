import requests
from Script_Estorno.Pix import Token
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
        
        res = requests.put(f"https://pix.qqpag.com.br/api/v2/pix/{end_to_end}/devolucao/30507", headers=header, json=data, verify=False)
        response = res.json()

        return response
    
    def validar_estorno(self, txid):
        header = {

            "Authorization": f"Bearer {self.token}"
        }
        res = requests.get(f"https://pix.qqpag.com.br/api/v1/cob/{txid}", headers=header, verify=False)
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
        