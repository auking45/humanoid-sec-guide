#!/bin/bash

set -e

# Determine the absolute path of the directory containing the script.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

usage() {
    echo "Usage: $0 <base_config.json> <ip_list_file>"
    echo "Example: $0 config.json fleet_ips.txt"
    exit 1
}

main() {
    if [ "$#" -lt 2 ]; then
        usage
    fi

    local BASE_CONFIG=$1
    local IP_LIST_FILE=$2

    if [ ! -f "$BASE_CONFIG" ]; then
        echo "❌ Error: Base config file not found: $BASE_CONFIG"
        exit 1
    fi

    if [ ! -f "$IP_LIST_FILE" ]; then
        echo "❌ Error: IP list file not found: $IP_LIST_FILE"
        exit 1
    fi

    if ! command -v jq &> /dev/null; then
        echo "❌ Error: 'jq' is required but not installed."
        exit 1
    fi

    # Sequence of commands to execute
    local COMMANDS=("setup-admin" "add-dev" "setup-firewall" "harden-services" "setup-auditd" "harden-usb")

    while IFS= read -r IP || [ -n "$IP" ]; do
        # Skip empty lines or comments (#)
        [[ -z "$IP" || "$IP" =~ ^# ]] && continue

        echo "================================================================="
        echo "🚀 Starting Batch Deployment for Robot IP: $IP"
        echo "================================================================="

        local TMP_CONFIG="config_${IP}.json"
        # Create a temporary config file for the specific robot by replacing the IP address in the base config
        jq ".server.ip = \"$IP\"" "$BASE_CONFIG" > "$TMP_CONFIG"

        for CMD in "${COMMANDS[@]}"; do
            echo "⏳ Running command: $CMD for $IP..."
            "$SCRIPT_DIR/robot_sec_setup.sh" --config "$TMP_CONFIG" "$CMD"
        done

        echo "🔍 Running verification for $IP..."
        # Run verification script and save results to JSON (using || true to continue to the next robot even if errors occur)
        "$SCRIPT_DIR/verify_robot_sec_setup.py" --config "$TMP_CONFIG" --output "verify_${IP}.json" || true

        # Delete the temporary config file
        rm -f "$TMP_CONFIG"
        echo "✅ Setup and verification completed for $IP."
        echo ""
    done < "$IP_LIST_FILE"

    echo "🎉 All robots in the fleet have been processed!"
}

main "$@"