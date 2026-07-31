import asyncio
import ipaddress
from core.base import BaseModule

class Module(BaseModule):
    def __init__(self):
        super().__init__()
        self.name = "recon/subnet_tcp_sweeper"
        self.description = "Fast asynchronous local network scanner targeting common IP Camera and DVR web/streaming ports."
        self.type = "recon"
        self.options = {
            "SUBNET": {"required": True, "value": "192.168.1.0/24"},
            "TIMEOUT": {"required": False, "value": "2.0"}
        }
        # Dictionnaire des ports de caméras IP / DVR ciblés pour la qualification rapide
        self.target_ports = {
            80: "HTTP Standard Web Panel",
            81: "Alternative Web/DVR Management (e.g., CVE-2018-9995)",
            8000: "Hikvision / Realtek Media Control Port",
            8554: "RTSP Smart Streaming Protocol (e.g., LSC Cam)",
            34567: "Xiongmai (XM) NetSurveillance Native Service"
        }

    async def check_host_port(self, ip, port, timeout):
        """
        Tente d'ouvrir une connexion TCP rapide sur un couple IP:Port spécifique.
        """
        try:
            # open_connection fait un TCP Handshake non bloquant
            conn = asyncio.open_connection(str(ip), port)
            reader, writer = await asyncio.wait_for(conn, timeout=timeout)
            writer.close()
            await writer.wait_closed()
            return port
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return None

    async def scan_single_host(self, ip, timeout):
        """
        Scanne tous les ports ciblés pour une seule adresse IP donnée.
        """
        active_ports = {}
        # Lancement simultané des vérifications de ports pour cette machine
        tasks = [self.check_host_port(ip, port, timeout) for port in self.target_ports.keys()]
        results = await asyncio.gather(*tasks)
        
        for port in results:
            if port:
                active_ports[port] = self.target_ports[port]
        return ip, active_ports

    async def run(self):
        subnet_str = self.options["SUBNET"]["value"]
        timeout = float(self.options["TIMEOUT"]["value"])
        
        print(f"\033[1;34m[*] Initializing fast asynchronous TCP sweep over subnet: {subnet_str}...\033[0m")
        print(f"[*] Targeting specific video surveillance infrastructure ports: {list(self.target_ports.keys())}\n")
        
        try:
            network = ipaddress.ip_network(subnet_str, strict=False)
        except ValueError as e:
            return {"success": False, "error": f"Invalid subnet definition format: {e}"}

        # On extrait la liste de tous les hôtes utilisables dans le sous-réseau (ex: .1 à .254)
        hosts = list(network.hosts())
        if not hosts:
            return {"success": False, "error": "No valid host addresses found in the provided network map input."}

        # ÉTAPE CLÉ : Lancement asynchrone simultané de TOUTES les IP du réseau d'un seul coup
        print(f"\033[1;33m[*] Flying tasks array across {len(hosts)} local network hosts concurrently...\033[0m")
        tasks = [self.scan_single_host(host, timeout) for host in hosts]
        
        # Attente globale de toutes les réponses (prendra au maximum le temps défini par le timeout)
        scan_results = await asyncio.gather(*tasks)
        
        discovered_devices = []
        print(f"\n\033[1;32m[+] Discovery phase completed! Live surveillance assets found:\033[0m")
        print(f"  {'IP Address':<18} | {'Open Port':<10} | {'Identified Service Context'}")
        print("  " + "-"*75)
        
        for ip, ports in scan_results:
            if ports:
                for port, desc in ports.items():
                    print(f"  {str(ip):<18} | {port:<10} | {desc}")
                    discovered_devices.append(f"{ip}:{port}")
                    
        print("  " + "-"*75)
        
        if discovered_devices:
            return {
                "success": True,
                "details": f"Local network sweep finished. Identified {len(discovered_devices)} potential video surveillance nodes.",
                "live_hosts": discovered_devices
            }
        else:
            return {"success": True, "details": "Sweep finished. No open surveillance web or video streaming ports responded on the network local segment."}
