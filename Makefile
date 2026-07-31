# --- Configuration des variables globales ---
PYTHON   = python
PIP      = pip
MAIN_SRC = main.py
REQ_FILE = requirements.txt
LOG_DIR  = reports

# --- Cibles principales ---

.PHONY: help install run clean clear-logs

help:
	@echo "======================================================="
	@echo "              CAM HUNTER - MAKEFILE ENGINE             "
	@echo "======================================================="
	@echo "Commandes disponibles :"
	@echo "  make install    - Installe proprement toutes les dépendances"
	@echo "  make run        - Lance le framework interactif Cam Hunter"
	@echo "  make clean      - Supprime les caches temporaires Python (__pycache__)"
	@echo "  make clear-logs - Réinitialise l'historique et le tableau de bord HTML"
	@echo "======================================================="

install:
	@echo "[*] Installation des dépendances depuis $(REQ_FILE)..."
	$(PIP) install -r $(REQ_FILE)
	@echo "[+] Installation terminée avec succès."

run:
	@echo "[*] Initialisation du framework de test Cam Hunter..."
	$(PYTHON) $(MAIN_SRC)

clean:
	@echo "[*] Nettoyage des fichiers de cache Python..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	@echo "[+] Caches nettoyés."

clear-logs:
	@echo "[*] Suppression des fichiers d'historique de rapports..."
	rm -rf $(LOG_DIR)
	@echo "[+] Dossier $(LOG_DIR)/ supprimé. Prêt pour une nouvelle session."

gui:
	@echo "[*] Launching Cam Hunter PySide6 Cyberpunk Graphical Workspace..."
	$(PYTHON) gui_main.py

