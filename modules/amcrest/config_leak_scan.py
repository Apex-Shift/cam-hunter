import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "amcrest/config_leak_scan"
        self.description = "Unauthenticated network parameter disclosure scanner for Amcrest IP cameras (CVE-2017-3195)."
        self.type = "scan"
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
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                if response.status_code == 200 and ("table.Network" in response.text or "dhcp" in response.text.lower()):
                    return {
                        "vulnerable": True,
                        "details": "Amcrest camera is vulnerable to configuration leakage. System variables are exposed."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
