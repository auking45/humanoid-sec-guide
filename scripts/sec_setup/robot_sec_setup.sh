#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# Determine the absolute path of the directory containing the script.
# This makes the script location-independent for future enhancements.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# --- Global Variables ---
CONFIG_FILE="config.json"

usage() {
    echo "Usage: $0 [--config <file>] <command>"
    echo
    echo "A script to set up and manage users on a remote server based on a config file."
    echo
    echo "Options:"
    echo "  --config <file>         Specify the configuration file. (default: config.json)"
    echo "  -h, --help              Show this help message."
    echo
    echo "Commands:"
    echo "  setup-admin             Sets up SSH key-based login for the admin account and hardens security."
    echo "  add-dev                 Adds developer accounts from the config file."
    echo "  delete-dev              Safely removes developer accounts from the config file for testing."
    echo "  harden-services         Disables common unnecessary network services (VNC, Samba, etc.)."
    echo "  setup-firewall [opts]   Installs and configures the UFW firewall."
    echo "  setup-auditd            Installs and configures the audit daemon (auditd)."
    echo "  harden-usb              Blocks USB storage devices."
    echo
    echo "Examples:"
    echo "  # Run the admin setup using a custom config file"
    echo "  $0 --config my-server.json setup-admin"
}

# Function to generate an SSH key if it doesn't exist
generate_key() {
    local key_path=$1
    local key_comment=$2
    if [ ! -f "$key_path" ]; then
        echo "🔑 Generating SSH key: $key_path"
        ssh-keygen -t rsa -b 4096 -f "$key_path" -N "" -C "$key_comment"
    else
        echo "✅ SSH key already exists: $key_path"
    fi
}

# --- Command: setup-admin ---
setup_admin() {
    echo "🚀 Step 1: Starting Admin account setup and SSH hardening..."

    local keys_dir="$SCRIPT_DIR/.keys"
    mkdir -p "$keys_dir"
    local admin_key="$keys_dir/id_rsa_rpc_admin"

    generate_key "$admin_key" "$ADMIN_USER@$RPC_IP"

    echo "1. 🔑 Deploying Admin SSH key to the server..."
    echo "   (You will be prompted for the password of the '$ADMIN_USER' account on the server)"
    ssh-copy-id -i "${admin_key}.pub" "$ADMIN_USER@$RPC_IP"

    echo "2. 🛡️  Hardening SSH configuration on the server..."
    ssh -t "$ADMIN_USER@$RPC_IP" sudo bash <<-EOF
set -e
echo "--> ⚙️  Configuring /etc/ssh/sshd_config..."
SSH_CONFIG="/etc/ssh/sshd_config"
sed -i "s/^#?PasswordAuthentication.*/PasswordAuthentication no/" \$SSH_CONFIG
sed -i "s/^#?PermitRootLogin.*/PermitRootLogin no/" \$SSH_CONFIG

# Find and modify AllowUsers to permit only the admin user (or add it)
	if grep -q "^AllowUsers" \$SSH_CONFIG; then
		sed -i "s/^AllowUsers.*/AllowUsers $ADMIN_USER/" \$SSH_CONFIG
	else
		echo "AllowUsers $ADMIN_USER" >> \$SSH_CONFIG
	fi

	echo "--> 🔄 Restarting SSH service..."
systemctl restart ssh
echo "--> 🔒 SSH hardening complete. Only the '$ADMIN_USER' account can now connect via SSH key."
EOF

    echo "✨ Admin account setup complete!"
    echo "   - You can now connect using: ssh -i $admin_key $ADMIN_USER@$RPC_IP"
}

