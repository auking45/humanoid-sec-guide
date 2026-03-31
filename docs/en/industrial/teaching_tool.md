# Teaching Tool

The following are the security requirements for threats that can occur in the teaching tool.

## Teach Pendant

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Physical Tampering | Equipment Integrity Verification | Apply functions to detect or prevent physical tampering inside the teach pendant, triggering alerts and recovery procedures upon case opening or board access. | Locking Device, Access Control System, Tamper-proof Device |
| | | Fail-Safe State Transition | Automatically switch to a safe mode in case of teach pendant hardware damage to prevent malfunction. | |
| | | Ensure Functional Continuity | Secure recovery procedures, such as having spare equipment, to maintain core functions even if part of the teach pendant is damaged. | |
| | Terminal Access | Enhanced Access Control & Authentication | Apply user authentication and session limits when accessing the teach pendant's management console. | |
| | Data Injection/Exfiltration via External Media | Media Control | On the teach pendant, restrict usage to allowed media such as secure USBs, and disallow or scan all other external media. | Media Control Solution, Secure USB |
| | | Physical Port Protection | Apply physical blocking devices like port locks and connector caps to the teach pendant. | Port Lock, Locking Device |
| | Storage Device Information Theft and Manipulation | Binary Symbol Removal | Remove symbols from the teach pendant binary to make reverse engineering of stolen binaries difficult. | |
| | | Disk Encryption | Apply full disk encryption to prevent teach pendant data exposure in case of physical theft. | Board with TPM, Security Chip |
| Network | Malfunction and Interruption | Ensure Communication Reliability | Detect communication anomalies through teach pendant device identification and authentication for communication access control, CRC checks, etc. | IoT Security Gateway |
| | | Packet Verification | Validate and properly handle teach pendant command frames and data packets. | Industrial IPS, Industrial Firewall |
| | | | Verify that teach pendant control commands are within the normal range and switch to safe mode in case of an error. | Industrial IDS, IoT Security Gateway |
| | | Device Authentication | Allow only authenticated devices to send teach pendant control commands. | IoT Security Gateway |
| | | Communication Encryption | Encrypt the teach pendant control command section with TLS/SSH, etc. | Secure AP |
| | Network Eavesdropping | Communication Encryption | Protect the teach pendant from eavesdropping by encrypting API module data transmitted and received over the network. | Security Chip, Secure AP |
| System S/W | Vulnerability Exploit | Regular Security Checks and Configuration Hardening | Detect abnormal input values occurring in the teach pendant. | Industrial EDR |
| | | | Block exploits with regular scans and prompt patching for known vulnerabilities. | Source Code Analysis Tool |
| | | | Disable unnecessary teach pendant services and manage security settings. | |
| | | | Establish procedures for officially reporting and improving discovered teach pendant vulnerabilities. | Security Certification Consulting |
| | | Supply Chain Security | Manage and update SBOM for teach pendant open-source and external modules. | Source Code Analysis Tool, Patch Management Solution |
| | | | Operate vulnerability patch and automatic deployment mechanisms based on the teach pendant service lifecycle (EoS). | Patch Management Solution |
| | Privilege Escalation | Principle of Least Privilege | Reduce the teach pendant's attack surface by removing unnecessary administrator/root privileges. | Server Access Control Solution |
| | | Kernel Hardening | Block privilege escalation attacks with teach pendant memory protection, address space layout randomization, etc. | |
| | | Allow Only Signed Drivers | Natively block the loading of malicious drivers/kernel modules on the teach pendant. | |
| | Update Function Abuse | Update Verification | Store behavioral evidence through signature-based integrity verification and anti-tampering for the teach pendant, and generate related logs. | Patch Management Solution |
| | | Safe Rollback | Provide automatic recovery function in case of teach pendant patch failure. | Patch Management Solution |
| | | Security Update Policy | Establish procedures for providing and applying regular teach pendant patches. | Patch Management Solution |
| | Log Tampering/Forgery | Audit Log Protection Management | Generate and store logs for various teach pendant events and audits, including timestamps. | |
| | | | Apply access control and encryption to prevent teach pendant log file tampering; establish a rotation/cycling policy to prevent log saturation. | |
| | | Event Analysis | Secure sufficient teach pendant logs and perform regular analysis. | |
| Application S/W | Access Control Function Abuse | Authentication-based Access Control | API key-based authentication and JWT token-based session management. | Server Access Control Solution |
| | | Role-based Access Control | Separate API access rights by user role (e.g., general user/operator/administrator). | Server Access Control Solution |
| | Job/Operation Setting Abuse | Authentication-based Access Control | Control so that only authorized users can change teach pendant safety settings. | Server Access Control Solution |
| | | Input Validation | Validate that setting values do not exceed the teach pendant's safe range. | |
| | | Safe Stop | Automatic mode transition to prevent abnormal operation of the teach pendant in case of an incorrect command. | |
| | | Job Notification | Execute teach pendant job monitoring, generate result logs, and notify in case of abnormality. | Industrial Firewall |
| | Configuration Data Tampering | Role-based Access Control | Allow only users with specific permissions, such as administrators, to change teach pendant configuration data. | Server Access Control Solution |
| | | Input Validation | Verify that teach pendant operating parameters are within the allowed range upon input. | |
| | | Backup Management | Record teach pendant change history and restore from periodic backups in case of configuration damage. | Backup Management System |
| | | Integrity Verification | Detect and protect against tampering of teach pendant configuration data. | |
| | Data Theft/Tampering | Data Encryption | Apply strong encryption algorithms to important teach pendant data. | |
| | | Role-based Access Control | Restrict access to sensitive teach pendant data and generate audit logs. | DB Access Control System |
| | | Integrity Verification | Use signatures/hashes to prevent teach pendant data tampering. | |
| | | Privacy Protection | When processing personally identifiable information on the teach pendant, collect the minimum necessary, store it encrypted, and completely delete it when required. | Data Erasure Solution |
| | | Backup Management | Prevent teach pendant data loss through periodic backups and recovery tests. | Backup Management System |
| | Backup/Restore Abuse | Integrity Verification | Verify whether teach pendant backup data has been tampered with. | |
| | | Role-based Access Control | Minimize access rights to the teach pendant backup storage. | Server Access Control Solution |
| | | Log Traceability | Store teach pendant backup/restore job logs, including time information. | Server Access Control Solution |

