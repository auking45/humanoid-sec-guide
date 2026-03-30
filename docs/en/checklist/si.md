# 4.1.5. System Integrity Checklist

The System Integrity Checklist is for protecting the components and data of the robot system from being tampered with or maliciously altered. It includes code and firmware integrity verification, configuration protection, and blocking of unauthorized commands, aiming to maintain the integrity of the system.

| ID | Security Level | Checklist Item | Description |
| :--- | :--- | :--- | :--- |
| SI-01 | L1 | Communication integrity | The capability to protect the integrity and authenticity of transmitted information shall be provided. |
| SI-02 | L1 | Malware protection<br>mechanism | A protection mechanism to prevent, detect, report, and mitigate the effects of malware or unauthorized software shall be provided. Additionally, the capability to update the protection mechanism shall be provided. |
| | L2 | Malware protection version<br>reporting | The versions of the malware protection software and files in use shall be reported automatically. |
| SI-03 | L1 | Security function verification | The capability to support the verification of the intended operation of security functions shall be provided. If an anomaly such as a compromised integrity is detected, it shall stop operation or switch to a safe mode, and automatically report the breach to the administrator or cloud with a log record. |
| SI-04 | L1 | Integrity of software,<br>data, and equipment | The integrity of software, data, and equipment stored inside the robot shall be stored in a protected storage that can guarantee integrity and be applied with hash functions, digital signatures, etc. Also, the capability to check the status at boot and at regular intervals to detect, record, and report unauthorized changes shall be provided. |
| | L2 | Automatic notification of<br>integrity violations | The capability to provide response measures such as administrator notification and automatic blocking when an unauthorized change attempt is detected on major software, data, or equipment of the robot system during operation or integrity check shall be provided. |
| | L3 | Authenticity checks for<br>software and information | The capability to perform authenticity checks on software, configuration, and other information, and to record and report the results of these checks shall be provided. |
| SI-05 | L1 | Input validation | The validity of input values used as control inputs or that directly affect the operation of the robot service shall be verified. |
| SI-06 | L1 | Deterministic output | In the event of an inability to maintain normal operation due to an attack or other factors, the capability to set the output to a predetermined state shall be provided. |
| SI-07 | L1 | Error handling | Error conditions shall be identified and handled in a way that does not provide information that could be exploited by an attacker. |
| SI-08 | L2 | Session integrity protection | The capability to protect communication session integrity, such as secure generation and verification of unique session IDs, rejection of invalid session IDs, and invalidation of session IDs upon session termination, shall be provided. |
| SI-09 | L2 | Protection of audit-related<br>information | Audit information, audit logs, and audit tools shall be protected from unauthorized access, modification, and deletion. |
| | L4 | Recording audit records on<br>write-once media | The capability to store audit records on hardware-based write-once media shall be provided. |
| SI-10 | L1 | Update support verification | The capability to support update and upgrade functions shall be provided. |
| | L2 | Verification of authenticity<br>and integrity of update<br>files | The authenticity and integrity of software update files shall be verified before installation. |
| SI-11 | L2 | Physical tamper resistance<br>and detection | Tamper-resistant and detection mechanisms shall be provided to prevent unauthorized physical access to the device. |
| | L3 | Notification of tampering<br>attempts | The capability to automatically notify when an unauthorized physical access attempt is detected shall be provided. |