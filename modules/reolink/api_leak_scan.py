import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "reolink/api_leak_scan"
        self.description = "Unauthenticated API metadata and connection parameter disclosure scanner for Reolink devices."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/cgi-bin/api.cgi?cmd=GetLocalLink"
        else:
            url = f"{target.rstrip('/')}/cgi-bin/api.cgi?cmd=GetLocalLink"
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) cam-hunter/1.0",
            "Content-Type": "application/json"
        }
        
        # Payload querying device connectivity links
        payload = [{"cmd": "GetLocalLink", "action": 0, "param": {}}]
        
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                response = await client.post(url, headers=headers, json=payload)
                
                # Reolink API typically returns an array layout containing execution responses
                if response.status_code == 200 and "value" in response.text:
                    data = response.json()
                    if isinstance(data, list) and len(data) > 0 and "value" in data[0]:
                        return {
                            "vulnerable": True,
                            "details": "Reolink unauthenticated API link exposure verified. Endpoint is fully accessible."
                        }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
            
        return {"vulnerable": False, "details": "Endpoint securely locked or non-Reolink system signatures detected."}
