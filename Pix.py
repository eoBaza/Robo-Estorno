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
            "client_id": "96418264021802.pedrobazotti.qqpag.com.br",
            "client_secret": "2EEA1563629E7666E0632500000A912A2EEA1563629F7666E0632500000A912A2EEA156362A07666E0632500000A912A2EEA156362A17666E0632500000A912A",
            "grant_type": "client_credentials",
            "scope": "cob.read pix.write pix.read"
        }
        r = requests.post("https://pix.qqpag.com.br/api/oauth/token", data=payload,verify=False)
        obj = json.loads(r.text)
        self.token = obj["access_token"]
        return self.token
    
    def obter_detalhes_pix(self):
        header = {
            "Authorization": f"Bearer {self.token}"
        }
        url = f"https://pix.qqpag.com.br/api/v1/cob/{self.txid}"
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
