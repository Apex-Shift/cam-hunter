import asyncio
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "xiongmai/netsurveillance_scan"
        self.description = "Unauthenticated configuration dump via raw NetSurveillance management service (Port 34567)."
        self.type = "scan"
        self.options = {
            "TARGET": {"required": True, "value": ""},
            "PORT": {"required": False, "value": "34567"}
        }

    async def run(self):
        target = self.options["TARGET"]["value"]
        port = int(self.options["PORT"]["value"])
        
        # En-tête binaire spécifique du protocole NetSurveillance pour demander la configuration système
        # Équivalent de la commande de récupération système brute
        packet = b"\xff\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x00\x00\x00\x00\x00\x00\x00"
        
        try:
            # Connexion par socket brute asynchrone (nécessaire pour les ports non-HTTP)
            reader, writer = await asyncio.open_connection(target, port)
            writer.write(packet)
            await writer.drain()
            
            data = await asyncio.wait_for(reader.read(1024), timeout=5.0)
            writer.close()
            await writer.wait_closed()
            
            # Si le protocole renvoie la signature de réponse valide contenant des structures système
            if len(data) > 0 and (b"System" in data or b"NetWork" in data or data.startswith(b"\xff\x00")):
                return {
                    "vulnerable": True,
                    "details": f"Xiongmai NetSurveillance service discovered active on port {port} and accepting raw configuration queries."
                }
        except Exception as e:
            return {"vulnerable": False, "error": str(e)}
        return {"vulnerable": False}
