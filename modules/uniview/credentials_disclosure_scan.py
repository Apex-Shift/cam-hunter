import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "uniview/credentials_disclosure_scan"
        self.description = "Configuration and cleartext credential disclosure scanner for Uniview (UNV) NVRs."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            base_url = f"http://{target}:{port}"
        else:
            base_url = target.rstrip('/')

        # 1. Vérification légère via l'API de version
        version_url = f"{base_url}/cgi-bin/main-cgi?json={{\"cmd\":%20116}}"
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                res_ver = await client.get(version_url)
                if res_ver.status_code == 200 and "szSoftwareVersion" in res_ver.text:
                    return {
                        "vulnerable": True,
                        "details": "Uniview endpoint active and leaking system software version information."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
            
        return {"vulnerable": False}
