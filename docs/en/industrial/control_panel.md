# Robot Control Panel

The following are the security requirements for threats that can occur in the robot control panel.

## Middleware

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| Network | Network Eavesdropping | Communication Encryption | Protect against eavesdropping by encrypting middleware data transmitted and received over the network. | Security Chip, Secure AP |
| | Message Replay Attack | Session Integrity Verification | Prevent middleware data retransmission with message sequence/Nonce-based verification. | |
| | | Packet Verification | Validate and properly handle middleware command frames and data packets. | Industrial IPS, Industrial Firewall, Industrial IDS, IoT Security Gateway |
| | Routing Function Abuse | Authentication-based Routing | Allow only authenticated users/devices to change middleware routing settings. | Industrial Firewall |
| | | Routing History Management | Record middleware routing changes and traffic flow. | |
| System S/W | Vulnerability Exploit | Regular Security Checks and Configuration Hardening | Detect abnormal input values in middleware. | Source Code Analysis Tool, Industrial EDR |
| | | | Block exploits with regular scans and prompt patching for known vulnerabilities. | Source Code Analysis Tool |
| | | | Disable unnecessary middleware services and manage security settings. | Security Certification Consulting |
| | | | Establish procedures for officially reporting and improving discovered middleware vulnerabilities. | |
| | | Supply Chain Security | Manage and update SBOM for middleware open-source and external modules. | Source Code Analysis Tool, Patch Management Solution |
| | | | Operate vulnerability patch and automatic deployment mechanisms based on middleware service lifecycle (EoS). | Patch Management Solution |
| | Update Function Abuse | Update Verification | Store behavioral evidence through signature-based integrity verification and anti-tampering for middleware, and generate related logs. | Patch Management Solution |
| | | Safe Rollback | Provide automatic recovery function in case of middleware patch failure. | Patch Management Solution |
| | | Security Update Policy | Establish procedures for providing and applying regular middleware patches. | Server Access Control Solution |
| Application S/W | Malware Infiltration/Infection | Log Traceability | Periodically check the normal operation of middleware security functions and generate logs of middleware-related activities for non-repudiation. | Server Access Control Solution |
| | | Malware Scan | Detect middleware malware with antivirus, sandboxing, and file integrity checks. | Industrial EDR, Antivirus |
| | Unauthorized Software Execution due to License File Tampering | Integrity Verification | Verify hash/signature of the license file before execution. | |
| | | Malware Scan | Detect malicious middleware activity through forged files. | Industrial EDR, Antivirus |
| | | Log Traceability | Generate activity logs in middleware related to software execution. | Server Access Control Solution |

## API Module

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| Network | Malfunction and Interruption | Ensure Communication Reliability | Detect API module communication anomalies through device identification and authentication for communication access control, CRC checks, etc. | IoT Security Gateway |
| | | Packet Verification | Validate and properly handle API module command frames and data packets. | Industrial IPS, Industrial Firewall |
| | Denial of Service | Protect Service Resources | Prevent API module resource exhaustion through connection request limits, session separation, etc. | Industrial IPS, Industrial Security Switch |
| | | Limit Unnecessary Functions and Ports | Do not provide terminal port access to the API module and unnecessary terminal functions; configure whitelists for each purpose of use. | Industrial IDS, Industrial IPS |
| | Network Eavesdropping | Communication Encryption | Protect against eavesdropping by encrypting API module data transmitted and received over the network. | Security Chip, Secure AP |
| Application S/W | Access Control Function Abuse | Authentication-based Access Control | Strengthen API module password policies, prevent brute-force attacks, and periodically change authenticators. | Server Access Control Solution |
| | | Session Management | Block illegal sessions with API module concurrent session limits, session lock/termination functions. | |
| | | Account Management | Periodically check and disable unnecessary API module accounts. | Server Access Control Solution |
| | | Log Traceability | Record all API module login, access, and failure histories, including time information. | Server Access Control Solution |
| | Job/Operation Setting Abuse | Authentication-based Access Control | Control so that only authorized users can change API module safety settings. | Server Access Control Solution |
| | | Input Validation | Validate that setting values do not exceed the safe range of the API module. | |
| | | Safe Stop | Automatic mode transition to prevent abnormal operation in case of an incorrect command to the API module. | |
| | | Job Notification | Execute job monitoring and generate result logs, and notify in case of API module abnormality. | Industrial Firewall |
| | Configuration Data Tampering | Role-based Access Control | Allow only users with specific permissions, such as administrators, to change API module configuration data. | Server Access Control Solution |
| | | Input Validation | Verify that API module operating parameters are within the allowed range upon input. | |
| | | Backup Management | Record API module change history and restore from periodic backups in case of configuration damage. | Backup Management System |
| | | Integrity Verification | Detect and protect against tampering of API module configuration data. | |

