import asyncio
import sys
import os
import shlex
import threading
import tempfile
from html import escape

# Define the local command history log location
HISTORY_FILE = os.path.expanduser("~/.cam_hunter_history")

# Initialize robust terminal input history and auto-complete configurations
try:
    import readline
    if os.path.exists(HISTORY_FILE):
        try:
            readline.read_history_file(HISTORY_FILE)
        except Exception:
            pass
except ImportError:
    try:
        import pyreadline3 as readline
        if os.path.exists(HISTORY_FILE):
            try:
                readline.read_history_file(HISTORY_FILE)
            except Exception:
                pass
    except ImportError:
        readline = None

from core.loader import ModuleLoader


def save_terminal_history():
    """
    Saves the user command shell history persistently across console sessions.
    """
    if readline:
        try:
            readline.write_history_file(HISTORY_FILE)
        except Exception:
            pass


def print_banner(modules_count):
    """
    Renders the modern stylized CAM HUNTER application banner layout.
    """
    print("\033[1;34m" + "="*57 + "\033[0m")
    print("\033[1;36m   ____    _    _  _   _   _ _   _ _   _ _____ _____ ____  ")
    print("  / ___|  / \\  | \\| | | | | | | | \\ | |_   _| ____|  _ \\ ")
    print(" | |     / _ \\ | . ` | | |_| | | | |  \\| | | | |  _| | |_) |")
    print(" | |___ / ___ \\| |\\  | |  _  | |_| | |\\  | | | | |___|  _ < ")
    print("  \\____/_/   \\_\\_| \\_| |_| |_|\\___/|_| \\_| |_| |_____|_| \\_\\ \033[0m")
    print(f"         DVR / NVR / XVR Security Testing Framework")
    print(f"         [{modules_count} modules loaded dynamically]")
    print("\033[1;34m" + "="*57 + "\033[0m")
    print("\033[1;33m -> Type 'help' or 'h' to review advanced power shortcuts.\033[0m\n")


def print_help_menu():
    """
    Displays the contextual refactored elite navigation instructions matrix.
    """
    print("\n\033[1;36m=== AVAILABLE CORE INSTRUCTIONS MATRIX ===\033[0m")
    print("  \033[1;32mhelp\033[0m, \033[1;32mh\033[0m                   Display this advanced shortcuts reference panel.")
    print("  \033[1;32mshow modules\033[0m, \033[1;32mlm\033[0m          [List Modules] Enumerate loaded testing assets.")
    print("  \033[1;32mshow options\033[0m, \033[1;32mlo\033[0m, \033[1;32moptions\033[0m [List Options] Review targeting workspace parameters.")
    print("  \033[1;32msearch <key>\033[0m              Filter registry by vendor brand name or CVE ID.")
    print("  \033[1;32muse <path>\033[0m                Initialize an operational testing script.")
    print("  \033[1;32mset <KEY>=<val>\033[0m           Bind values (Supports spaces and optional '=' format).")
    print("  \033[1;32mrun\033[0m, \033[1;32mexploit\033[0m, \033[1;32mx\033[0m           [Execute] Fire active module offensive payload chains.")
    print("  \033[1;32mvulnscan <IP>\033[0m, \033[1;32mvs <IP>\033[0m    [Global Scan] Cycle ALL vendor verifiers sequentially.")
    print("  \033[1;32mback\033[0m                      Unload active context and return to absolute root prompt.")
    print("  \033[1;32mexit\033[0m                      Terminate framework runtime execution loops safely.")
    print("\033[1;35m* SHORTCUTS NOTE: Press [TAB] to trigger dynamic auto-completion suggestions anytime.\033[0m\n")


