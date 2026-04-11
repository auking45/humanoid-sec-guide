#!/usr/bin/env python3

import json
import argparse
import os
import sys
import socket
import paramiko

# --- Constants ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
KEYS_DIR = os.path.join(SCRIPT_DIR, ".keys")


# --- Globals for Reporting ---
RESULTS = {"server": None, "config_file": None, "overall_success": False, "checks": []}
OUTPUT_FILE = None


def save_results_and_exit(success):
    """Saves the verification results to a JSON file and exits."""
    RESULTS["overall_success"] = success
    if OUTPUT_FILE:
        try:
            with open(OUTPUT_FILE, "w") as f:
                json.dump(RESULTS, f, indent=4)
            print(f"\n📄 Results saved to {OUTPUT_FILE}")
        except Exception as e:
            print(f"❌ Failed to save results to {OUTPUT_FILE}: {e}")
    if not success:
        sys.exit(1)
    else:
        sys.exit(0)


# --- ANSI Color Codes for Output ---
class Color:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    END = "\033[0m"


def print_status(label, success, message=""):
    """Prints a formatted status line."""
    status = (
        f"{Color.GREEN}PASS{Color.END}" if success else f"{Color.RED}FAIL{Color.END}"
    )
    print(f"[{status}] {label:.<50} {message}")

    RESULTS["checks"].append({"label": label, "success": success, "message": message})

    if not success:
        # Exit on first failure to prevent cascading errors
        save_results_and_exit(False)


def validate_key_paths(dev_users):
    """Validates that all necessary SSH keys exist and returns the admin key path."""
    admin_key_path = os.path.join(KEYS_DIR, "id_rsa_rpc_admin")
    if not os.path.exists(admin_key_path):
        msg = f"Admin SSH key not found in '{KEYS_DIR}'"
        print(f"❌ {Color.RED}Error: {msg}.{Color.END}")
        print("Please run './robot_sec_setup.sh setup-admin' first.")
        RESULTS["checks"].append(
            {"label": "Validate Admin SSH Key", "success": False, "message": msg}
        )
        save_results_and_exit(False)

    for user in dev_users:
        dev_key_path = os.path.join(KEYS_DIR, f"id_rsa_rpc_{user}")
        if not os.path.exists(dev_key_path):
            msg = f"SSH key for user '{user}' not found"
            print(f"❌ {Color.RED}Error: {msg}.{Color.END}")
            print("Please run './robot_sec_setup.sh add-dev' first.")
            RESULTS["checks"].append(
                {
                    "label": f"Validate SSH Key for '{user}'",
                    "success": False,
                    "message": msg,
                }
            )
            save_results_and_exit(False)

    return admin_key_path


def check_dev_key_login(host, user, key_path):
    """Tests if the dev user can log in with their SSH key."""
    label = f"Login with key for user '{user}'"
    try:
        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(host, username=user, key_filename=key_path, timeout=5)
            stdin, stdout, stderr = client.exec_command("whoami")
            output = stdout.read().decode().strip()

            if output == user:
                print_status(label, True)
            else:
                print_status(label, False, f"Logged in but whoami returned '{output}'")
    except Exception as e:
        print_status(label, False, f"Connection failed: {e}")


def check_password_login(host, user):
    """Tests that password-based login is disabled."""
    label = f"Attempt password login for user '{user}'"
    try:
        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # This connection attempt should fail with an AuthenticationException
            client.connect(
                host,
                username=user,
                password="dummy_password",
                allow_agent=False,
                look_for_keys=False,  # Crucial: do not use local keys
                timeout=5,
            )
        # If we reach here, the connection succeeded, which is a failure for this test
        print_status(label, False, "Password login succeeded unexpectedly.")
    except paramiko.AuthenticationException:
        # This is the expected outcome
        print_status(label, True, "Correctly failed as expected.")
    except Exception as e:
        print_status(label, False, f"An unexpected error occurred: {e}")


