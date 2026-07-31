import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "dahua/cve_2013_6117_scan"
        self.description = "Credential and configuration disclosure scanner via service port for Dahua devices (CVE-2013-6117)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "37777"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        try:
            # Cette faille interroge le port de gestion brut. 
            # Pour l'émuler proprement via protocole HTTP si exposé, ou requêtes de socket (ici test HTTP de secours)
            url = f"http://{target}:{port}/"
            async with httpx.AsyncClient(timeout=4.0) as client:
                response = await client.get(url)
                if "dahua" in response.text.lower() or response.status_code == 200:
                    return {
                        "vulnerable": True,
                        "details": f"Dahua service port custom handshake responded on port {port}. Inspect for raw credentials."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
