import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "foscam/user_leak_scan"
        self.description = "Unauthenticated user database and account leak scanner for Foscam IP cameras."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "88"}  # Le port 88 est le port par défaut très courant chez Foscam
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/get_params.cgi"
        else:
            url = f"{target.rstrip('/')}/get_params.cgi"
            
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(url)
                # Le script get_params fuit la configuration utilisateur sous forme de variables texte brutes
                if response.status_code == 200 and ("var user1=" in response.text or "var alias=" in response.text):
                    return {
                        "vulnerable": True,
                        "details": "Foscam unauthenticated parameter leakage verified. Account list is exposed."
                    }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
