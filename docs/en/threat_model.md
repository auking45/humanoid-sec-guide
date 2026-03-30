# Security Threat Types

This section classifies security threat types for the four attributes defined in Chapter 2: hardware, network, system software, and application software. The security threats for each attribute are as follows.

## 1. Hardware Security Threat Types

Hardware security threats are threats to the physical assets of a robot system, including attacks such as physical access, signal forgery, and terminal access. Considering the characteristics of robot systems, they are classified into the following threat types.

| Security Threat | Attack Technique | Affected Security Objectives |
| :--- | :--- | :--- |
| **Physical Tampering** | Physically accessing and damaging the robot, equipment, and protected areas within the perimeter. | Availability, Safety, Reliability |
| **Signal Forgery** | Physically accessing the robot and equipment within the perimeter to transmit malicious signals. | Integrity, Safety, Accuracy |
| **Terminal Access** | Physically accessing and using a keyboard-based terminal within the perimeter to access the operating system. | Confidentiality, Integrity, Availability |
| **Side-Channel Attack** | Indirectly leaking internal secret data or computational values by analyzing measurable information such as power, electromagnetics, and timing from the area. | Confidentiality, Integrity, Reliability |
| **Data Injection/Exfiltration via External Media** | Injecting malicious programs or configuration files, or exfiltrating critical data via external media (e.g., USB) within the area. | Confidentiality, Integrity, Reliability |
| **Storage Device Information Theft and Manipulation** | Physically accessing within the perimeter to dump firmware or steal storage devices to exfiltrate critical data or arbitrarily modify data on the device. | Confidentiality, Integrity, Reliability |

## 2. Network Security Threat Types

Network security threats are threats to the network assets of a robot system, including attacks that cause malfunction and interruption, denial of service, and network eavesdropping. Considering the characteristics of robot systems, they are classified as follows.

| Security Threat | Attack Technique | Affected Security Objectives |
| :--- | :--- | :--- |
| **Inducing Malfunction and Interruption** | Accessing the area network to directly transmit control commands, causing robot malfunction. | Integrity, Availability, Safety, Accuracy, Reliability |
| **Denial of Service (DoS)** | Accessing the area network to send manipulated packets to a vulnerable robot system, causing a denial of service. | Availability, Safety |
| **Message Replay Attack** | Collecting packets from control terminals, message brokers, or routers to bypass authentication and execute malicious commands. | Integrity, Confidentiality, Safety |
| **Network Eavesdropping** | Accessing the area network to eavesdrop on unencrypted communications and collect sensitive data. | Confidentiality |
| **Routing Function Abuse** | Compromising routers installed within the robot or its infrastructure for unauthorized routing or policy bypass. | Confidentiality, Integrity, Availability |
| **Communication Forgery via Key/Certificate Theft** | Neutralizing the trust framework by stealing cryptographic keys and certificates from the control and management domain to forge package signatures and TLS communications. | Confidentiality, Integrity, Reliability |

## 3. System Software Security Threat Types

System software security threats are threats to the system software assets of a robot system, including attacks such as vulnerability exploitation and update function abuse. Considering the characteristics of robot systems, they are classified as follows.

| Security Threat | Attack Technique | Affected Security Objectives |
| :--- | :--- | :--- |
| **Vulnerability Exploitation** | Scanning and exploiting known vulnerabilities to gain privileges and propagate malware. | Confidentiality, Integrity, Availability |
| **Compromising Bootloader and Initial Trust Chain** | Manipulating the initial boot stages (bootloader, secure boot, root of trust) to start the entire system in a malicious state. | Integrity, Reliability, Safety |
| **Update Function Abuse** | Manipulating or bypassing the distribution, verification, and installation procedures of firmware and software updates to weaken security. | Integrity, Reliability |
| **Privilege Escalation** | Exploiting kernel vulnerabilities, drivers, or OS privilege models to gain administrative rights. | Confidentiality, Integrity, Availability |
| **Bypassing Protection Mechanisms** | Bypassing protection mechanisms to perform attacks like ROP, memory corruption, or process hijacking. | Integrity, Safety, Accuracy |
| **Service Configuration Abuse** | Using errors or vulnerable configurations in the OS network stack and system services for unauthorized use of network and system functions. | Availability, Reliability |
| **Log Tampering/Forgery** | Damaging traceability by deleting, altering, or forging event/audit logs. | Integrity, Reliability |
| **Diagnostic Function Abuse** | Exploiting remaining diagnostic ports, debugging modes, or test functions in the system to bypass authentication or gain privileges. | Confidentiality, Integrity, Safety |

## 4. Application Software Security Threat Types

Application software security threats are threats to the application software assets of a robot system, including attacks such as vulnerability exploitation and malware infection. Considering the characteristics of robot systems, they are classified as follows.

| Security Threat | Attack Technique | Affected Security Objectives |
| :--- | :--- | :--- |
| **Vulnerability Exploitation** | Scanning and exploiting known vulnerabilities to gain privileges and propagate malware. | Confidentiality, Integrity, Availability |
| **Task/Motion Configuration Abuse** | Altering robot motion settings to induce behavior intended by the attacker, such as exceeding safety limits. | Integrity, Safety, Accuracy |
| **Access Control Abuse** | Stealing or bypassing access control elements like accounts, authentication, and sessions for unauthorized access. | Confidentiality, Integrity |
| **Configuration Data Tampering** | Distorting system behavior by altering or forging configuration data values (operational/settings, parameters, network, etc.). | Integrity, Reliability, Accuracy |
| **Data Theft/Tampering** | Performing unauthorized viewing, exfiltration, modification, or deletion of data/files stored in or transmitted from the internal DB. | Confidentiality, Integrity |
| **Status Query/Setting Tampering** | Affecting robot operations by manipulating status queries/settings for CPU, Memory, Disk, Time, etc. | Availability, Reliability |
| **Update Function Abuse** | Weakening security by manipulating or bypassing update distribution, verification, and installation procedures. | Integrity, Reliability |
| **Backup/Restore Abuse** | Manipulating backup and restore procedures to cause data leakage or rollbacks (forcing older versions). | Confidentiality, Integrity, Availability |
| **Log Tampering/Forgery** | Damaging traceability by deleting, altering, or forging event/audit logs. | Integrity, Reliability |
| **Remote Support Function Abuse** | Injecting remote commands/settings and hiding maintenance logs by exploiting weak authentication or configuration errors in the remote support function. | Confidentiality, Integrity, Reliability |
| **Malware Infiltration/Infection** | Infecting with malware to cause abnormal process termination or execute additional actions. | Integrity, Availability, Safety |
| **License Authentication Forgery** | Bypassing genuine verification or blocking features of simulation/development tools by stealing license server accounts/keys or attacking server availability. | Integrity, Availability |
| **Unauthorized Software Execution via License File Tampering** | Abusing simulation/development tools by accessing the license server to tamper with license files or issue forged licenses. | Integrity, Reliability |