## EWS (Engineering Workstation)

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Physical Tampering | Equipment Integrity Verification | Apply functions to detect or prevent physical tampering inside the EWS equipment, triggering alerts and recovery procedures upon case opening or board access. | Locking Device, Access Control System, Tamper-proof Device |
| | | Fail-Safe State Transition | Automatically switch to a safe mode in case of EWS hardware damage to prevent malfunction. | |
| | | Ensure Functional Continuity | Secure recovery procedures, such as having spare equipment, to maintain core functions even if part of the EWS is damaged. | |
| | Terminal Access | Enhanced Access Control & Authentication | Apply user authentication and session limits when accessing the EWS management console. | |
| | Data Injection/Exfiltration via External Media | Media Control | On the EWS, restrict usage to allowed media such as secure USBs, and disallow or scan all other external media. | Media Control Solution, Secure USB |
| | | Physical Port Protection | Apply physical blocking devices like port locks and connector caps to the EWS. | Port Lock, Locking Device |
| | Storage Device Information Theft and Manipulation | Binary Symbol Removal | Remove symbols from the EWS binary to make reverse engineering of stolen binaries difficult. | |
| | | Disk Encryption | Apply full disk encryption to prevent EWS data exposure in case of physical theft. | Board with TPM, Security Chip |
| Network | Malfunction and Interruption | Ensure Communication Reliability | Detect EWS communication anomalies through device identification and authentication for communication access control, CRC checks, etc. | IoT Security Gateway |
| | | Packet Verification | Validate and properly handle EWS command frames and data packets. | Industrial IPS, Industrial Firewall |
| | | | Verify that EWS control commands are within the normal range and switch to safe mode in case of an error. | Industrial IDS, IoT Security Gateway |
| | | Device Authentication | Allow only authenticated devices to send EWS control commands. | IoT Security Gateway |
| | | Communication Encryption | Encrypt the EWS control command section with TLS/SSH, etc. | Secure AP |
| | Denial of Service | Protect Service Resources | Prevent EWS resource exhaustion through connection request limits, session separation, etc. | Industrial IPS, Industrial Security Switch |
| | | Limit Unnecessary Functions and Ports | Do not provide terminal port access to the EWS and unnecessary terminal functions; configure whitelists for each purpose of use. | Industrial IDS, Industrial IPS |
| | Network Eavesdropping | Communication Encryption | Protect the EWS from eavesdropping by encrypting API module data transmitted and received over the network. | Security Chip, Secure AP |
| System S/W | Vulnerability Exploit | Regular Security Checks and Configuration Hardening | Detect abnormal input values that have occurred in the EWS. | Industrial IPS |
| | | | Block exploits with regular scans and prompt patching for known vulnerabilities. | Source Code Analysis Tool |
| | | | Disable unnecessary EWS services and manage security settings. | |
| | | | Establish procedures for officially reporting and improving discovered EWS vulnerabilities. | Security Certification Consulting |
| | | Supply Chain Security | Manage and update SBOM for open-source and external modules used in the EWS. | Source Code Analysis Tool, Patch Management Solution |
| | | | Operate vulnerability patch and automatic deployment mechanisms based on the EWS service lifecycle (EoS). | Patch Management Solution |
| | Privilege Escalation | Principle of Least Privilege | Reduce the EWS attack surface by removing unnecessary administrator/root privileges. | Server Access Control Solution |
| | | Kernel Hardening | Block privilege escalation attacks with EWS memory protection, address space layout randomization, etc. | |
| | | Allow Only Signed Drivers | Natively block the loading of malicious drivers/kernel modules on the EWS. | |
| | Update Function Abuse | Update Verification | Store behavioral evidence through signature-based integrity verification and anti-tampering for the EWS, and generate related logs. | Patch Management Solution |
| | | Safe Rollback | Provide automatic recovery function in case of EWS patch failure. | Patch Management Solution |
| | | Security Update Policy | Establish procedures for providing and applying regular EWS patches. | Patch Management Solution |
| | Log Tampering/Forgery | Audit Log Protection Management | Generate and store logs for various EWS events and audits, including timestamps. | |
| | | | Apply access control and encryption to prevent EWS log file tampering; establish a rotation/cycling policy to prevent log saturation. | |
| | | Event Analysis | Secure sufficient EWS logs and perform regular analysis. | |
| Application S/W | Access Control Function Abuse | Authentication-based Access Control | API key-based authentication and JWT token-based session management. | Server Access Control Solution |
| | | Role-based Access Control | Separate API access rights by user role (e.g., general user/operator/administrator). | Server Access Control Solution |
| | Job/Operation Setting Abuse | Authentication-based Access Control | Control so that only authorized users can change EWS safety settings. | Server Access Control Solution, Backup Management System |
| | | Input Validation | Validate that setting values do not exceed the EWS's safe range. | |
| | | Safe Stop | Automatic mode transition to prevent abnormal operation of the EWS in case of an incorrect command. | |
| | | Job Notification | Execute EWS job monitoring, generate result logs, and notify in case of abnormality. | Industrial Firewall |
| | Configuration Data Tampering | Role-based Access Control | Allow only users with specific permissions, such as administrators, to change EWS configuration data. | |
| | | Input Validation | Verify that parameters are within the EWS's allowed range upon input. | |
| | | Backup Management | Record EWS change history and restore from periodic backups in case of configuration damage. | Backup Management System |
| | | Integrity Verification | Detect and protect against tampering of EWS configuration data. | |
| | Data Theft/Tampering | Data Encryption | Apply strong encryption algorithms to important EWS data. | DB Access Control System |
| | | Role-based Access Control | Restrict access to sensitive EWS data and generate audit logs. | DB Access Control System |
| | | Integrity Verification | Use signatures/hashes to prevent EWS data tampering. | |
| | | Privacy Protection | When processing personally identifiable information on the EWS, collect the minimum necessary, store it encrypted, and completely delete it when required. | Data Erasure Solution |
| | | Backup Management | Prevent EWS data loss through periodic backups and recovery tests. | Backup Management System |
| | Remote Support Function Abuse | Authentication-based Access Control | Strengthen EWS password policies, prevent brute-force attacks, and periodically change authenticators. | Server Access Control Solution |
| | | Session Management | Block illegal sessions with EWS concurrent session limits, session lock/termination functions. | |
| | | Account Management | Periodically check and disable unnecessary EWS accounts. | Server Access Control Solution |
| | | Log Traceability | Record all EWS login, access, and failure histories, including time information. | Server Access Control Solution |
| | Malware Infiltration/Infection | Malware Scan | Detect malware inside the EWS with antivirus, sandboxing, and file integrity checks. | Industrial EDR, Antivirus |
| | Unauthorized Software Execution due to License File Tampering | Integrity Verification | Verify hash/signature of the EWS license file before execution. | |
| | | Malware Scan | Detect malicious EWS activity through forged files. | Industrial EDR, Antivirus |
| | | Log Traceability | Generate activity logs related to EWS software execution. | Server Access Control Solution |

