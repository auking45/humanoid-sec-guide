#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Determine the absolute path of the directory containing the script.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)

usage() {
    echo "Usage: $0 [OPTIONS]"
    echo ""
    echo "Options:"
    echo "  --all       Run all scanners (Default if no option is provided)"
    echo "  --lynis     Run only Lynis (System Configuration & Hardening Scan)"
    echo "  --grype     Run only Syft & Grype (SBOM & Vulnerability Scan)"
    echo "  --nmap      Run only Nmap + Vulners (Network Service Scanning)"
    echo "  -h, --help  Show this help message"
    exit 1
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        echo "❌ Please run this script as root (e.g., sudo $0)"
        exit 1
    fi
}

setup_dependencies() {
    echo "[*] Installing basic dependencies..."
    apt-get update -qq
    apt-get install -y -qq curl wget git nmap
}

run_lynis() {
    echo -e "\n[+] Running Lynis (System Audit)..."
    if [ ! -d "/tmp/lynis" ]; then
        git clone https://github.com/CISOfy/lynis.git /tmp/lynis --quiet
    fi

    cd /tmp/lynis
    # Run Lynis without waiting for user input
    ./lynis audit system --quick > "$REPORT_DIR/lynis_full_report.txt" || true
    # Extract only warnings and suggestions for a quick overview
    grep -E "(Warning|Suggestion)" "$REPORT_DIR/lynis_full_report.txt" > "$REPORT_DIR/lynis_warnings_summary.txt" || true
    cd - > /dev/null

    echo "    -> ✅ Lynis scan complete. (Saved to lynis_full_report.txt)"
}

run_grype() {
    echo -e "\n[+] Running Syft & Grype (SBOM & Vulnerability Scan)..."
    if ! command -v syft &> /dev/null; then
        echo "    -> Installing Syft..."
        curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh | sh -s -- -b /usr/local/bin > /dev/null 2>&1
    fi
    if ! command -v grype &> /dev/null; then
        echo "    -> Installing Grype..."
        curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b /usr/local/bin > /dev/null 2>&1
    fi

    echo "    -> Generating SBOM for root filesystem (This may take a few minutes)..."
    # Exclude virtual and dynamic directories to prevent infinite loops
    syft dir:/ --exclude /proc --exclude /sys --exclude /dev -o json > "$REPORT_DIR/sbom.json" 2> /dev/null

    echo "    -> Scanning SBOM for vulnerabilities..."
    grype sbom:"$REPORT_DIR/sbom.json" > "$REPORT_DIR/grype_vulnerabilities.txt" 2> /dev/null || true
    echo "    -> ✅ Syft & Grype scan complete. (Saved to grype_vulnerabilities.txt and sbom.json)"
}

run_nmap() {
    echo -e "\n[+] Running Nmap + Vulners (Localhost Service Scan)..."
    if [ ! -f "/usr/share/nmap/scripts/vulners.nse" ]; then
        echo "    -> Downloading vulners.nse script..."
        wget -qO /usr/share/nmap/scripts/vulners.nse https://raw.githubusercontent.com/vulnersCom/nmap-vulners/master/vulners.nse
        nmap --script-updatedb > /dev/null
    fi

    # Scan localhost to identify exposed services and potential CVEs on the robot itself
    nmap -sV --script vulners localhost > "$REPORT_DIR/nmap_vulners_report.txt" || true
    echo "    -> ✅ Nmap scan complete. (Saved to nmap_vulners_report.txt)"
}

main() {
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        usage
    fi

    check_root

    local RUN_LYNIS=false
    local RUN_GRYPE=false
    local RUN_NMAP=false

    if [ "$#" -eq 0 ]; then
        RUN_LYNIS=true
        RUN_GRYPE=true
        RUN_NMAP=true
    else
        while [[ "$#" -gt 0 ]]; do
            case $1 in
                --all)
                    RUN_LYNIS=true
                    RUN_GRYPE=true
                    RUN_NMAP=true
                    shift
                    ;;
                --lynis)
                    RUN_LYNIS=true
                    shift
                    ;;
                --grype)
                    RUN_GRYPE=true
                    shift
                    ;;
                --nmap)
                    RUN_NMAP=true
                    shift
                    ;;
                *)
                    echo "❌ Error: Unknown option: $1"
                    usage
                    ;;
            esac
        done
    fi

    # Define report directory based on SCRIPT_DIR and current timestamp
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    export REPORT_DIR="${SCRIPT_DIR}/scan_reports_${TIMESTAMP}"

    echo "=============================================================="
    echo "🤖 Humanoid Robot Comprehensive Open-Source Security Scanner"
    echo "=============================================================="
    echo "[*] Reports will be saved to: $REPORT_DIR"
    echo ""

    mkdir -p "$REPORT_DIR"
    setup_dependencies

    if [ "$RUN_LYNIS" = true ]; then
        run_lynis
    fi

    if [ "$RUN_GRYPE" = true ]; then
        run_grype
    fi

    if [ "$RUN_NMAP" = true ]; then
        run_nmap
    fi

    echo -e "\n=============================================================="
    echo "🎉 All requested Open-Source Security Scans Completed!"
    echo "📂 Please check the results in: $REPORT_DIR"
    echo "=============================================================="
}

main "$@"