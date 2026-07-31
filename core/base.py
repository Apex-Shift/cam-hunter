class BaseModule:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.type = ""  # "scan" ou "attack"
        self.options = {}  # Paramètres requis (ex: TARGET_IP, PORT)

    async def run(self):
        raise NotImplementedError("Chaque module doit définir sa méthode run().")