## HMI (Human-Machine Interface)

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Physical Tampering | Equipment Integrity Verification | Apply functions to detect or prevent physical tampering inside the HMI equipment, triggering alerts and recovery procedures upon case opening or board access. | Locking Device, Access Control System, Tamper-proof Device |
| | | Fail-Safe State Transition | Automatically switch to a safe mode in case of HMI hardware damage to prevent malfunction. | |
| | | Ensure Functional Continuity | Secure recovery procedures, such as having spare equipment, to maintain core HMI functions even if partially damaged. | |
| | Terminal Access | Enhanced Access Control & Authentication | Apply user authentication and session limits when accessing the HMI management console. | |
| | Data Injection/Exfiltration via External Media | Media Control | On the HMI, restrict usage to allowed media such as secure USBs, and disallow or scan all other external media. | Media Control Solution, Secure USB |
| | | Physical Port Protection | Apply physical blocking devices like port locks and connector caps to the HMI. | Port Lock, Locking Device |
| Network | Malfunction and Interruption | Ensure Communication Reliability | Detect communication anomalies through HMI device identification and authentication for communication access control, CRC checks, etc. | IoT Security Gateway |
| | | Packet Verification | Validate and properly handle HMI command frames and data packets. | Industrial IPS, Industrial Firewall |
| | | | Verify that HMI control commands are within the normal range and switch to safe mode in case of an error. | Industrial IDS, IoT Security Gateway |
| | | Communication Encryption | Encrypt the HMI control command section with TLS/SSH, etc. | Secure AP |
| | | Device Authentication | Allow only authenticated devices to send HMI control commands. | IoT Security Gateway |
| | Denial of Service | Protect Service Resources | Prevent HMI resource exhaustion through connection request limits, session separation, etc. | Industrial IPS, Industrial Security Switch |
| | | Limit Unnecessary Functions and Ports | Do not provide terminal port access to the HMI and unnecessary terminal functions; configure whitelists for each purpose of use. | Industrial IDS, Industrial IPS |
| | Network Eavesdropping | Communication Encryption | Protect the HMI from eavesdropping by encrypting API module data transmitted and received over the network. | Security Chip, Secure AP |
| System S/W | Vulnerability Exploit | Regular Security Checks and Configuration Hardening | Detect abnormal input values that have occurred in the HMI. | Industrial EDR |
| | | | Block exploits with regular scans and prompt patching for known vulnerabilities. | Source Code Analysis Tool |
| | | | Disable unnecessary HMI services and manage security settings. | |
| | | | Establish procedures for officially reporting and improving discovered HMI vulnerabilities. | Security Certification Consulting |
| | | Supply Chain Security | Manage and update SBOM for open-source and external modules used by the HMI. | Source Code Analysis Tool, Patch Management Solution |
| | | Patch Management | Operate vulnerability patch and automatic deployment mechanisms based on the HMI service lifecycle (EoS). | Patch Management Solution |
| | Privilege Escalation | Principle of Least Privilege | Reduce the HMI attack surface by removing unnecessary administrator/root privileges. | Server Access Control Solution |
| | | Kernel Hardening | Block privilege escalation attacks with HMI memory protection, address space layout randomization, etc. | |
| | | Allow Only Signed Drivers | Natively block the loading of malicious drivers/kernel modules on the HMI. | Industrial IDS |
| | Update Function Abuse | Update Verification | Store behavioral evidence through signature-based integrity verification and anti-tampering for the HMI, and generate related logs. | Patch Management Solution |
| | | Safe Rollback | Provide automatic recovery function in case of HMI patch failure. | Patch Management Solution |
| | | Security Policy | Establish procedures for providing and applying regular HMI patches. | Patch Management Solution |
| | Log Tampering/Forgery | Audit Log Protection Management | Generate and store logs for various HMI events and audits, including timestamps. | Backup Management System |
| | | Event Analysis | Secure sufficient HMI logs and perform regular analysis. | |
| | | Audit Log Protection Management | Apply access control and encryption to prevent HMI log file tampering; establish a rotation/cycling policy to prevent log saturation. | |
| Application S/W | Access Control Function Abuse | Authentication-based Access Control | API key-based authentication and JWT token-based session management. | Server Access Control Solution |
| | | Role-based Access Control | Separate API access rights by user role (e.g., general user/operator/administrator). | Server Access Control Solution |
| | Job/Operation Setting Abuse | Authentication-based Access Control | Control so that only authorized users can change HMI safety settings. | Server Access Control Solution |
| | | Input Validation | Validate that setting values do not exceed the HMI's safe range. | |
| | | Safe Stop | Automatic mode transition to prevent abnormal operation of the HMI in case of an incorrect command. | |
| | | Job Notification | Execute HMI job monitoring, generate result logs, and notify in case of abnormality. | Industrial Firewall |
| | Configuration Data Tampering | Role-based Access Control | Allow only users with specific permissions, such as administrators, to change HMI configuration data. | Server Access Control Solution |
| | | Input Validation | Verify that operating parameters are within the HMI's allowed range upon input. | |
| | | Backup Management | Record change history and restore from periodic backups in case of HMI configuration damage. | Backup Management System |
| | | | Detect and protect against tampering of HMI configuration data. | Industrial Firewall |
| | Data Theft/Tampering | Data Encryption | Apply strong encryption algorithms to important HMI data. | |
| | | Access Control | Restrict access to sensitive HMI data and generate audit logs. | |
| | | Integrity Verification | Use signatures/hashes to prevent HMI data tampering. | |
| | | Privacy Protection | When processing personally identifiable information on the HMI, collect the minimum necessary, store it encrypted, and completely delete it when required. | Data Erasure Solution |
| | | Backup Management | Prevent HMI data loss through periodic backups and recovery tests. | Backup Management System |
| | Status Inquiry/Setting Tampering | Authentication-based Access Control | Allow only authenticated users to view HMI device status (CPU, Memory, etc.), and generate logs for access and actions. | Server Access Control Solution |
| | | Role-based Access Control | Differentiate between viewing and changing HMI permissions and prevent arbitrary settings. | |
| | | Integrity Verification | Apply a protection mechanism to prevent tampering of HMI status information. | |
| | Remote Support Function Abuse | Authentication-based Access Control | Strengthen HMI password policies, prevent brute-force attacks, and periodically change authenticators. | Server Access Control Solution |
| | | Session Management | Block illegal sessions with HMI concurrent session limits, session lock/termination functions. | |
| | | Account Management | Periodically check and disable unnecessary HMI accounts. | Server Access Control Solution |
| | | Log Traceability | Record all HMI login, access, and failure histories, including time information. | Server Access Control Solution |