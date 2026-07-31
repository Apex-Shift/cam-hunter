import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "netgear/arlo_leak_scan"
        self.description = "Unauthenticated diagnostic and token data disclosure scanner for Netgear Arlo base stations."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/debug/display_info.txt"
        else:
            url = f"{target.rstrip('/')}/debug/display_info.txt"
            
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                if response.status_code == 200 and ("serial" in response.text or "token" in response.text.lower()):
                    return {
                        "vulnerable": True,
                        "details": "Netgear Arlo base station allows unauthenticated read-access to diagnostic environment metrics."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
