import asyncio
import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "lsc/rtsp_unauth_scan"
        self.description = "Exposed RTSP unauthenticated service detector for LSC Smart Connect (CVE-2024-51362)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "8554"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = int(self.options["PORT"]["value"])
        
        try:
            # Test d'ouverture brute du port pour s'assurer que le service RTSP écoute
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(target, port), 
                timeout=4.0
            )
            writer.close()
            await writer.wait_closed()
            
            return {
                "vulnerable": True,
                "details": f"RTSP port {port} is exposed on the target. Enforce path discovery to verify stream bypass."
            }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