def check_root_login(host, key_path):
    """Tests that root login is disabled."""
    label = "Attempt root login"
    try:
        with paramiko.SSHClient() as client:
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            # Attempt to connect as root, even with a valid key (e.g., admin's)
            client.connect(host, username="root", key_filename=key_path, timeout=5)
        print_status(label, False, "Root login succeeded unexpectedly.")
    except paramiko.AuthenticationException:
        print_status(label, True, "Correctly failed as expected.")
    except Exception as e:
        print_status(label, False, f"An unexpected error occurred: {e}")


def run_remote_command(host, user, key_path, command):
    """Helper to run a command on the remote server."""
    with paramiko.SSHClient() as client:
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=user, key_filename=key_path, timeout=5)
        stdin, stdout, stderr = client.exec_command(command)
        exit_status = stdout.channel.recv_exit_status()
        return (
            stdout.read().decode().strip(),
            stderr.read().decode().strip(),
            exit_status,
        )


def check_sshd_config(host, admin_user, admin_key_path):
    """Verifies key settings in /etc/ssh/sshd_config."""
    label_prefix = "Verify sshd_config:"

    # 1. Check PasswordAuthentication
    cmd = "grep -E '^[[:space:]]*PasswordAuthentication[[:space:]]+no' /etc/ssh/sshd_config"
    stdout, _, exit_status = run_remote_command(
        host, admin_user, admin_key_path, f"sudo {cmd}"
    )
    print_status(f"{label_prefix} PasswordAuthentication is 'no'", exit_status == 0)

    # 2. Check PermitRootLogin
    cmd = "grep -E '^[[:space:]]*PermitRootLogin[[:space:]]+no' /etc/ssh/sshd_config"
    stdout, _, exit_status = run_remote_command(
        host, admin_user, admin_key_path, f"sudo {cmd}"
    )
    print_status(f"{label_prefix} PermitRootLogin is 'no'", exit_status == 0)


def check_firewall_rules(host, admin_user, admin_key_path, firewall_config):
    """Checks UFW status and rules against expectations."""
    label_prefix = "Verify Firewall (UFW):"

    stdout, _, exit_status = run_remote_command(
        host, admin_user, admin_key_path, "sudo ufw status verbose"
    )

    if not firewall_config.get("enabled", False):
        is_inactive = "Status: inactive" in stdout
        print_status(f"{label_prefix} UFW is inactive (as expected)", is_inactive)
        return

    if exit_status != 0:
        print_status(
            f"{label_prefix} Could not get UFW status",
            False,
            "Is UFW installed and enabled?",
        )
        return  # Can't proceed

    lines = stdout.splitlines()

    # 1. Check if active
    is_active = any("Status: active" in line for line in lines)
    print_status(f"{label_prefix} UFW is active", is_active)
    if not is_active:
        return  # Further checks are pointless

    # 2. Check default policies
    has_deny_incoming = any("Default: deny (incoming)" in line for line in lines)
    print_status(f"{label_prefix} Default policy is DENY INCOMING", has_deny_incoming)

    has_allow_outgoing = any("Default: allow (outgoing)" in line for line in lines)
    print_status(f"{label_prefix} Default policy is ALLOW OUTGOING", has_allow_outgoing)

    # 3. Check logging status
    is_logging_on = any("Logging: on" in line for line in lines)
    print_status(f"{label_prefix} Logging is ON", is_logging_on)

    # 4. Check rules
    # Helper to check for a rule. UFW output can vary (e.g., '22/tcp' or 'OpenSSH')
    def rule_exists(port_or_name):
        return any((port_or_name in line and "ALLOW IN" in line) for line in lines)

    # SSH must always be allowed
    ssh_allowed = rule_exists("22/tcp") or rule_exists("OpenSSH")
    print_status(f"{label_prefix} Allows SSH", ssh_allowed)

    # 5. Check configured ports
    allowed_ports = firewall_config.get("allow_ports", [])
    # Create a set of rules found on the server for efficient checking
    rules = {line for line in lines if "ALLOW IN" in line}
    for port in allowed_ports:
        # Normalize port for check, e.g., "9090/tcp" -> "9090"
        port_num = port.split("/")[0]
        port_allowed = rule_exists(port) or rule_exists(port_num)
        print_status(f"{label_prefix} Allows custom port '{port}'", port_allowed)


