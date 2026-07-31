import sys
import asyncio
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QTableWidget, QTableWidgetItem, QLineEdit,
    QPushButton, QTextEdit, QLabel, QSplitter, QHeaderView
)
from PySide6.QtCore import Qt, QThread, Signal
from core.loader import ModuleLoader

class ExploitWorker(QThread):
    """
    Worker thread to execute asynchronous modules without freezing the GUI.
    """
    result_signal = Signal(dict)
    log_signal = Signal(str)

    def __init__(self, module, target, options):
        super().__init__()
        self.module = module
        self.target = target
        self.options = options

    def run(self):
        # Dynamically map the configured GUI values back to the module instance
        for key, val in self.options.items():
            if key in self.module.options:
                self.module.options[key]["value"] = val

        self.log_signal.emit(f"[*] Initializing execution loop for module: {self.module.name} against {self.target}...")
        
        # Instantiate a dedicated event loop for the background QThread execution
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(self.module.run())
            self.result_signal.emit({"status": "success", "data": result})
        except Exception as e:
            self.result_signal.emit({"status": "error", "message": str(e)})
        finally:
            loop.close()

class CamHunterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📡 CAM HUNTER // Enterprise IoT Auditing Suite")
        self.setGeometry(100, 100, 1100, 700)
        
        # Load the operational modules core registry
        self.loader = ModuleLoader()
        self.modules_registry = self.loader.load_modules()
        
        self.current_module = None
        self.init_ui()
        self.apply_dark_theme()

    def init_ui(self):
        # Absolute root container setup
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Dynamic structural windows splitter
        splitter = QSplitter(Qt.Horizontal)

                # ---------------- LEFT SIDEBAR PANEL (Modules list with Search) ----------------
        sidebar_widget = QWidget()
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)

        sidebar_label = QLabel("🎯 REPOSITORY MODULES")
        sidebar_label.setAlignment(Qt.AlignCenter)
        
        # New real-time search input bar
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("🔍 Search module (e.g., dahua, cve)...")
        self.search_input.textChanged.connect(self.filter_modules)  # Connected to the instant filter logic

        self.module_list = QListWidget()
        
        # Auto-populate the sidebar from the dynamic core loader engine registry
        self.populate_module_list()
        self.module_list.itemClicked.connect(self.on_module_selected)

        sidebar_layout.addWidget(sidebar_label)
        sidebar_layout.addWidget(self.search_input)  # Inject the search bar into the layout
        sidebar_layout.addWidget(self.module_list)
        splitter.addWidget(sidebar_widget)


        # ---------------- RIGHT CENTER PANEL (Workspace grid) ----------------
        workspace_widget = QWidget()
        self.workspace_layout = QVBoxLayout(workspace_widget)
        self.workspace_layout.setContentsMargins(10, 0, 0, 0)

        self.module_title = QLabel("Select an automated target vector from the sidebar panel.")
        self.module_title.setWordWrap(True)
        self.module_title.setObjectName("ModuleTitle")

        # Table configuration mapping setup grid parameters
        self.options_table = QTableWidget()
        self.options_table.setColumnCount(3)
        self.options_table.setHorizontalHeaderLabels(["Variable Input Key", "Configured Value", "Required Status"])
        self.options_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.options_table.verticalHeader().setVisible(False)

        # Action execution control buttons
        self.fire_button = QPushButton("🚀 FIRE OFFENSIVE EXPLOIT LOOP")
        self.fire_button.setEnabled(False)
        self.fire_button.clicked.connect(self.on_fire_exploit)

        # Lower historical runtime console windows logger panel
        console_label = QLabel("📟 LIVE SYSTEM OPERATIONAL LOGS")
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setPlaceholderText("Execution log monitoring stream matrix...")

        self.workspace_layout.addWidget(self.module_title)
        self.workspace_layout.addWidget(self.options_table)
        self.workspace_layout.addWidget(self.fire_button)
        self.workspace_layout.addWidget(console_label)
        self.workspace_layout.addWidget(self.console_output)
        
        splitter.addWidget(workspace_widget)
        splitter.setSizes([300, 800]) # Lock comfortable default side grid geometry aspect ratios

        main_layout.addWidget(splitter)
        self.setCentralWidget(main_widget)

    def apply_dark_theme(self):
        """
        Applies a stylized Cyberpunk Dark/Neon UI palette context across window elements.
        """
        self.setStyleSheet("""
            QMainWindow, QWidget {
                background-color: #0b0f19;
                color: #f5f6fa;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLabel {
                font-weight: bold;
                color: #9ca3af;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                font-size: 11px;
                margin-bottom: 4px;
            }
            QLabel#ModuleTitle {
                font-size: 16px;
                color: #38bdf8;
                border-bottom: 2px solid #1f2937;
                padding-bottom: 8px;
                margin-bottom: 12px;
            }
            QListWidget {
                background-color: #111827;
                border: 1px solid #1f2937;
                border-radius: 6px;
                padding: 5px;
                color: #e5e7eb;
            }
            QListWidget::item {
                padding: 8px;
                border-radius: 4px;
            }
            QListWidget::item:hover {
                background-color: #1f2937;
                color: #38bdf8;
            }
            QListWidget::item:selected {
                background-color: #0369a1;
                color: #ffffff;
                font-weight: bold;
            }
            QTableWidget {
                background-color: #111827;
                border: 1px solid #1f2937;
                gridline-color: #1f2937;
                border-radius: 6px;
                color: #ffffff;
            }
            QHeaderView::section {
                background-color: #1f2937;
                color: #9ca3af;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #111827;
                font-size: 11px;
            }
            QLineEdit {
                background-color: #1f2937;
                color: #ffffff;
                border: 1px solid #374151;
                border-radius: 4px;
                padding: 4px;
            }
            QLineEdit:focus {
                border: 1px solid #38bdf8;
            }
            QPushButton {
                background-color: #f43f5e;
                color: #ffffff;
                font-weight: bold;
                border: none;
                border-radius: 6px;
                padding: 12px;
                font-size: 13px;
                margin-top: 8px;
                margin-bottom: 15px;
            }
            QPushButton:hover {
                background-color: #e11d48;
            }
            QPushButton:disabled {
                background-color: #374151;
                color: #9ca3af;
            }
            QTextEdit {
                background-color: #030712;
                border: 1px solid #1f2937;
                border-radius: 6px;
                font-family: 'Consolas', 'Courier New', monospace;
                font-size: 12px;
                color: #00ff66;
                padding: 8px;
            }
        """)
    def on_module_selected(self, item):
        """
        Triggered when a module is selected in the sidebar list.
        Dynamically populates the option input fields grid.
        """
        mod_name = item.text()
        self.current_module = self.modules_registry[mod_name]
        
        # Display the formatted target details header
        self.module_title.setText(f"🚀 ACTIVE PAYLOAD: {self.current_module.name}\n📋 DESC: {self.current_module.description}")
        
        # Clear previous rows layout configuration
        self.options_table.setRowCount(0)
        self.options_table.setRowCount(len(self.current_module.options))
        
        # Build the dynamic inputs rows
        for row_idx, (opt_name, opt_data) in enumerate(self.current_module.options.items()):
            # Column 0: Variable Key name string
            key_item = QTableWidgetItem(opt_name)
            key_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.options_table.setItem(row_idx, 0, key_item)
            
            # Column 1: Editable input field text editor instance
            val_input = QLineEdit()
            val_input.setText(str(opt_data.get("value", "")))
            # Store the configuration option token key inside the dynamic widget object data
            val_input.setProperty("opt_name", opt_name)
            self.options_table.setCellWidget(row_idx, 1, val_input)
            
            # Column 2: Required validation constraint indicator layout status
            req_str = "YES (Mandatory)" if opt_data.get("required") else "NO (Optional)"
            req_item = QTableWidgetItem(req_str)
            req_item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            if opt_data.get("required"):
                req_item.setForeground(Qt.red)
            self.options_table.setItem(row_idx, 2, req_item)
            
        self.fire_button.setEnabled(True)
        self.console_output.append(f"[+] Loaded workspace environment mapping for: {mod_name}")
    def populate_module_list(self, filter_text=""):
        """
        Clears and repopulates the module list widget based on search filters.
        """
        self.module_list.clear()
        for mod_name in sorted(self.modules_registry.keys()):
            # If no filter is applied, or if the keyword matches the module path/description
            if not filter_text or filter_text in mod_name.lower() or filter_text in self.modules_registry[mod_name].description.lower():
                self.module_list.addItem(mod_name)

    def filter_modules(self, text):
        """
        Triggered in real-time whenever the user types into the search input bar.
        """
        cleaned_search_text = text.strip().lower()
        self.populate_module_list(cleaned_search_text)


    def on_fire_exploit(self):
        """
        Validates missing structural variables and handles safe background worker executions.
        """
        if not self.current_module:
            return
            
        # Parse current active text input fields state data back to options dictionaries
        extracted_options = {}
        target_host = "Unknown Target"
        
        for row in range(self.options_table.rowCount()):
            cell_widget = self.options_table.cellWidget(row, 1)
            if isinstance(cell_widget, QLineEdit):
                opt_name = cell_widget.property("opt_name")
                opt_value = cell_widget.text().strip()
                extracted_options[opt_name] = opt_value
                if opt_name == "TARGET":
                    target_host = opt_value

        # Enforce validation checks array over mandatory keys before spawning processes
        missing_keys = []
        for key, data in self.current_module.options.items():
            current_value = extracted_options.get(key, "")
            if data.get("required") and not current_value:
                missing_keys.append(key)
                
        if missing_keys:
            self.console_output.append(f"[\033[1;31m!\033[0m] CRITICAL: Execution blocked. Missing required inputs: {', '.join(missing_keys)}")
            return

        # Neutralize interface triggers during active transaction loops
        self.fire_button.setEnabled(False)
        self.module_list.setEnabled(False)
        
        # Initialize the secure background worker task routine
        self.worker = ExploitWorker(self.current_module, target_host, extracted_options)
        self.worker.log_signal.connect(self.update_console_logs)
        self.worker.result_signal.connect(self.on_execution_finished)
        self.worker.start()

    def update_console_logs(self, message):
        """Adds live system operational logging outputs to the lower console container view."""
        self.console_output.append(message)

    def on_execution_finished(self, response):
        """
        Parses asynchronous callback logs and handles application structural release locks.
        """
        # Unlock control mechanisms back to standard state array maps
        self.fire_button.setEnabled(True)
        self.module_list.setEnabled(True)
        
        if response.get("status") == "success":
            data_payload = response.get("data")
            self.console_output.append(f"[+] EXPLOIT LOOP TERMINATED SUCCESSFUL!")
            self.console_output.append(f"[Payload Output Data]:\n{data_payload}\n")
            
            # Re-verify and auto-save successful leaks history using standard engine mechanisms
            if isinstance(data_payload, dict) and (data_payload.get("vulnerable") or data_payload.get("success")):
                # Refresh local html log ledgers files dynamically if imported
                try:
                    from main import save_result_to_log
                    target_ip = self.current_module.options.get("TARGET", {}).get("value", "0.0.0.0")
                    save_result_to_log(self.current_module.name, target_ip, data_payload)
                except ImportError:
                    pass
        else:
            self.console_output.append(f"[!] SYSTEM EXECUTION ERROR: {response.get('message')}\n")

if __name__ == "__main__":
    # Create the top-level QApplication infrastructure application mapping
    app = QApplication(sys.argv)
    window = CamHunterGUI()
    window.show()
    sys.exit(app.exec())
