# 4.1.9. Resource Availability Checklist

The Resource Availability Checklist is for maintaining resources stably to prevent robot functions from being interrupted by denial of service or system overload. It includes performance protection, securing backup resources, and preparing for failures, aiming to ensure the continuous availability of the robot system.

| ID | Security Level | Checklist Item | Description |
| :--- | :--- | :--- | :--- |
| RA-01 | L1 | Denial of service<br>protection | Connection limits, queue settings, process resource limits, etc., shall be applied to prevent the robot system from being paralyzed by attacks such as a large number of connection attempts from the outside, excessive command requests, or large data transmissions. |
| | L2 | Communication load<br>protection | The capability to mitigate the effects of information and/or message flooding types of DoS events shall be provided. |
| RA-02 | L1 | Resource management | The capability to limit the resource usage of security functions to prevent resource exhaustion shall be provided. |
| RA-03 | L1 | Resource status diagnosis | The usage and status of CPU, memory, storage, communication channels, etc., shall be verifiable. |
| RA-04 | L1 | Inventory function support | The capability to report the current list of installed components and the attribute information of each component shall be provided. |
| RA-05 | L1 | System backup | A backup function shall be supported to protect the device state, and the backup process shall not affect normal robot service operation. |
| RA-06 | L1 | Component recovery and<br>reconstitution | The capability to recover and reconstitute to a known secure state after an interruption or failure shall be provided. |
| | L2 | Integrity check before<br>recovery | The capability to verify the integrity of backup files before initiating recovery shall be provided. |
| RA-07 | L1 | Network and security<br>configuration settings | The capability to configure according to the recommended network and security configurations described in the supplier's provided instructions shall be provided, and an interface for the currently applied network and security configuration settings shall be provided. |
| | L3 | Report generation on<br>current security settings | The capability to generate a report listing the currently deployed security settings in a machine-readable format shall be provided. |
| RA-08 | L1 | Restriction of unneeded<br>functionality, ports, and<br>services | The capability to disable or restrict the use of unnecessary functions, ports, protocols, and services shall be provided. |