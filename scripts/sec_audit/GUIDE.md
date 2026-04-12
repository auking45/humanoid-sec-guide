# Humanoid Security Auditor (`humanoid_sec_auditor.py`)

This script is an automated tool designed to verify if the robot's current system state complies with the **'Humanoid-Specific Security Requirements'**.
It is built with a plugin-based architecture, allowing you to easily add new audit checks without modifying the main source code.

## Key Features

- **Plugin Architecture**: Dynamically loads audit modules from the `checks/` directory.
- **Multilingual Support (i18n)**: Supports English (`en`) and Korean (`ko`) for terminal output and report generation (utilizing `messages.json`).
- **Multiple Output Formats**: Supports JSON output for CI/CD integration and Markdown reports for human-readable visibility.

## Prerequisites

- **Execution Environment**: This script must be **copied to and executed directly on the target robot device** (e.g., x86 or NVIDIA board), not from an external host PC.
- Python 3.6 or higher
- Root or `sudo` privileges (required to inspect certain security configurations and system daemons).

## Usage

You can easily deploy the entire toolset to the robot device and fetch the results later using the provided `audit_manager.sh` helper script.

```bash
# 1. Deploy the scripts to the robot (Default path: ~/humanoid_sec_audit)
chmod +x audit_manager.sh
./audit_manager.sh deploy robot_user@192.168.1.100
```

Once deployed, SSH into the robot and run the audit.

```bash
ssh robot_user@192.168.1.100
cd ~/humanoid_sec_audit
```

By default, the script outputs the audit results to the terminal in Korean (`ko`).

```bash
# Run basic audit (Terminal output)
sudo ./humanoid_sec_auditor.py
```

### Options (CLI Arguments)

- `--output <file_path>`: Saves the audit results as a machine-readable JSON file.
- `--report <file_path>`: Saves the audit results as a human-readable Markdown table.
- `--lang <en|ko>`: Sets the output language. Default is `ko`.

**Examples:**

```bash
# Run the audit in English and generate both a Markdown report and a JSON file
sudo ./humanoid_sec_auditor.py --lang en --report audit_report.md --output results.json
```

## Adding a New Check (Plugin Creation)

To add a new security requirement check (e.g., `SYS-22` AppArmor enforcement), follow these two steps:

### 1. Add Messages to `messages.json`

Add the check name and pass/fail messages to both `en` and `ko` blocks in the `messages.json` file.
The key names must strictly follow the format: `{check_id}_name`, `{check_id}_pass`, and `{check_id}_fail`.

```json
"en": {
    ...
    "SYS-22_name": "AppArmor Enforcement",
    "SYS-22_pass": "AppArmor is enabled and enforcing profiles.",
    "SYS-22_fail": "AppArmor is disabled or not enforcing."
}
```

### 2. Add a Check Class in the `checks/` Directory

Add a new class inheriting from `SecurityCheck` to a file inside the `checks/` directory (e.g., `sys_checks.py`).
You can use the `SecurityCheck` base class and the translation function `_()` directly without needing to import them.

```python
# Add this to checks/sys_checks.py

class CheckSYS22(SecurityCheck):
    check_id = "SYS-22"

    def audit(self):
        # Execute a shell command and capture the result
        success, out = self.run_cmd("aa-status | grep 'apparmor module is loaded'")

        if success:
            return True, _("SYS-22_pass")
        else:
            return False, _("SYS-22_fail")
```

The next time you run the main script, the newly added `SYS-22` check will be dynamically loaded and included in the audit!
