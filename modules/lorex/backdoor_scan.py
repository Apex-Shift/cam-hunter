import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "lorex/backdoor_scan"
        self.description = "Unauthenticated ORPC management interface and parameter vulnerability scanner for Lorex devices."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/orpc/Network.get"
        else:
            url = f"{target.rstrip('/')}/orpc/Network.get"
            
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                # Si le serveur renvoie un statut 200 avec une structure d'en-tête JSON valide sans redirection
                if response.status_code == 200 and ("params" in response.text or "result" in response.text):
                    return {
                        "vulnerable": True,
                        "details": "Lorex unprotected management interface identified. Endpoint is accessible without privileges."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
