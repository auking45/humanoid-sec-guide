# 4.1.4. Use Control Checklist

The Use Control Checklist is for controlling access so that only users with legitimate permissions can use robot functions and data. It includes the principle of least privilege and role-based access control (RBAC), aiming to prevent unauthorized manipulation.

| ID | Security Level | Checklist Item | Description |
| :--- | :--- | :--- | :--- |
| UC-01 | L1 | Authorization for human<br>users | The capability to enforce the assigned privileges of human users to support separation of duties and least privilege, and to control the use of all interfaces shall be provided. |
| | L2 | Authorization for all users | The capability to enforce the assigned privileges of all users to support separation of duties and least privilege, and to control the use of all interfaces shall be provided. |
| | L2 | Role-based authorization<br>for users | The capability to define and modify the mapping of privileges to user roles shall be provided. |
| UC-02 | L1 | Use control for mobile<br>code | When using mobile code technologies, the capability to enforce a security policy regarding the use of mobile code technologies shall be provided. |
| | L2 | Mobile code integrity<br>check | The capability to verify the integrity of mobile code before allowing it to execute shall be provided. |
| UC-03 | L1 | Session lock | When providing a user interface locally or over a network, a session lock feature shall be used. |
| UC-04 | L2 | Remote session termination | When supporting remote sessions, the capability to terminate a remote session automatically after a configured period of inactivity, manually by a local administrator, or manually by the user who initiated the session shall be provided. |
| UC-05 | L3 | Concurrent session control | The capability to limit the number of concurrent sessions for a specific user per interface shall be provided. |
| UC-06 | L1 | Audit log generation | The capability to generate security-related audit logs and individual audit logs shall be provided. |
| UC-07 | L1 | Audit log storage capacity | Sufficient audit log storage capacity shall be allocated for audit log management, and a feature to prepare for component failure when the audit storage capacity is approached or exceeded shall be provided. |
| | L3 | Warning on reaching audit<br>storage capacity threshold | The capability to issue a warning when the audit log storage reaches its maximum threshold shall be provided. |
| UC-08 | L1 | Response to audit<br>processing failures | The capability to prevent the loss of essential services and functions in case of audit processing failure and to support appropriate actions in response to audit processing failures in accordance with generally accepted industry practices and recommendations shall be provided. |
| UC-09 | L1 | Timestamps | Timestamps used for audit log generation shall be provided. |
| | L2 | Time synchronization | The capability to synchronize the internal system time shall be provided. |
| | L4 | Protection of time source<br>integrity | The time source shall be protected from unauthorized modification, and an audit event shall be generated upon modification. |
| UC-10 | L1 | Non-repudiation for<br>human users | When providing a human user interface, the capability to determine whether a specific human user has taken a specific action shall be provided. |
| | L4 | Non-repudiation for all<br>users | The capability to determine whether a specific user has taken a specific action shall be provided. |
| UC-11 | L2 | Protection of physical<br>diagnostic and test<br>interfaces | Protection against unauthorized use of physical diagnostic and test interfaces shall be provided. |
| | L3 | Active monitoring of<br>physical diagnostic and<br>test interfaces | Active monitoring of physical diagnostic and test interfaces shall be provided, and an audit log shall be generated when an access attempt to these interfaces is detected. |