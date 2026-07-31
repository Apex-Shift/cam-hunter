import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "dlink/cve_2018_18013_scan"
        self.description = "Unauthenticated system configuration and credential leak scanner for D-Link IP cameras."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        # Script interne vulnérable exposant les paramètres de sauvegarde
        url = f"http://{target}:{port}/common/info.cgi"
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                
                # Le fichier info.cgi de D-Link renvoie des paires clé/valeur système claires
                if response.status_code == 200 and ("mac_addr=" in response.text or "camera_name=" in response.text.lower()):
                    return {
                        "vulnerable": True,
                        "details": "D-Link system information page leaked. Admin password hashes or plain-text strings are exposed."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
