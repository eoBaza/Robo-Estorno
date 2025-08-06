import requests
import json
import certifi

class Token:
    def __init__(self):
        self.txid = None
        self.payload = None
        self.token = self.obter_token()

    def obter_token(self):
        payload = {
            "client_id": "",
            "client_secret": "",
            "grant_type": "",
            "scope": ""
        }
        url = f"suaurl/api/oauth/token"
        r = requests.post(url, data=payload,verify=False)
        obj = json.loads(r.text)
        self.token = obj["access_token"]
        return self.token
    
    def obter_detalhes_pix(self):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        url = f"suaurl/{self.txid}"
        print(f"🔍 Chamando API do Pix: {url}")
        res = requests.get(url, headers=header, verify=False)
        response = res.json()

        if "pix" in response and len(response["pix"]) >0:
            detalhes_pix = {
                "end_to_end": response["pix"][0]["endToEndId"],
                "valor": response["pix"][0]["valor"],
            }
            return detalhes_pix
        else:
            return None