# --- Command: add-dev ---
add_dev_users() {
    echo "🚀 Step 2: Starting to add developer accounts from config..."

    # Read users from config into a bash array
    mapfile -t dev_users < <(jq -r '.users[]' "$CONFIG_FILE")

    local keys_dir="$SCRIPT_DIR/.keys"
    mkdir -p "$keys_dir" # Ensure directory exists
    local admin_key="$keys_dir/id_rsa_rpc_admin"
    local dev_key="$keys_dir/id_rsa_rpc_${dev_user}"

    if [ ! -f "$admin_key" ]; then
        echo "❌ Error: Admin key ($admin_key) not found." >&2
        echo "Please run '$0 setup-admin' first." >&2
        exit 1
    fi

    for dev_user in "${dev_users[@]}"; do
        echo "--- Processing user: $dev_user ---"
        local dev_key="$keys_dir/id_rsa_rpc_${dev_user}"
        generate_key "$dev_key" "$dev_user@$RPC_IP"
        local dev_pub_key
        dev_pub_key=$(cat "${dev_key}.pub")

        echo "1. 👤 Creating '$dev_user' account on the server and deploying the key..."
        # Connect with the admin key to create and configure the developer account with sudo privileges
        ssh -i "$admin_key" -t "$ADMIN_USER@$RPC_IP" sudo bash <<-EOF
set -e

# Define variables for use within the remote script
DEV_USER="$dev_user"
DEV_PUB_KEY="$dev_pub_key"

echo "--> 👤 Creating '\$DEV_USER' account..."
    if ! id "\$DEV_USER" &>/dev/null; then
        useradd -m -s /bin/bash \$DEV_USER
        echo "Account '\$DEV_USER' has been created."
    else
        echo "Account '\$DEV_USER' already exists."
    fi

echo "--> ➕ Adding '\$DEV_USER' to essential groups (sudo, video, etc.)..."
usermod -aG sudo,video,dialout,i2c \$DEV_USER

echo "--> 🔑 Configuring SSH for '\$DEV_USER' account..."
DEV_HOME=/home/\$DEV_USER
    mkdir -p \$DEV_HOME/.ssh
    echo "\$DEV_PUB_KEY" > \$DEV_HOME/.ssh/authorized_keys

# Set permissions for SSH directory and files
    chmod 700 \$DEV_HOME/.ssh
    chmod 600 \$DEV_HOME/.ssh/authorized_keys
    chown -R \$DEV_USER:\$DEV_USER \$DEV_HOME/.ssh

echo "--> ⚙️  Updating SSH daemon configuration..."
SSH_CONFIG=/etc/ssh/sshd_config

# Read the existing AllowUsers list and add the new developer account
    CURRENT_USERS=\$(grep "^AllowUsers" \$SSH_CONFIG | sed "s/AllowUsers //")
    if [[ ! " \$CURRENT_USERS " =~ " \$DEV_USER " ]]; then
        echo "--> Adding '\$DEV_USER' to the allowed list..."
        sed -i "s/^AllowUsers.*/AllowUsers \$CURRENT_USERS \$DEV_USER/" \$SSH_CONFIG
    else
        echo "--> Account '\$DEV_USER' is already in the allowed list."
    fi

echo "--> 🔄 Restarting SSH service..."
systemctl restart ssh
EOF

        echo "✨ Developer account '$dev_user' setup complete!"
        echo "   - You can now connect using: ssh -i $dev_key $dev_user@$RPC_IP"
    done
}

# --- Command: delete-dev ---
delete_dev_users() {
    echo "🚀 Step: Starting to delete developer accounts from config..."

    mapfile -t dev_users < <(jq -r '.users[]' "$CONFIG_FILE")

    local keys_dir="$SCRIPT_DIR/.keys"
    local admin_key="$keys_dir/id_rsa_rpc_admin"

    if [ ! -f "$admin_key" ]; then
        echo "❌ Error: Admin key ($admin_key) not found." >&2
        exit 1
    fi

    for dev_user in "${dev_users[@]}"; do
        echo "--- Processing user deletion: $dev_user ---"
        
        ssh -i "$admin_key" -t "$ADMIN_USER@$RPC_IP" sudo bash <<-EOF
set -e
DEV_USER="$dev_user"

echo "--> 🗑️  Removing '\$DEV_USER' account..."
if id "\$DEV_USER" &>/dev/null; then
    killall -u "\$DEV_USER" || true
    userdel -r "\$DEV_USER"
    echo "Account '\$DEV_USER' has been deleted."
else
    echo "Account '\$DEV_USER' does not exist."
fi

echo "--> ⚙️  Updating SSH daemon configuration..."
SSH_CONFIG=/etc/ssh/sshd_config
if grep -q "^AllowUsers" \$SSH_CONFIG; then
    CURRENT_USERS=\$(grep "^AllowUsers" \$SSH_CONFIG | sed "s/AllowUsers //")
    NEW_USERS=\$(echo "\$CURRENT_USERS" | sed "s/\b\$DEV_USER\b//g" | tr -s ' ' | sed 's/^ *//;s/ *$//')
    sed -i "s/^AllowUsers.*/AllowUsers \$NEW_USERS/" \$SSH_CONFIG
fi
systemctl restart ssh
EOF

        rm -f "$keys_dir/id_rsa_rpc_${dev_user}" "$keys_dir/id_rsa_rpc_${dev_user}.pub"
        echo "✨ Developer account '$dev_user' deletion complete!"
    done
}

