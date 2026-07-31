import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "axis/cve_2023_21406_scan"
        self.description = "Unauthenticated information and network layout disclosure scanner for Axis IP cameras."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        # Point d'accès vulnérable dans les services de télémétrie et de statistiques bruts
        url = f"http://{target}:{port}/axis-cgi/param.cgi?action=list&group=Network"
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                # Si l'appareil fuit ses paramètres d'adressage réseau internes sans invite 401
                if response.status_code == 200 and "Network.Eth0" in response.text:
                    return {
                        "vulnerable": True,
                        "details": "Axis IP camera is vulnerable to CVE-2023-21406. System parameters are exposed."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
