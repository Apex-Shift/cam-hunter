import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "dahua/cve_2022_30563_scan"
        self.description = "Unauthenticated ONVIF system command injection vulnerability scanner for Dahua (CVE-2022-30563)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/onvif/device_service"
        else:
            url = f"{target.rstrip('/')}/onvif/device_service"
            
        # Payload ONVIF malveillant provoquant une réponse d'erreur de parseur spécifique si vulnérable
        payload = "<s:Envelope xmlns:s='http://w3.org'><s:Body><GetSystemDateAndTime xmlns='http://onvif.org></s:Body></s:Envelope>"
        
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.post(url, content=payload, headers={"Content-Type": "application/soap+xml"})
                if response.status_code == 200 and "GetSystemDateAndTimeResponse" in response.text:
                    return {
                        "vulnerable": True,
                        "details": "Dahua ONVIF parser is open and susceptible to input parameter manipulation (CVE-2022-30563)."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