def check_disabled_services(host, admin_user, admin_key_path, services_config):
    """Verifies that common unnecessary services are inactive."""
    label_prefix = "Verify Disabled Services:"

    if not services_config.get("enabled", False):
        print_status(f"{label_prefix} Skipped", True, "Not enabled in config.")
        return

    SERVICES_TO_CHECK = services_config.get("disable", [])

    for service in SERVICES_TO_CHECK:
        label = f"{label_prefix} '{service}' is not active"

        # `systemctl is-active` is the most direct way to check if a service is running.
        # It returns exit code 0 if 'active', and a non-zero code (3) if 'inactive' or 'not-found'.
        # A non-zero exit code is a success for this test.
        cmd = f"systemctl is-active {service}"
        stdout, stderr, exit_status = run_remote_command(
            host, admin_user, admin_key_path, cmd
        )

        is_not_active = exit_status != 0

        message = (
            f"Correctly not active (state: {stdout})."
            if is_not_active
            else "Service is unexpectedly active."
        )

        print_status(label, is_not_active, message)


def check_auditd_status(host, admin_user, admin_key_path, auditd_config):
    """Verifies that auditd is installed, active, and has rules loaded."""
    label_prefix = "Verify Auditd:"

    if not auditd_config.get("enabled", False):
        cmd = "systemctl is-active auditd"
        _, _, exit_status = run_remote_command(host, admin_user, admin_key_path, cmd)
        print_status(
            f"{label_prefix} Service is not active (as expected)", exit_status != 0
        )
        return

    # 1. Check if service is active
    cmd = "systemctl is-active auditd"
    stdout, _, exit_status = run_remote_command(host, admin_user, admin_key_path, cmd)
    is_active = exit_status == 0 and stdout == "active"
    print_status(f"{label_prefix} Service is active", is_active)
    if not is_active:
        return  # Can't proceed

    # 2. Check if our rules file exists
    rules_file = "/etc/audit/rules.d/99-local.rules"
    cmd = f"test -f {rules_file}"
    _, _, exit_status = run_remote_command(
        host, admin_user, admin_key_path, f"sudo {cmd}"
    )
    print_status(
        f"{label_prefix} Custom rules file '{rules_file}' exists", exit_status == 0
    )

    # 3. Check if rules are loaded
    cmd = "auditctl -l"
    stdout, _, exit_status = run_remote_command(
        host, admin_user, admin_key_path, f"sudo {cmd}"
    )
    has_identity_rule = "-w /etc/passwd -p wa -k identity" in stdout
    print_status(f"{label_prefix} Identity watch rule is loaded", has_identity_rule)


def check_usb_hardening(host, admin_user, admin_key_path, usb_config):
    """Verifies that USB storage is blocked."""
    label_prefix = "Verify USB Hardening:"

    if not usb_config.get("block_storage", False):
        print_status(f"{label_prefix} Skipped", True, "Not enabled in config.")
        return

    # 1. Check if the blacklist file exists
    blacklist_file = "/etc/modprobe.d/blacklist-usb-storage.conf"
    cmd = f"test -f {blacklist_file}"
    _, _, exit_status = run_remote_command(
        host, admin_user, admin_key_path, f"sudo {cmd}"
    )
    print_status(
        f"{label_prefix} Blacklist file '{blacklist_file}' exists", exit_status == 0
    )

    # 2. Check if the module is currently loaded.
    # A non-zero exit code means it's not loaded, which is a success.
    cmd = "lsmod | grep -q '^usb_storage'"
    _, _, exit_status = run_remote_command(host, admin_user, admin_key_path, cmd)
    print_status(f"{label_prefix} 'usb-storage' module is not loaded", exit_status != 0)


