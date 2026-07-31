import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "vivotek/param_disclosure_scan"
        self.description = "Unauthenticated information and system configuration disclosure scanner for Vivotek IP cameras."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/cgi-bin/viewer/getparam.cgi"
        else:
            url = f"{target.rstrip('/')}/cgi-bin/viewer/getparam.cgi"
            
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                
                # Le fichier getparam.cgi de Vivotek liste les variables d'environnement système
                if response.status_code == 200 and ("system." in response.text or "network." in response.text):
                    return {
                        "vulnerable": True,
                        "details": "Vivotek configuration bypass verified. The parameter dump script is publicly exposed."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
