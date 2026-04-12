# Open-Source Security Scanner (`run_open_source_scanners.sh`)

This script is a comprehensive tool that scans for configuration vulnerabilities, package (supply chain) vulnerabilities, and network service vulnerabilities existing within the robot system, utilizing three open-source tools (Lynis, Syft/Grype, Nmap) all at once.

## Prerequisites

- **Execution Environment**: This script must be **copied to and executed directly on the target robot device** (e.g., x86 or NVIDIA board), not from an external host PC.
- Internet connection (required for tool installation and vulnerability DB updates).
- Root or `sudo` privileges.

## Usage

You can easily deploy the scanner script to the robot device and fetch the generated report folders later using the provided `scanner_manager.sh` helper script.

```bash
# 1. Deploy the script to the robot (Default path: ~/humanoid_sec_scanner)
chmod +x scanner_manager.sh
./scanner_manager.sh deploy robot_user@192.168.1.100
```

Once deployed, SSH into the robot and run the scanner.

```bash
ssh robot_user@192.168.1.100
cd ~/humanoid_sec_scanner
sudo ./run_open_source_scanners.sh
exit
```

### Options (CLI Arguments)

You can also run specific scanners individually.

- `--all` : Runs all scanners. (Default)
- `--lynis` : Scans only OS and system configuration vulnerabilities using Lynis.
- `--grype` : Generates an SBOM and scans only package/library vulnerabilities (CVEs) using Syft and Grype.
- `--nmap` : Scans only open network ports and service vulnerabilities on the localhost using Nmap and the vulners script.

## Checking Results

Once the execution is complete, a folder in the format of `scan_reports_YYYYMMDD_HHMMSS` will be created under the directory where the script was executed. Inside this folder, detailed analysis reports (`.txt`, `.json`) for each tool will be saved. You can fetch these result files to your host PC for further analysis.
