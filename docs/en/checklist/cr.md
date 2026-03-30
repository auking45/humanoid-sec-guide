# 4.1.10. Cyber Resilience Checklist

The Cyber Resilience Checklist is to ensure that the robot's core functions are maintained and can be quickly restored in the event of a breach. It includes security updates, backup and restore, vulnerability management, and ensuring operational continuity, aiming to strengthen the cyber resilience of the robot system.

| ID | Checklist Item | Description |
| :--- | :--- | :--- |
| CR-01 | Regular Backup and Management<br>of Critical Configuration Data | Critical settings and data of the robot system must be periodically backed up and managed. |
| CR-02 | Backup Data Integrity and<br>Recovery Verification Procedures | The recovery procedures for robot operation must be documented, and checks and verifications must be performed to ensure their effectiveness. |
| CR-03 | Documentation and Testing of<br>Recovery Procedures for Cyber<br>Incidents | Robot operation recovery procedures must be documented in preparation for cyber incidents, and mock tests must be conducted regularly. |
| CR-04 | Definition of Recovery Time<br>Objective (RTO) and Recovery<br>Point Objective (RPO) | The Recovery Time Objective (RTO) and Recovery Point Objective (RPO) must be clearly defined for robot system failures to enable rapid recovery. |
| CR-05 | Timely Provision and Application<br>of Security Updates and Patches | Security updates and patches for robot software and firmware must be provided for prompt application. |
| CR-06 | Rollback or Recovery Function<br>in Case of Update Failure | It must be possible to roll back to a previous stable version or recover if a security update for the robot system fails. |
| CR-07 | Specification of Security Update<br>Support Policy and Lifecycle | A clear security update provision policy must be established and operated for the support life of the robot. |
| CR-08 | Establishment of Official<br>Procedures for Reporting and<br>Handling Security Vulnerabilities | There must be an official procedure for receiving and promptly handling security vulnerability reports from external sources. |
| CR-09 | Securing Sufficient Logs and<br>Supporting Security Event<br>Analysis | Sufficient logs must be secured and managed to support cause analysis and recovery when a security event occurs in the robot system. |
| CR-10 | Procedure for Improving Security<br>Measures Based on Incidents/<br>Vulnerabilities | Security measures must be periodically reviewed and continuously improved based on incident and vulnerability information. |
| CR-11 | Service Continuity and<br>Maintenance of Essential<br>Functions | The robot system must be designed so that essential safety and operational functions are maintained even in partial system failures or DoS attack situations. |
| CR-12 | Implementation of Safe Stop and<br>Mode Transition in Abnormal<br>States | The robot system must be able to automatically perform a safe stop or switch to a safe mode in abnormal states such as communication loss or sensor errors. |
| CR-13 | Protection of Authentication<br>Data such as User Information | Personal data used in the robot system's authentication, identity, and access systems should only be stored, transmitted, or otherwise processed if relevant to the product and must be protected from unauthorized access and confidentiality breaches. |