def generate_html_report():
    """
    Generates a web-based interactive HTML status dashboard with visual statistics counters.
    """
    txt_file = "reports/vulnerabilities.txt"
    html_file = "reports/dashboard.html"
    
    if not os.path.exists(txt_file):
        return

    table_rows = ""
    unique_targets = set()
    unique_modules = set()
    total_success = 0

    try:
        with open(txt_file, "r", encoding="utf-8") as f:
            for line in f:
                if "TARGET:" in line and "STATUS:" in line:
                    parts = line.strip().split(" | ")
                    if len(parts) < 4:
                        continue
                    mod_part_raw = parts[0].replace("[", "").replace("]", "")
                    target_part_raw = parts[1].replace("TARGET: ", "")
                    status_part_raw = parts[2].replace("STATUS: ", "")
                    details_part_raw = parts[3].replace("DETAILS: ", "")
                    
                    # Track unique counts using raw values
                    unique_targets.add(target_part_raw)
                    unique_modules.add(mod_part_raw)
                    total_success += 1

                    # Escape values before embedding into HTML to avoid XSS
                    mod_part = escape(mod_part_raw)
                    target_part = escape(target_part_raw)
                    status_part = escape(status_part_raw)
                    details_part = escape(details_part_raw)
                    
                    badge_color = "#00ff66" if status_part_raw == "SUCCESS" else "#ff3333"
                    
                    table_rows += f"""
                    <tr>
                        <td style="color: #36d1dc; font-weight: bold;">{mod_part}</td>
                        <td style="color: #ffffff;">{target_part}</td>
                        <td><span style="background: {badge_color}; color: #000; padding: 2px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;">{status_part}</span></td>
                        <td style="color: #cccccc; max-width: 400px; word-wrap: break-word;">{details_part}</td>
                    </tr>
                    """
    except Exception as e:
        print(f"[-] Log reading failure: {e}")
        return

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Cam Hunter - Operational Dashboard</title>
    <style>
        body {{ background-color: #0b0f19; color: #f5f6fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 30px; }}
        h1 {{ color: #00ff66; border-bottom: 2px solid #1e272c; padding-bottom: 10px; font-size: 28px; margin-bottom: 5px; }}
        .subtitle {{ color: #8a99ad; margin-bottom: 30px; font-size: 14px; }}
        .stats-container {{ display: flex; gap: 20px; margin-bottom: 30px; }}
        .stat-card {{ background: #111827; border: 1px solid #1f2937; border-radius: 6px; padding: 15px 25px; flex: 1; box-shadow: 0 4px 6px rgba(0,0,0,0.2); }}
        .stat-val {{ font-size: 24px; font-weight: bold; color: #00ff66; margin-top: 5px; }}
        .stat-lbl {{ font-size: 12px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; }}
        table {{ width: 100%; border-collapse: collapse; background-color: #111827; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }}
        th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #1f2937; }}
        th {{ background-color: #1f2937; color: #9ca3af; text-transform: uppercase; font-size: 12px; letter-spacing: 0.5px; }}
        tr:hover {{ background-color: #1e293b; }}
    </style>
</head>
<body>
    <h1>📡 CAM HUNTER // Exploitation Dashboard</h1>
    <div class="subtitle">Automated historical ledger for audited and compromised IoT network assets</div>
    <div class="stats-container">
        <div class="stat-card">
            <div class="stat-lbl">Total Successful Exploits</div>
            <div class="stat-val" style="color: #38bdf8;">{total_success}</div>
        </div>
        <div class="stat-card">
            <div class="stat-lbl">Unique Targets Compromised</div>
            <div class="stat-val" style="color: #a855f7;">{len(unique_targets)}</div>
        </div>
        <div class="stat-card">
            <div class="stat-lbl">Active Attack Vectors Used</div>
            <div class="stat-val" style="color: #f43f5e;">{len(unique_modules)}</div>
        </div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Module</th>
                <th>Target Host</th>
                <th>Execution Status</th>
                <th>Extracted Metadata / Findings Payload</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</body>
</html>
"""
    try:
        # Ensure reports directory exists
        os.makedirs(os.path.dirname(html_file), exist_ok=True)
        # Atomic write to avoid partial writes / corruption
        dir_name = os.path.dirname(html_file) or '.'
        fd, tmp_path = tempfile.mkstemp(dir=dir_name, prefix="dashboard-", suffix=".html")
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as tmpf:
                tmpf.write(html_template)
            os.replace(tmp_path, html_file)
        finally:
            # If tmp_path still exists (on error), attempt to remove
            if os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
    except Exception as e:
        print(f"[-] Dashboard write failure: {e}")


def save_result_to_log(module_name, target, result):
    """
    Automatically tracks critical discoveries and refreshes the live HTML dashboard view.
    """
    os.makedirs("reports", exist_ok=True)
    log_file = "reports/vulnerabilities.txt"
    
    is_vuln = isinstance(result, dict) and (result.get("vulnerable") or result.get("success"))
    
    if is_vuln:
        details = str(result.get("details", "")).replace("\n", " ")
        # Append structured line to the log file
        try:
            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"[{module_name.upper()}] | TARGET: {target} | STATUS: SUCCESS | DETAILS: {details}\n")
        except Exception as e:
            print(f"[-] Failed to write vulnerability log: {e}")
            return

        print(f"\033[1;33m[+] Finding logged. HTML Dashboard refreshed inside 'reports/dashboard.html'\033[0m")
        # Refresh dashboard in background to avoid blocking CLI
        try:
            t = threading.Thread(target=generate_html_report, daemon=True)
            t.start()
        except Exception as e:
            print(f"[-] Failed to spawn dashboard update thread: {e}")

class Completer:
    """
    Custom TAB-completion management engine matching core instructions and internal modules registry.
    """
    def __init__(self, commands, modules):
        self.commands = commands
        self.modules = list(modules.keys())

    def complete(self, text, state):
        buffer = readline.get_line_buffer()
        words = buffer.strip().split()
        
        if not words:
            options = self.commands
        elif words[0].lower() in ["use", "search"] and len(words) <= 2:
            token = words[1] if len(words) == 2 else ""
            options = [m for m in self.modules if m.startswith(token)]
        else:
            token = text.lower()
            options = [c for c in self.commands if c.startswith(token)]

        try:
            return options[state] + " "
        except IndexError:
            return None


async def run_global_vulnscan(modules_registry, target, port_fallback="80"):
    """
    Global pipeline loop: Executes all scanning modules sequentially against a target host.
    """
    print(f"\n\033[1;35m[!] TRIGGERING GLOBAL AUTOMATED VULNERABILITY CYCLES AGAINST {target} [!]\033[0m")
    print("\033[1;34m" + "-"*57 + "\033[0m")
    
    scan_modules = {name: mod for name, mod in modules_registry.items() if mod.type == "scan"}
    vulnerabilities_detected = 0

    for name, module in scan_modules.items():
        print(f"\033[1;34m[*] Running verification script: {name}...\033[0m")
        module.options["TARGET"]["value"] = target
        if "PORT" in module.options:
            if not module.options["PORT"]["value"]:
                module.options["PORT"]["value"] = port_fallback

        try:
            # Consider adding asyncio.wait_for(module.run(), timeout=...) in future
            result = await module.run()
            if isinstance(result, dict) and result.get("vulnerable"):
                print(f"  \033[1;31m[VULNERABLE] -> {result.get('details', 'Vulnerability signature confirmed.')}\033[0m")
                save_result_to_log(name, target, result)
                vulnerabilities_detected += 1
            else:
                print("  \033[1;32m[SAFE] Asset not vulnerable or patched.\033[0m")
        except Exception as e:
            print(f"  \033[1;31m[MODULE ERROR] : {e}\033[0m")
            
    print("\033[1;34m" + "-"*57 + "\033[0m")
    print(f"\033[1;35m[+] GLOBAL CYCLES TERMINATED. Total vulnerabilities flagged: {vulnerabilities_detected}\033[0m\n")


async def cli():
    loader = ModuleLoader()
    modules_registry = loader.load_modules()
    
    print_banner(len(modules_registry))
    current_module = None

    # Supported system command instructions list
    commands = ["show", "search", "use", "set", "run", "exploit", "vulnscan", "vs", "lm", "lo", "options", "x", "back", "help", "h", "exit"]
    if readline:
        completer = Completer(commands, modules_registry)
        readline.set_completer(completer.complete)
        readline.parse_and_bind("tab: complete")

    while True:
        try:
            # Dynamic prompt tracking context adjustments
            module_name = current_module.name if current_module else "none"
            prompt = f"\033[1;31mcam-hunter\033[0m(\033[1;33m{module_name}\033[0m) > "
            
            user_input_raw = input(prompt).strip()
            if not user_input_raw:
                continue

            # Use shlex.split to respect quoted arguments
            try:
                cmd = shlex.split(user_input_raw)
            except Exception:
                # Fall back to simple split on error
                cmd = user_input_raw.split()

            action = cmd[0].lower()

            # Global command check: EXIT
            if action == "exit":
                print("\033[1;32m[+] Shutting down the framework workspace. Saving history logs... Goodbye!\033[0m")
                save_terminal_history()
                sys.exit(0)

            # Global command check: BACK (Unloads active script context)
            elif action == "back":
                if current_module:
                    print(f"[*] Unloaded active module workspace: {current_module.name}")
                    current_module = None
                else:
                    print("\033[1;31m[!] Already at the core root framework environment level.\033[0m")

            # Global command check: HELP / H
            elif action in ["help", "h"]:
                print_help_menu()

            # Global command check: VULNSCAN / VS
            elif action in ["vulnscan", "vs"]:
                if len(cmd) > 1:
                    target_ip = cmd[1]
                    fallback_port = cmd[2] if len(cmd) > 2 else "80"
                    await run_global_vulnscan(modules_registry, target_ip, fallback_port)
                else:
                    print("\033[1;31m[!] Syntax error : vulnscan/vs <TARGET_IP> [FALLBACK_PORT]\033[0m")

            # Global command check: SEARCH
            elif action == "search":
                if len(cmd) > 1:
                    keyword = cmd[1].lower()
                    print(f"\n=== Search results registry for query: '{keyword}' ===")
                    found = False
                    for name, mod in modules_registry.items():
                        if keyword in name.lower() or keyword in mod.description.lower():
                            print(f"  \033[1;32m{name:<30}\033[0m [{mod.type.upper()}] - {mod.description}")
                            found = True
                    if not found:
                        print("  No internal modules matched your keyword context descriptor.")
                    print("")
                else:
                    print("\033[1;31m[!] Syntax error : search <keyword>\033[0m")

            # Global command check: SHOW MODULES / LM (List Modules)
            elif action == "lm" or (action == "show" and len(cmd) > 1 and cmd[1].lower() == "modules"):
                print("\n=== Active Modules Registry ===")
                for name, mod in modules_registry.items():
                    print(f"  \033[1;32m{name:<30}\033[0m [{mod.type.upper()}] - {mod.description}")
                print("")

            # Global command check: SHOW OPTIONS / LO / OPTIONS (List Options)
            elif action in ["lo", "options"] or (action == "show" and len(cmd) > 1 and cmd[1].lower() == "options"):
                if current_module:
                    print(f"\nOptions dataset for module scope '{current_module.name}':")
                    print(f"  {'Option':<15} {'Value':<25} {'Required':<10}")
                    print("  " + "-"*50)
                    for opt, data in current_module.options.items():
                        val = data['value'] if data['value'] else "Not configured"
                        req = "Yes" if data['required'] else "No"
                        print(f"  {opt:<15} {val:<25} {req:<10}")
                    print("")
                else:
                    print("\033[1;31m[!] Operational context missing. Please allocate a target runtime workspace via 'use <module>'.\033[0m")

            # Global command check: USE
            elif action == "use":
                if len(cmd) > 1:
                    target_module = cmd[1]
                    if target_module in modules_registry:
                        current_module = modules_registry[target_module]
                    else:
                        print(f"\033[1;31m[!] Target script module path '{target_module}' could not be loaded.\033[0m")
                else:
                    print("\033[1;31m[!] Syntax error : use <module_path>\033[0m")

            # Global command check: SET (Intelligent variable parsing with or without '=')
            elif action == "set":
                if current_module:
                    # Clean user input to standardize format variations (supports space or equal sign)
                    raw_argument = " ".join(cmd[1:])
                    if "=" in raw_argument:
                        opt_name, opt_value = raw_argument.split("=", 1)
                    else:
                        argument_parts = raw_argument.split(" ", 1)
                        opt_name = argument_parts[0]
                        opt_value = argument_parts[1] if len(argument_parts) > 1 else ""

                    opt_name = opt_name.strip().upper()
                    opt_value = opt_value.strip()

                    if opt_name in current_module.options:
                        current_module.options[opt_name]["value"] = opt_value
                        print(f"\033[1;32m[+] {opt_name} => {opt_value}\033[0m")
                    else:
                        print(f"\033[1;31m[!] Target variable option structural key '{opt_name}' is invalid.\033[0m")
                else:
                    print("\033[1;31m[!] Operational context missing. Please allocate a target runtime workspace via 'use <module>'.\033[0m")

            # Global command check: RUN / EXPLOIT / X
            elif action in ["run", "exploit", "x"]:
                if current_module:
                    missing = [opt for opt, data in current_module.options.items() if data['required'] and not data['value']]
                    if missing:
                        print(f"\033[1;31m[!] Mandatory input variables requirements missing : {', '.join(missing)}\033[0m")
                        continue
                    
                    target_ip = current_module.options["TARGET"]["value"]
                    print(f"\033[1;34m[*] Executing automated offensive loops {current_module.name} tracking host {target_ip}...\033[0m")
                    
                    # Execute the selected module asynchronously
                    result = await current_module.run()
                    print(f"  \033[1;32m[Execution payload returned result] {result}\033[0m")
                    
                    # Save results to flat-file database and refresh the dashboard layout
                    save_result_to_log(current_module.name, target_ip, result)
                    print("")
                else:
                    print("\033[1;31m[!] Operational environment missing. Cannot compute execution context arrays.\033[0m")

            else:
                print(f"\033[1;31m[!] Runtime command parser mismatch: '{action}'. Input 'help' to review instructions.\033[0m")

        except KeyboardInterrupt:
            print("\n\033[1;33m[*] Interruption request parsed. Standard input aborted. Type 'exit' to terminate.\033[0m")
        except Exception as e:
            print(f"\033[1;31m[!] Framework core exception thrown : {e}\033[0m")


if __name__ == "__main__":
    asyncio.run(cli())
