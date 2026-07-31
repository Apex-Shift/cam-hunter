import os
import importlib
import inspect
from core.base import BaseModule

class ModuleLoader:
    def __init__(self, modules_dir="modules"):
        self.modules_dir = modules_dir
        self.registry = {}

    def load_modules(self):
        """
        Parcourt récursivement le dossier des modules et charge dynamiquement
        les classes valides dérivées de BaseModule.
        """
        self.registry.clear()
        
        # On vérifie que le dossier racine existe
        if not os.path.exists(self.modules_dir):
            return self.registry

        # Parcours récursif de tous les dossiers et fichiers
        for root, _, files in os.walk(self.modules_dir):
            for file in files:
                if file.endswith(".py") and file != "__init__.py":
                    # Construction du chemin d'import en notation python (ex: modules.samsung.scan)
                    relative_path = os.path.relpath(os.path.join(root, file), start=os.getcwd())
                    module_import_path = relative_path.replace(os.path.sep, ".").rstrip(".py")
                    
                    try:
                        # Import dynamique du fichier de script
                        mod = importlib.import_module(module_import_path)
                        
                        # Recherche des classes définies à l'intérieur du fichier
                        for _, cls in inspect.getmembers(mod, inspect.isclass):
                            # On vérifie que la classe hérite de BaseModule et qu'elle n'est pas la classe abstraite parente
                            if issubclass(cls, BaseModule) and cls is not BaseModule:
                                # Instanciation du module
                                instance = cls()
                                if instance.name:
                                    self.registry[instance.name] = instance
                                    
                    except Exception as e:
                        print(f"[!] Impossible de charger le module {module_import_path}: {e}")
                        
        return self.registry
