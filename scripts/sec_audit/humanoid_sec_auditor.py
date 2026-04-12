#!/usr/bin/env python3
"""
Humanoid Security Auditor
This script automatically audits the system against Humanoid-Specific Security Requirements
specified in 'specific_requirements.md'.
"""

import subprocess
import sys
import argparse
import json
import os
import importlib.util
import urllib.request
import urllib.error

# ==============================================================================
# Load messages for i18n support
# ==============================================================================

CURRENT_LANG = "ko"
MESSAGES = {}

MSG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "messages.json"
)
try:
    with open(MSG_FILE_PATH, "r", encoding="utf-8") as f:
        MESSAGES = json.load(f)
except Exception as e:
    print(f"❌ Failed to load messages file (messages.json): {e}")
    sys.exit(1)


def _(key, **kwargs):
    """Returns the string matching the current language."""
    text = MESSAGES.get(CURRENT_LANG, MESSAGES["en"]).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text


class SecurityCheck:
    """Base class for all security checks"""

    check_id = "UNKNOWN"

    @property
    def name(self):
        return (
            _(f"{self.check_id}_name")
            if self.check_id != "UNKNOWN"
            else _("unknown_check")
        )

    def run_cmd(self, cmd):
        """Executes a shell command and returns success status and output."""
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            return True, result.stdout.strip()
        except subprocess.CalledProcessError as e:
            return False, e.stdout.strip()

    def audit(self):
        """Subclasses must implement the actual audit logic.
        Returns: (success: bool, message: str)
        """
        raise NotImplementedError("audit() method must be implemented.")


# ==============================================================================
# Main Auditor Runner
# ==============================================================================


class HumanoidAuditor:
    def __init__(self):
        self.results = {"overall_success": False, "checks": []}
        self._load_plugins()
        # Automatically scan and instantiate all classes inheriting from SecurityCheck
        self.checks = [cls() for cls in SecurityCheck.__subclasses__()]

    def _load_plugins(self):
        """Dynamically load audit modules from the checks/ directory."""
        checks_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checks")
        if not os.path.exists(checks_dir):
            os.makedirs(checks_dir, exist_ok=True)

        for filename in sorted(os.listdir(checks_dir)):
            if filename.endswith(".py") and not filename.startswith("__"):
                module_name = filename[:-3]
                file_path = os.path.join(checks_dir, filename)
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                if spec and spec.loader:
                    module = importlib.util.module_from_spec(spec)
                    # Inject globals into the plugin so they can be used without importing
                    module.SecurityCheck = SecurityCheck
                    module._ = _
                    spec.loader.exec_module(module)

    def run_all(self):
        passed = 0
        manual = 0
        for check in self.checks:
            print(_("auditing", id=check.check_id, name=check.name))
            success, msg = check.audit()

            is_manual = not success and ("[MANUAL]" in msg or "[수동점검]" in msg)

            if is_manual:
                status_str = "[MANUAL]"
                manual += 1
            else:
                status_str = "[PASS]" if success else "[FAIL]"

            print(f"  {status_str} {msg}")

            self.results["checks"].append(
                {
                    "id": check.check_id,
                    "label": f"{check.check_id}: {check.name}",
                    "success": success,
                    "is_manual": is_manual,
                    "message": msg,
                }
            )

            if success:
                passed += 1

        self.results["overall_success"] = passed == len(self.checks)
        return passed, manual, len(self.checks)


def main():
    parser = argparse.ArgumentParser(description="Humanoid Security Auditor")
    parser.add_argument(
        "--output", help="Path to save the audit results as a JSON file."
    )
    parser.add_argument(
        "--report", help="Path to save the audit results as a Markdown report."
    )
    parser.add_argument(
        "--webhook", help="Webhook URL to send the JSON audit results via POST."
    )
    parser.add_argument(
        "--lang",
        choices=["en", "ko"],
        default="ko",
        help="Output language (default: ko)",
    )
    args = parser.parse_args()

    global CURRENT_LANG
    CURRENT_LANG = args.lang

    print("=" * 60)
    print(_("header_title").center(60))
    print("=" * 60)

    auditor = HumanoidAuditor()
    passed, manual, total = auditor.run_all()
    failed = total - passed - manual

    print("=" * 60)
    print(_("summary", passed=passed, manual=manual, total=total))
    print("=" * 60)

    auditor.results["summary"] = {
        "total": total,
        "passed": passed,
        "failed": failed,
        "manual": manual,
    }

    if args.output:
        try:
            with open(args.output, "w", encoding="utf-8") as f:
                json.dump(auditor.results, f, indent=4, ensure_ascii=False)
            print(_("saved_to", file=args.output))
        except Exception as e:
            print(_("save_fail", err=e))

    if args.report:
        try:
            with open(args.report, "w", encoding="utf-8") as f:
                md = f"# {_('report_title')}\n\n"
                md += f"## {_('report_summary')}\n"
                md += f"- **{_('report_total')}**: {total}\n"
                md += f"- **{_('report_passed')}**: {passed}\n"
                md += f"- **{_('report_failed')}**: {failed}\n"
                md += f"- **{_('report_manual')}**: {manual}\n\n"
                md += f"## {_('report_detail')}\n"
                md += f"| {_('report_col_id')} | {_('report_col_status')} | {_('report_col_msg')} |\n"
                md += "|---|---|---|\n"
                for check in auditor.results["checks"]:
                    if check.get("is_manual"):
                        status = "🟡 MANUAL"
                    else:
                        status = "🟢 PASS" if check["success"] else "🔴 FAIL"
                    md += f"| {check['id']} | {status} | {check['message']} |\n"

                f.write(md)
            print(_("report_saved_to", file=args.report))
        except Exception as e:
            print(_("save_fail", err=e))

    if args.webhook:
        try:
            req = urllib.request.Request(
                args.webhook,
                data=json.dumps(auditor.results).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                print(_("webhook_success", url=args.webhook))
        except Exception as e:
            print(_("webhook_fail", err=e))


if __name__ == "__main__":
    main()