def main():
    """Main function to parse arguments and run checks."""
    parser = argparse.ArgumentParser(
        description="Verify the security configuration of a remote server.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "--config",
        default="config.json",
        help="Path to the configuration file. (default: config.json)",
    )
    parser.add_argument(
        "--output",
        help="Path to save the verification results as a JSON file.",
    )

    args = parser.parse_args()

    global OUTPUT_FILE
    OUTPUT_FILE = args.output
    RESULTS["config_file"] = args.config

    try:
        with open(args.config, "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        msg = f"Config file '{args.config}' not found"
        print(f"❌ {Color.RED}Error: {msg}.{Color.END}")
        RESULTS["checks"].append(
            {"label": "Load Config", "success": False, "message": msg}
        )
        save_results_and_exit(False)
    except json.JSONDecodeError as e:
        msg = f"Could not decode JSON from '{args.config}': {e}"
        print(f"❌ {Color.RED}Error: {msg}{Color.END}")
        RESULTS["checks"].append(
            {"label": "Parse Config", "success": False, "message": msg}
        )
        save_results_and_exit(False)

    # Get values from config
    server_config = config.get("server", {})
    ip = server_config.get("ip")
    admin_user = server_config.get("admin_user")
    dev_users = config.get("users", [])
    security_config = config.get("security", {})

    RESULTS["server"] = ip

    # Check if configuration variables are set
    if not ip or not admin_user:
        msg = f"'server.ip' and 'server.admin_user' must be set in '{args.config}'"
        print(f"❌ {Color.RED}Error: {msg}.{Color.END}")
        RESULTS["checks"].append(
            {"label": "Configuration Validation", "success": False, "message": msg}
        )
        save_results_and_exit(False)

    print(
        f"\n🚀 {Color.BLUE}--- Starting Verification for Server: {ip} based on '{args.config}' ---{Color.END}"
    )

    admin_key = validate_key_paths(dev_users)

    # --- Run Checks ---
    for dev_user in dev_users:
        print(
            f"\n🧪 {Color.YELLOW}1. Testing Logins for user '{dev_user}'...{Color.END}"
        )
        dev_key = os.path.join(KEYS_DIR, f"id_rsa_rpc_{dev_user}")
        check_dev_key_login(ip, dev_user, dev_key)
        check_password_login(ip, dev_user)

    print(f"\n🧪 {Color.YELLOW}1a. Testing Root Login...{Color.END}")
    check_root_login(ip, admin_key)  # Use admin key for the attempt

    print(f"\n🧪 {Color.YELLOW}2. Verifying SSH Daemon Configuration...{Color.END}")
    check_sshd_config(ip, admin_user, admin_key)

    print(f"\n🧪 {Color.YELLOW}3. Verifying Firewall Configuration...{Color.END}")
    check_firewall_rules(ip, admin_user, admin_key, security_config.get("firewall", {}))

    print(f"\n🧪 {Color.YELLOW}4. Verifying Disabled Network Services...{Color.END}")
    check_disabled_services(
        ip, admin_user, admin_key, security_config.get("harden_services", {})
    )

    print(f"\n🧪 {Color.YELLOW}5. Verifying Audit Daemon (auditd)...{Color.END}")
    check_auditd_status(ip, admin_user, admin_key, security_config.get("auditd", {}))

    print(f"\n🧪 {Color.YELLOW}6. Verifying USB Hardening...{Color.END}")
    check_usb_hardening(
        ip, admin_user, admin_key, security_config.get("usb_hardening", {})
    )

    print(
        f"\n🎉 {Color.GREEN}--- Verification Complete: All checks passed! ---{Color.END}\n"
    )
    save_results_and_exit(True)


if __name__ == "__main__":
    main()
