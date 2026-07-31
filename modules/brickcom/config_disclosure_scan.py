import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "brickcom/config_disclosure_scan"
        self.description = "Unauthenticated configuration dump disclosure scanner for Brickcom IP cameras."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/configfile.dump?action=get"
        else:
            url = f"{target.rstrip('/')}/configfile.dump?action=get"
            
        try:
            # On utilise une requête HEAD ou un timeout court pour ne pas saturer la bande passante avec le fichier complet
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                
                # Le fichier dump de Brickcom contient généralement des signatures de variables système explicites
                if response.status_code == 200 and ("UserSetSetting" in response.text or "SystemSetting" in response.text):
                    return {
                        "vulnerable": True,
                        "details": "Brickcom camera configuration file endpoint is fully accessible without authentication."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
            
        return {"vulnerable": False}
