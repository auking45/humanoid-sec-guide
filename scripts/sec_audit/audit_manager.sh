#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Default paths
DEFAULT_TARGET_DIR="~/humanoid_sec_audit"
DEFAULT_LOCAL_DIR="."

usage() {
    echo "Usage: $0 <action> <user@host> [target_dir] [local_dir]"
    echo ""
    echo "Actions:"
    echo "  deploy   - Copy the audit scripts and plugins to the remote robot"
    echo "  fetch    - Download the audit reports (JSON/Markdown) from the remote robot"
    echo "             Optional: Provide a webhook URL to send the JSON report after fetching."
    echo ""
    echo "Examples:"
    echo "  $0 deploy robot@192.168.1.100"
    echo "  $0 fetch robot@192.168.1.100 /home/robot/humanoid_sec_audit ./reports"
    echo "  $0 fetch robot@192.168.1.100 /home/robot/humanoid_sec_audit ./reports https://my-dashboard/webhook"
    exit 1
}

deploy() {
    local host=$1
    local target_dir=$2

    echo "[*] Preparing to deploy audit scripts to ${host}:${target_dir}..."

    # Create remote directory, copy required files, and grant execution permissions
    ssh "${host}" "mkdir -p ${target_dir}"
    scp -r humanoid_sec_auditor.py messages.json checks "${host}:${target_dir}/"
    ssh "${host}" "chmod +x ${target_dir}/humanoid_sec_auditor.py"

    echo "[+] Deployment complete!"
    echo "[+] To run the audit, SSH into the robot and execute:"
    echo "    ssh ${host}"
    echo "    cd ${target_dir}"
    echo "    sudo ./humanoid_sec_auditor.py --report audit_report.md --output results.json"
}

fetch() {
    local host=$1
    local target_dir=$2
    local local_dir=$3
    local webhook_url=$4

    echo "[*] Fetching audit reports from ${host}:${target_dir} to local directory: ${local_dir}..."

    # Create local directory if it does not exist
    mkdir -p "${local_dir}"

    # Temporarily disable exit-on-error to handle cases where reports might not exist
    set +e
    scp "${host}:${target_dir}/*.json" "${local_dir}/" 2>/dev/null
    local json_status=$?
    
    scp "${host}:${target_dir}/*.md" "${local_dir}/" 2>/dev/null
    local md_status=$?
    set -e

    if [ $json_status -ne 0 ] && [ $md_status -ne 0 ]; then
        echo "[-] No JSON or Markdown reports found on the remote host."
        echo "[-] Did you run the auditor script with --report or --output options?"
    else
        echo "[+] Fetch complete! Check the '${local_dir}' directory."

        if [ -n "$webhook_url" ]; then
            local latest_json=$(ls -t "${local_dir}"/*.json 2>/dev/null | head -n 1)
            if [ -n "$latest_json" ]; then
                echo "[*] Sending webhook with ${latest_json} to ${webhook_url}..."
                curl -s -X POST -H "Content-Type: application/json" -d @"${latest_json}" "${webhook_url}"
                echo -e "\n[+] Webhook sent successfully!"
            else
                echo "[-] No JSON report found to send via webhook."
            fi
        fi
    fi
}

main() {
    if [ "$#" -lt 2 ]; then
        usage
    fi

    local action=$1
    local host=$2
    local target_dir=${3:-$DEFAULT_TARGET_DIR}
    local local_dir=${4:-$DEFAULT_LOCAL_DIR}
    local webhook_url=$5

    case "$action" in
        deploy)
            deploy "$host" "$target_dir"
            ;;
        fetch)
            fetch "$host" "$target_dir" "$local_dir" "$webhook_url"
            ;;
        *)
            echo "[-] Unknown action: $action"
            usage
            ;;
    esac
}

# Execute main function with all arguments
main "$@"