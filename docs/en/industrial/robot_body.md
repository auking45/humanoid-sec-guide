# Robot Body

The following are the security requirements for threats that can occur in the robot body.

## Actuator/Drive Unit

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Physical Tampering | Equipment Integrity Verification | Apply functions to detect or prevent physical tampering of the drive unit, triggering alerts and recovery procedures upon case opening or board access. | Locking Device, Access Control System, Tamper-proof Device |
| | | Fail-Safe State Transition | Automatically switch to a safe mode in case of drive unit hardware damage to prevent malfunction. | |
| | | Ensure Functional Continuity | Secure recovery procedures, such as having spare equipment, to maintain core functions even if part of the drive unit is damaged. | |
| | Signal Forgery | Inter-Device Authentication | Ensure drive unit reliability through mutual device/user authentication for all signal transmissions. | |
| | | Enhanced Key Management | Prevent forged drive unit signals by establishing a lifecycle and management procedure for symmetric/public keys. | Cryptographic Module |
| | Storage Device Information Theft and Manipulation | Binary Symbol Removal | Remove symbols from the binary to make reverse engineering of stolen binaries difficult. | |
| | | Disk Encryption | Apply full disk encryption to prevent data exposure in case of physical theft. | Board with TPM, Security Chip |
| | Side-Channel Attack | Apply Side-Channel Attack Resistance Patterns | Apply randomization and constant-time operations to sensitive drive unit calculations to prevent leakage through power, timing, or EM patterns. | Security Chip |
| | | Power/Electromagnetic Shielding | Apply shielding design to minimize power and electromagnetic signals emitted from the drive unit. | |

## Sensor and Feedback Unit

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Physical Tampering | Equipment Integrity Verification | Apply functions to detect or prevent physical tampering of the sensor and feedback unit, triggering alerts and recovery procedures upon case opening or board access. | Locking Device, Access Control System, Tamper-proof Device |
| | | Fail-Safe State Transition | Automatically switch to a safe mode in case of sensor and feedback unit hardware damage to prevent malfunction. | |
| | | Ensure Functional Continuity | Secure recovery procedures, such as having spare equipment, to maintain core functions even if part of the sensor and feedback unit is damaged. | |
| | Signal Forgery | Inter-Device Authentication | Ensure sensor and feedback unit reliability through mutual device/user authentication for all signal transmissions. | |
| | | Enhanced Key Management | Prevent forged sensor and feedback unit signals by establishing a lifecycle and management procedure for symmetric/public keys. | Cryptographic Module |
| | Storage Device Information Theft and Manipulation | Binary Symbol Removal | Remove symbols from the binary to make reverse engineering of stolen binaries difficult. | |
| | | Disk Encryption | Apply full disk encryption to prevent data exposure in case of physical theft. | Board with TPM, Security Chip |
| Network | Network Eavesdropping | Communication Encryption | Protect against eavesdropping by encrypting data transmitted and received over the network. | Security Chip, Secure AP |
| | Message Replay Attack | Session Integrity Verification | Prevent middleware data retransmission with message sequence/Nonce-based verification. | |
| | | Packet Verification | Validate and properly handle middleware command frames and data packets. | Industrial IPS, Industrial Firewall, Industrial IDS, IoT Security Gateway |
| | Malfunction and Interruption | Device Authentication | Allow only authenticated devices to send sensor and feedback unit control commands. | IoT Security Gateway |
| | | Packet Verification | Verify that sensor and feedback unit control commands are within the normal range and switch to safe mode in case of an error. | |
| | | Communication Encryption | Encrypt the sensor and feedback unit control command section with TLS/SSH, etc. | Secure AP |
| | Denial of Service | Protect Service Resources | Prevent resource exhaustion through connection request limits, session separation, etc. | Industrial IPS, Industrial Security Switch |
| | | Limit Unnecessary Functions and Ports | Do not provide terminal port access and unnecessary terminal functions; configure whitelists for each purpose of use. | Industrial IDS, Industrial IPS |

## End-Effector

| Attribute | Security Threat | Security Requirement | Mitigation Measure | Security Solution |
| :--- | :--- | :--- | :--- | :--- |
| H/W | Physical Tampering | Equipment Integrity Verification | Apply functions to detect or prevent physical tampering of the end-effector, triggering alerts and recovery procedures upon case opening or board access. | Locking Device, Access Control System, Tamper-proof Device |
| | | Fail-Safe State Transition | Automatically switch to a safe mode in case of end-effector hardware damage to prevent malfunction. | |
| | | Ensure Functional Continuity | Secure recovery procedures, such as having spare equipment, to maintain core functions even if part of the end-effector is damaged. | |
| | Signal Forgery | Inter-Device Authentication | Ensure end-effector reliability through mutual device/user authentication for all signal transmissions. | |
| | | Enhanced Key Management | Prevent forged signals by establishing a lifecycle and management procedure for symmetric/public keys. | Cryptographic Module |
| | Terminal Access | Enhanced Access Control & Authentication | Apply user authentication and session limits when accessing the management console. | |
| Network | Network Eavesdropping | Communication Encryption | Protect from eavesdropping by encrypting API module data transmitted and received over the network. | Security Chip, Secure AP |
| | Malfunction and Interruption | Device Authentication | Allow only authenticated devices to send end-effector control commands. | IoT Security Gateway |
| | | Input Validation | Verify that end-effector control commands are within the normal range and switch to safe mode in case of an error. | |
| | | Communication Encryption | Encrypt the control command section with TLS/SSH, etc. | Secure AP |