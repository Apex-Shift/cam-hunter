import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "linksys/ping_rce_scan"
        self.description = "Unauthenticated ping utility command injection vulnerability scanner for Linksys devices."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/ping.cgi"
        else:
            url = f"{target.rstrip('/')}/ping.cgi"
            
        try:
            # Envoi d'un payload léger d'interrogation
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(url, data={"ping_ip": "127.0.0.1"})
                # Si le script de ping répond publiquement sans demander de session active
                if response.status_code == 200 and ("ping" in response.text or "bytes from" in response.text.lower()):
                    return {
                        "vulnerable": True,
                        "details": "Linksys ping diagnostics endpoint is publicly exposed and vulnerable to manipulation."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