## Operating System

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| Network | Denial of Service | Protect Service Resources | Prevent resource exhaustion by limiting OS connection requests, separating sessions, etc. | Industrial IPS, Industrial Security Switch |
| | | Limit Unnecessary Functions and Ports | Do not provide terminal port access to the OS and unnecessary terminal functions; configure whitelists for each purpose of use. | Industrial IDS, Industrial IPS |
| System S/W | Bootloader and Initial Trust Chain Corruption | Boot Setting Protection | Prevent tampering by verifying the signature of the OS boot image/bootloader. | |
| | | | Maintain initial trust by verifying the hash of the OS firmware/kernel before loading. | Board with TPM |
| | | | Lock OS boot parameters, debug mode, and firmware selection options to be unchangeable. | |
| | Privilege Escalation | Principle of Least Privilege | Reduce attack surface by removing unnecessary administrator/root privileges from the OS. | Server Access Control Solution |
| | | Kernel Hardening | Block privilege escalation attacks with OS memory protection, address space layout randomization, etc. | |
| | | Allow Only Signed Drivers | Natively block the loading of malicious drivers/kernel modules in the OS. | |
| | Update Function Abuse | Update Verification | Store behavioral evidence through signature-based integrity verification and anti-tampering for the OS, and generate related logs. | Patch Management Solution |
| | | Safe Rollback | Provide automatic recovery function in case of OS patch failure. | Patch Management Solution |
| | | Security Update Policy | Establish procedures for providing and applying regular OS patches. | Patch Management Solution |
| | Protection Bypass | Process Integrity Verification | Continuously check for code tampering or hooking during OS execution. | Industrial EDR |
| | Log Tampering/Forgery | Audit Log Protection Management | Generate and store logs for various events and OS audits, including timestamps. | |
| | | | Apply access control and encryption to prevent OS log file tampering. | |
| | | | Establish a rotation/cycling policy to prevent log saturation. | |
| | | Event Analysis | Secure sufficient OS logs and perform regular analysis. | |
| | Diagnostic Function Abuse | Diagnostic Function Access Control | Restrict developer/test functions remaining in the OS for diagnostics with authentication. | |

## I/O Module

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Signal Forgery | Inter-Device Authentication | Ensure I/O module reliability through mutual device/user authentication for all signal transmissions. | |
| | | Enhanced Key Management | Prevent forged I/O module signals by establishing a lifecycle and management procedure for symmetric/public keys. | Cryptographic Module |
| | Storage Device Information Theft and Manipulation | Binary Symbol Removal | Remove symbols from the I/O module binary to make reverse engineering of stolen binaries difficult. | |
| | | Disk Encryption | Apply full disk encryption to prevent data exposure in case of physical theft. | Board with TPM, Security Chip |
| | Data Injection/Exfiltration via External Media | Media Control | Restrict usage to allowed media such as secure USBs, and disallow or scan all other external media. | Media Control Solution, Secure USB |
| | | Physical Port Protection | Apply physical blocking devices like port locks and connector caps that could indirectly affect the I/O module. | Port Lock, Locking Device |

## Main Board

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Physical Tampering | Equipment Integrity Verification | Apply functions to detect or prevent physical tampering of the main board inside the equipment, triggering alerts and recovery procedures upon case opening or board access. | Locking Device, Access Control System, Tamper-proof Device |
| | | Fail-Safe State Transition | Automatically switch to a safe mode in case of hardware damage to prevent main board malfunction. | |
| | | Ensure Functional Continuity | Secure recovery procedures, such as having spare equipment, to maintain core functions even if part of the main board is damaged. | |
| | Terminal Access | Enhanced Access Control & Authentication | Apply user authentication and session limits when accessing the main board's management console. | |
| | Storage Device Information Theft and Manipulation | Binary Symbol Removal | Remove symbols from the main board binary to make reverse engineering of stolen binaries difficult. | |
| | | Disk Encryption | Apply full disk encryption to prevent main board data exposure in case of physical theft. | Board with TPM, Security Chip |
| | Signal Forgery | Inter-Device Authentication | Ensure main board reliability through mutual device/user authentication for all signal transmissions. | |
| | | Enhanced Key Management | Prevent forged main board signals by establishing a lifecycle and management procedure for symmetric/public keys. | Cryptographic Module |

## Interface

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Terminal Access | Enhanced Access Control & Authentication | Apply user authentication and session limits when accessing the management console. | |
| | Data Injection/Exfiltration via External Media | Media Control | Restrict usage to allowed media such as secure USBs, and disallow or scan all other external media. | Media Control Solution, Secure USB |
| | | Physical Port Protection | Apply physical blocking devices like port locks and connector caps. | Port Lock, Locking Device |
| | Signal Forgery | Inter-Device Authentication | Ensure reliability through mutual device/user authentication for all signal transmissions. | |
| | | Enhanced Key Management | Prevent forged signals by establishing a lifecycle and management procedure for symmetric/public keys. | Cryptographic Module |

## Servo Drive

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Physical Tampering | Equipment Integrity Verification | Apply functions to detect or prevent physical tampering of the servo drive inside the equipment, triggering alerts and recovery procedures upon case opening or board access. | Locking Device, Access Control System, Tamper-proof Device |
| | | Fail-Safe State Transition | Automatically switch to a safe mode in case of servo drive hardware damage to prevent malfunction. | |
| | | Ensure Functional Continuity | Secure recovery procedures, such as having spare equipment, to maintain core functions even if part of the servo drive is damaged. | |
| | Signal Forgery | Inter-Device Authentication | Ensure servo drive reliability through mutual device/user authentication for all signal transmissions. | |
| | | Enhanced Key Management | Prevent forged servo drive signals by establishing a lifecycle and management procedure for symmetric/public keys. | Cryptographic Module |
| | Storage Device Information Theft and Manipulation | Binary Symbol Removal | Remove symbols from the servo drive binary to make reverse engineering of stolen binaries difficult. | |
| | | Disk Encryption | Apply full disk encryption to prevent data exposure in case of physical theft. | Board with TPM, Security Chip |
| | Side-Channel Attack | Apply Side-Channel Attack Resistance Patterns | Apply randomization and constant-time operations to sensitive servo drive calculations to prevent leakage through power, timing, or EM patterns. | Security Chip |
| | | Power/Electromagnetic Shielding | Apply shielding design to minimize power and electromagnetic signals emitted from the servo drive. | |