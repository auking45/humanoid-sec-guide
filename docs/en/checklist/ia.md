# 4.1.3. Identification and Authentication Checklist

The Identification and Authentication Checklist is for accurately identifying and authenticating all subjects accessing the robot system and its components. It includes strengthening user and device authentication procedures and confirming authorization, aiming to block unauthorized access.

| ID | Security Level | Checklist Item | Description |
| :--- | :--- | :--- | :--- |
| IA-01 | L1 | User authentication | The capability to authenticate all users for all user-accessible interfaces shall be provided. |
| | L2 | Unique user identification<br>and authentication | The capability to uniquely identify and authenticate all users for all user-accessible interfaces shall be provided. |
| | L4 | Multi-factor authentication<br>for all users | The capability to apply multi-factor authentication for all users shall be provided. |
| IA-02 | L2 | Device authentication | The capability to identify and authenticate robotic service components shall be provided. |
| | L3 | Unique device identification<br>and authentication | The robot shall provide the capability to uniquely identify and authenticate other robotic service components. |
| IA-03 | L1 | User password strength | The capability to enforce user password strength in accordance with internationally recognized user password guidelines shall be provided. |
| | L3 | Restriction on reuse of<br>previously used user<br>passwords | The capability to restrict the reuse of previously used user passwords based on configuration shall be provided. |
| | L4 | User password<br>expiration | The capability to limit the valid lifetime of user passwords shall be provided. |
| IA-04 | L2 | Public key authentication | When using a public key infrastructure (PKI), the capability to operate a PKI or obtain public key certificates from an existing PKI shall be provided. |
| | L3 | Hardware security for<br>public key authentication | The capability to protect the associated private keys through a hardware-based security mechanism shall be provided. |
| IA-05 | L2 | Symmetric key<br>authentication | When using symmetric keys, the capability for secure key storage and access restriction, mutual trust establishment, and use of secure cryptographic algorithms shall be provided. |
| | L3 | Hardware security for<br>symmetric key<br>authentication | The capability to protect the associated symmetric keys through a hardware-based security mechanism shall be provided. |
| IA-06 | L1 | Prevention of authenticator<br>feedback | During the user authentication process, authenticators shall not be exposed on output devices, and feedback on the reason for authentication failure shall not be provided. |
| IA-07 | L1 | Limitation on consecutive<br>failed login attempts | In the event of consecutive failed authentication attempts for any user (human, software process, or device), the login attempts for that user shall be limited. |
| IA-08 | L1 | System use notification | For functions that can have a significant impact on the system, users shall be notified of the associated risks. |
| IA-09 | L1 | User account management | The capability to support all user account management, including adding, modifying, deleting, activating, or deactivating all user accounts, shall be provided. |
| IA-10 | L1 | User identifier management | The capability to support user identifier management by user, group, or role shall be provided. |
| IA-11 | L1 | User authenticator<br>management | The user authenticator management function shall provide features for authenticator initialization, default value changes, periodic updates and validation, and protection during storage, use, and transmission. |
| | L3 | Protection of authenticators<br>through hardware security | The capability to protect the associated authenticators through a hardware-based security mechanism shall be provided. |