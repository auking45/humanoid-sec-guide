#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Determine the absolute path of the directory containing the script
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

# Default paths
DEFAULT_TARGET_DIR="~/humanoid_sec_scanner"
DEFAULT_LOCAL_DIR="./reports"

usage() {
    echo "Usage: $0 <action> <user@host> [target_dir] [local_dir]"
    echo ""
    echo "Actions:"
    echo "  deploy   - Copy the scanner script to the remote robot"
    echo "  fetch    - Download the scan reports from the remote robot"
    echo ""
    echo "Examples:"
    echo "  $0 deploy robot@192.168.1.100"
    echo "  $0 fetch robot@192.168.1.100 ~/humanoid_sec_scanner ./my_reports"
    exit 1
}

deploy() {
    local host=$1
    local target_dir=$2

    echo "[*] Preparing to deploy the open-source scanner to ${host}:${target_dir}..."
    
    ssh "${host}" "mkdir -p ${target_dir}"
    scp "${SCRIPT_DIR}/run_open_source_scanners.sh" "${host}:${target_dir}/"
    ssh "${host}" "chmod +x ${target_dir}/run_open_source_scanners.sh"

    echo "[+] Deployment complete!"
    echo "[+] To run the scanner, SSH into the robot and execute:"
    echo "    ssh ${host}"
    echo "    cd ${target_dir}"
    echo "    sudo ./run_open_source_scanners.sh --all"
}

fetch() {
    local host=$1
    local target_dir=$2
    local local_dir=$3

    echo "[*] Fetching scan reports from ${host}:${target_dir} to local directory: ${local_dir}..."
    mkdir -p "${local_dir}"

    # scp with -r to download the timestamped directories
    scp -r "${host}:${target_dir}/scan_reports_*" "${local_dir}/" 2>/dev/null || echo "[-] No scan reports found."
    
    echo "[+] Fetch attempt complete! Check the '${local_dir}' directory."
}

main() {
    if [ "$#" -lt 2 ]; then
        usage
    fi

    local action=$1
    local host=$2
    local target_dir=${3:-$DEFAULT_TARGET_DIR}
    local local_dir=${4:-$DEFAULT_LOCAL_DIR}

    case "$action" in
        deploy) deploy "$host" "$target_dir" ;;
        fetch) fetch "$host" "$target_dir" "$local_dir" ;;
        *) echo "[-] Unknown action: $action"; usage ;;
    esac
}

main "$@"