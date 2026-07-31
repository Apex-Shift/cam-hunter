import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "bosch/rcp_leak_scan"
        self.description = "Unauthenticated RCP.xml system metadata parameter disclosure scanner for Bosch IP cameras."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/rcp.xml?cmd=0x09a5"
        else:
            url = f"{target.rstrip('/')}/rcp.xml?cmd=0x09a5"
            
        try:
            async with httpx.AsyncClient(timeout=5.0, verify=False) as client:
                response = await client.get(url)
                # Si l'endpoint renvoie une structure de configuration RCP XML Bosch valide
                if response.status_code == 200 and ("<rcp" in response.text or "hex" in response.text.lower()):
                    return {
                        "vulnerable": True,
                        "details": "Bosch RCP parameter bypass verified. Internal system logs/configurations are exposed."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