# --- Command: harden-services ---
harden_services() {
    if [[ "$(jq -r '.security.harden_services.enabled' "$CONFIG_FILE")" != "true" ]]; then
        echo "🟡 Skipping service hardening as it is not enabled in '$CONFIG_FILE'."
        return
    fi

    echo "🚀 Hardening network services as per config..."

    local keys_dir="$SCRIPT_DIR/.keys"
    local admin_key="$keys_dir/id_rsa_rpc_admin"

    if [ ! -f "$admin_key" ]; then
        echo "❌ Error: Admin key ($admin_key) not found." >&2
        echo "Please run '$0 setup-admin' first." >&2
        exit 1
    fi

    # Create a string of services to pass to the remote script
    local services_to_disable
    services_to_disable=$(jq -r '.security.harden_services.disable[]' "$CONFIG_FILE" | tr '\n' ' ')

    echo "1. 🔌 Connecting to server to disable services..."
    ssh -i "$admin_key" -t "$ADMIN_USER@$RPC_IP" sudo bash -s -- "$services_to_disable" <<'EOF'
set -e

SERVICES_TO_DISABLE=($1)

echo "--> 🔍 Checking and disabling services..."
for service in "${SERVICES_TO_DISABLE[@]}"; do
    if systemctl list-units --full -all | grep -q --fixed-strings "$service.service"; then
        echo "--> 🛑 Disabling and stopping '$service'..."
        systemctl disable --now "$service"
    else
        echo "--> 💨 Service '$service' not found, skipping."
    fi
done

echo "--> 🛡️  Service hardening complete."
EOF

    echo "✨ Network services hardened."
}

# --- Command: setup-firewall ---
setup_firewall() {
    if [[ "$(jq -r '.security.firewall.enabled' "$CONFIG_FILE")" != "true" ]]; then
        echo "🟡 Skipping firewall setup as it is not enabled in '$CONFIG_FILE'."
        return
    fi

    echo "🚀 Configuring Firewall (UFW) as per config..."

    local allow_ports
    allow_ports=$(jq -r '.security.firewall.allow_ports[]? // ""' "$CONFIG_FILE" | tr '\n' ' ')

    local keys_dir="$SCRIPT_DIR/.keys"
    local admin_key="$keys_dir/id_rsa_rpc_admin"

    if [ ! -f "$admin_key" ]; then
        echo "❌ Error: Admin key ($admin_key) not found." >&2
        echo "Please run '$0 setup-admin' first." >&2
        exit 1
    fi

    echo "1. 🛡️  Connecting to server to configure UFW..."
    ssh -i "$admin_key" -t "$ADMIN_USER@$RPC_IP" sudo bash -s -- "$allow_ports" <<-EOF
set -e

# Pass local shell variables to the remote script
ALLOW_PORTS_STR="\$1"

echo "--> 📦 Installing UFW..."
apt-get update > /dev/null
apt-get install -y ufw > /dev/null

echo "--> 🔄 Resetting UFW to a clean state..."
ufw --force reset

echo "--> 룰 Setting default policies (deny incoming, allow outgoing)..."
ufw default deny incoming
ufw default allow outgoing

echo "--> ✅ Allowing SSH connections (critical)..."
ufw allow ssh

for port in \$ALLOW_PORTS_STR; do
    echo "--> ✅ Allowing custom port: \$port..."
    ufw allow "\$port"
fi

echo "--> 📝 Enabling firewall logging (level: low)..."
ufw logging on

echo "--> 🔥 Enabling firewall..."
ufw --force enable

echo "--> 📊 Firewall status:"
ufw status verbose
EOF

    echo "✨ Firewall configured successfully!"
}

# --- Command: setup-auditd ---
setup_auditd() {
    if [[ "$(jq -r '.security.auditd.enabled' "$CONFIG_FILE")" != "true" ]]; then
        echo "🟡 Skipping auditd setup as it is not enabled in '$CONFIG_FILE'."
        return
    fi

    echo "🚀 Installing and configuring Auditd as per config..."

    local keys_dir="$SCRIPT_DIR/.keys"
    local admin_key="$keys_dir/id_rsa_rpc_admin"

    if [ ! -f "$admin_key" ]; then
        echo "❌ Error: Admin key ($admin_key) not found." >&2
        echo "Please run '$0 setup-admin' first." >&2
        exit 1
    fi

    echo "1. 📜 Connecting to server to configure Auditd..."
    ssh -i "$admin_key" -t "$ADMIN_USER@$RPC_IP" sudo bash <<-EOF
set -e

echo "--> 📦 Installing auditd and plugins..."
apt-get update > /dev/null
apt-get install -y auditd audispd-plugins > /dev/null

echo "--> ✍️  Writing baseline audit rules to /etc/audit/rules.d/99-local.rules..."
# Create a robust set of baseline rules. The '-e 2' makes the configuration immutable.
cat > /etc/audit/rules.d/99-local.rules <<'AUDIT_RULES'
# Make the configuration immutable until next reboot to prevent tampering.
-e 2

## Audit user, group, and password database changes
-w /etc/group -p wa -k identity
-w /etc/passwd -p wa -k identity
-w /etc/shadow -p wa -k identity
-w /etc/gshadow -p wa -k identity

## Audit system configuration changes
-w /etc/sudoers -p wa -k sudoers
-w /etc/sudoers.d/ -p wa -k sudoers
-w /etc/ssh/sshd_config -p wa -k sshd_config

## Audit login/logout and session initiation
-w /var/log/faillog -p wa -k logins
-w /var/log/lastlog -p wa -k logins

## Audit changes to audit configuration
-w /etc/audit/ -p wa -k audit_config
AUDIT_RULES

echo "--> 🔄 Restarting auditd service to apply new rules..."
systemctl restart auditd
EOF

    echo "✨ Auditd setup complete!"
}

