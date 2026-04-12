# Robot Security Setup Script (`robot_sec_setup.sh`)

This script is a comprehensive tool for initializing and managing a remote Linux server based on a configuration file (`config.json`). It focuses on security and ease of use, automating the setup of SSH key-based authentication, firewalls, service hardening, and more.

## Key Features

- **Configuration-Driven**: Declaratively manage the server's target state in a `config.json` file for consistent and reusable deployments.
- **Automated User Setup**: Automatically creates and configures all developer accounts listed in the configuration file, including SSH key setup.
- **Enhanced Security**: Disables password login, configures a firewall, disables unnecessary services, and sets up the `auditd` for security monitoring.
- **Centralized Key Management**: Automatically generates and stores all necessary SSH keys in a `.keys` subdirectory relative to the script's location, making the entire setup portable.
- **Location-Independent**: The script can be run from any directory without issues.

## Prerequisites

- A local machine with `ssh` and `ssh-keygen` installed.
- A local machine with `jq` installed (`sudo apt-get install jq`).
- A newly installed remote Ubuntu/Debian-based server with an initial user account (e.g., `admin`) that has `sudo` privileges and password-based SSH access enabled.

## File Structure

The project is organized to keep configuration, scripts, and generated credentials separate and clean.

```
.
├── robot_sec_setup.sh
├── GUIDE.md
├── GUIDE.ko.md
├── config.json.example
└── .keys/
    ├── id_rsa_rpc_admin
    ├── id_rsa_rpc_admin.pub
    ├── id_rsa_rpc_dev-user-1
    └── id_rsa_rpc_dev-user-1.pub
```

## Core Workflow: Configuration-Driven Setup

All operations in this project revolve around the `config.json` file.

1.  **Prepare Config**: Copy the example configuration file to `config.json`.
    ```bash
    cp config.json.example config.json
    ```
2.  **Edit Config**: Open `config.json` and modify the values for `ip`, `admin_user`, `users`, etc., to match your target server environment.
3.  **Run Commands Sequentially**: Execute the commands listed in the section below in order to provision the server.

## Batch Setup for Multiple Robots

To apply the same security configuration to multiple robots sequentially, you can use the provided `batch_sec_setup.sh` wrapper script.

1. Create a text file (e.g., `fleet_ips.txt`) containing the IP addresses of your robots, one per line.
   ```text
   192.168.1.101
   192.168.1.102
   192.168.1.103
   ```
2. Run the batch setup script by providing the base configuration file and the IP list file.
   ```bash
   chmod +x batch_sec_setup.sh
   ./batch_sec_setup.sh config.json fleet_ips.txt
   ```
   _Note: During the `setup-admin` step, you may be prompted to enter the initial password for each robot._
   _Once completed, individual verification results will be saved as `verify_IP.json`._

## Commands

All commands are run without arguments and read their settings from the `config.json` file.

### 1. `setup-admin`

This is the **first command** you should run on a new server. It performs the initial security hardening.

- **What it does**:
  1.  Generates a local SSH key pair for the admin user (`.keys/id_rsa_rpc_admin`).
  2.  Copies the public key to the remote server's admin account.
  3.  Modifies the server's SSH configuration to disable password login and restrict access to the admin user via their key.
  ```bash
  ./robot_sec_setup.sh setup-admin
  ```
  _You will be prompted for the admin user's password one time to allow `ssh-copy-id` to work._

### 2. `add-dev`

After `setup-admin` is complete, this command adds all developer accounts from the `users` list in `config.json`.

- **What it does**:
  1.  Generates an SSH key pair for each user in the `users` list.
  2.  Creates each user on the remote server, adds them to the `sudo` group, and deploys their SSH key.
  3.  Updates the `AllowUsers` list in the SSH configuration to grant access to the new developers.
- **Usage**:
  ```bash
  ./robot_sec_setup.sh add-dev
  ```

### 3. `delete-dev`

Removes developer accounts listed in config.json from the server. Useful for testing create/delete cycles.

- **What it does**:
  1.  Deletes the user and their home directory from the remote server.
  2.  Removes the user from the AllowUsers list in the SSH configuration.
  3.  Deletes the locally generated SSH key pair for the user.

- **Usage**:
  ```bash
  ./robot_sec_setup.sh delete-dev
  ```

### 4. `setup-firewall [options]`

Configures the firewall according to the `security.firewall` section in `config.json`.

- **What it does**:
  1.  Only runs if `enabled` is `true` in the config.
  2.  Installs `ufw` and sets the default policy to deny all incoming traffic.
  3.  Always allows SSH and then allows any additional ports listed in `allow_ports`.
- **Usage**:
  ```bash
  ./robot_sec_setup.sh setup-firewall
  ```

### 5. `harden-services`

Disables unnecessary network services based on the `security.harden_services` section in `config.json`.

- **What it does**:
  1.  Only runs if `enabled` is `true` in the config.
  2.  Finds, stops, and disables each service listed in the `disable` array.
- **Usage**:
  ```bash
  ./robot_sec_setup.sh harden-services
  ```

### 6. `setup-auditd`

Installs and configures the audit daemon based on the `security.auditd` section in `config.json`.

- **What it does**:
  1.  Only runs if `enabled` is `true` in the config.
  2.  Installs `auditd` and applies a baseline set of audit rules for monitoring key system files and events.
- **Usage**:
  ```bash
  ./robot_sec_setup.sh setup-auditd
  ```

### 7. `harden-usb`

Blocks USB storage devices based on the `security.usb_hardening` section in `config.json`.

- **What it does**:
  1.  Only runs if `block_storage` is `true` in the config.
  2.  Blacklists the `usb-storage` kernel module to prevent USB storage devices from being used.
- **Usage**:
  ```bash
  ./robot_sec_setup.sh harden-usb
  ```

## Configuration Options

All settings are managed via the `config.json` file. You can create your own by copying `config.json.example`.

- **Command-line Option**:
  - `--config <path>`: Specify a configuration file to use (default: `config.json`).

## Verification Script (`verify_robot_sec_setup.py`)

A companion Python script is provided to automatically verify that the server's state matches the configuration defined in `config.json`.

### Prerequisites

You need Python 3 and `pip` installed on your local machine.

### Setup

Install the required Python libraries using the `requirements.txt` file.

```bash
# Navigate to the script's directory
cd /home/auking45/repos/robot/rpc/

# Install dependencies
pip install -r requirements.txt
```

### Usage

The verification script uses the `config.json` file to run its checks.

```bash
# Run verification using the default config.json
./verify_robot_sec_setup.py

# Run verification using a different config file
./verify_robot_sec_setup.py --config my-server.json

# Run verification and save the results to a JSON file
./verify_robot_sec_setup.py --output results.json

# Verify that developer accounts were successfully deleted after running delete-dev
./verify_robot_sec_setup.py --verify-deleted
```
