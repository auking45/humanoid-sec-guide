# 4.2.1. Hardware Security Requirements

These are security requirements to protect the physical components of the robot, responding to the threats identified in Chapter 3. The detailed security requirements are as follows.

| Security Requirement | Mitigation Measure | Checklist ID (Vulnerability Check) | Security Solution |
| :--- | :--- | :--- | :--- |
| **Equipment Integrity Verification** | Protect against physical tampering/opening of equipment with tamper detection functions. | `[SI-11]` Physical tamper resistance and detection<br>`[WS-23]` Equipment integrity assurance | Locking Device,<br>Access Control System,<br>Tamper-proof Device |
| **Fail-Safe State Transition** | Protect against abnormal operations that may occur due to hardware damage by transitioning to a pre-defined safe stop mode. | `[CR-12]` Implementation of safe stop/mode transition in abnormal states | |
| **Ensure Functional Continuity** | Establish recovery procedures to prepare for functional interruption due to partial component damage. | `[CR-11]` Service continuity and maintenance of essential functions | |
| **Inter-Device Authentication** | Protect against unauthorized signal transmission with inter-device authentication. | `[IA-01]` User identification and authentication<br>`[IA-02]` Device identification and authentication | |
| **Enhanced Key Management** | Protect against signal forgery attempts with symmetric/public key lifecycle management. | `[IA-04]` Public key management<br>`[IA-05]` Symmetric key management | Cryptographic Module |
| **Enhanced Access Control & Authentication** | Protect against unauthorized terminal access with authentication and session control. | `[IA-01]` User identification and authentication<br>`[UC-06]` Audit log generation | |
| **Media Control** | Protect against malicious file injection/data leakage with an external media whitelist and scanning policy. | `[SI-02]` Malware protection<br>`[SI-11]` Physical tamper resistance and detection<br>`[UC-06]` Audit log generation | Media Control Solution,<br>Secure USB |
| **Physical Port Protection** | Protect against unauthorized media connection with port locks and physical blocking devices. | `[UC-11]` Control of physical diagnostic and test interfaces<br>`[WS-21]` Restriction of external physical interfaces | Port Lock, Locking Device |
| **Binary Symbol Removal** | Protect against reverse engineering-based information theft by removing binary symbols. | `[DP-01]` Confidentiality of information | |
| **Side-Channel Attack Resistance** | Apply randomization and constant-time algorithms to cryptographic and sensitive operations to prevent leakage of internal operational values through power, timing, or electromagnetic patterns. | `[UC-11]` Control of physical diagnostic and test interfaces | Security Chip |
| **Power/Electromagnetic Shielding** | Apply shielding design to minimize power and electromagnetic signals leaking from the equipment. | `[UC-11]` Control of physical diagnostic and test interfaces | |
| **Disk Encryption** | Protect against data exposure from physical storage device theft with disk encryption. | `[DP-01]` Confidentiality of information | Board with TPM,<br>Security Chip |