# --- Command: harden-usb ---
harden_usb() {
    if [[ "$(jq -r '.security.usb_hardening.block_storage' "$CONFIG_FILE")" != "true" ]]; then
        echo "🟡 Skipping USB storage blocking as it is not enabled in '$CONFIG_FILE'."
        return
    fi

    echo "🚀 Hardening USB ports on the server..."

    local keys_dir="$SCRIPT_DIR/.keys"
    local admin_key="$keys_dir/id_rsa_rpc_admin"

    if [ ! -f "$admin_key" ]; then
        echo "❌ Error: Admin key ($admin_key) not found." >&2
        echo "Please run '$0 setup-admin' first." >&2
        exit 1
    fi

    echo "1. 🚫 Connecting to server to block USB storage devices..."
    ssh -i "$admin_key" -t "$ADMIN_USER@$RPC_IP" sudo bash <<-EOF
set -e

echo "--> ✍️  Blacklisting 'usb-storage' kernel module..."
echo "blacklist usb-storage" > /etc/modprobe.d/blacklist-usb-storage.conf

echo "--> 🔄 Applying changes. A reboot is recommended for the blacklist to be fully effective if devices are currently plugged in."
# Unloading the module if it's already loaded. This might fail if a device is in use.
modprobe -r usb-storage || echo "--> ⚠️  Could not unload 'usb-storage' module, it might be in use. A reboot will enforce the block."

EOF

    echo "✨ USB storage devices have been blocked."
}

# --- Main Logic ---
main() {
    if [[ "$1" == "--config" ]]; then
        CONFIG_FILE="$2"
        shift 2
    elif [[ "$1" == "-h" || "$1" == "--help" ]]; then
        usage
        exit 0
    fi

    if [ ! -f "$CONFIG_FILE" ]; then
        echo "❌ Error: Config file '$CONFIG_FILE' not found." >&2
        echo "   You can create one from 'config.json.example'." >&2
        exit 1
    fi

    # Check for jq dependency
    if ! command -v jq &> /dev/null; then
        echo "❌ Error: 'jq' is not installed. Please install it to continue (e.g., 'sudo apt-get install jq')." >&2
        exit 1
    fi

    # Read config values into global variables for other functions to use
    RPC_IP=$(jq -r '.server.ip' "$CONFIG_FILE")
    ADMIN_USER=$(jq -r '.server.admin_user' "$CONFIG_FILE")

    # Check if configuration variables are set
    if [[ -z "$RPC_IP" || "$RPC_IP" == "null" || -z "$ADMIN_USER" || "$ADMIN_USER" == "null" ]]; then
        echo "❌ Error: 'server.ip' and 'server.admin_user' must be set in '$CONFIG_FILE'." >&2
        usage
        exit 1
    fi

    local command=${1:-} # The first non-option argument is the command

    if [[ -z "$command" ]] && [[ "$#" -eq 0 ]]; then
        echo "❌ Error: A command is required." >&2
        usage
        exit 1
    fi

    case "$command" in
        setup-admin)
            setup_admin
            ;;
        add-dev)
            add_dev_users
            ;;
        delete-dev)
            delete_dev_users
            ;;
        harden-services)
            harden_services
            ;;
        setup-firewall)
            setup_firewall
            ;;
        setup-auditd)
            setup_auditd
            ;;
        harden-usb)
            harden_usb
            ;;
        *)
            echo "❌ Error: Unknown command '$command'." >&2
            echo
            usage
            exit 1
            ;;
    esac

    echo "✅ Done."
}

main "$@"
