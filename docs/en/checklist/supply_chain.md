# 4.1.2. Supply Chain Security Checklist

The Supply Chain Security Checklist is for ensuring the reliability of the entire supply chain, including parts, firmware, and external libraries that make up the robot product. It includes SBOM management, vendor verification, and update source confirmation, aiming to prevent security risks that occur throughout the supply chain lifecycle.

| ID | Checklist Item | Description |
| :--- | :--- | :--- |
| SC-01 | Manage Open Source Software<br>Components | All components, including open-source software and external libraries included in the product, must be identified and managed. |
| SC-02 | Manage EoS | Components must not be in an End-of-Support (EoS) state, and EoS must be managed to maintain security patches and technical support from the time of introduction. |
| SC-03 | Establish and Apply<br>Vendor Security Capability<br>Assessment Criteria | The organization must establish and apply security capability assessment criteria to minimize security risks when selecting vendors for supply components. |
| SC-04 | Prepare for Security Impact<br>Assessment and Response to<br>Supply Chain Changes | The organization must have a plan to assess and respond to the security impact of changed vendors/components in the event of a supply chain change. |
| SC-05 | Manage Component<br>Vulnerabilities | Known vulnerability information must be identified and managed along with the version, license, and patch status of each component. |
| SC-06 | Verify Integrity of Robot<br>Firmware and Software<br>Updates | The organization must establish an integrity verification system to prevent security threats such as malware insertion and unauthorized tampering during the firmware and software update process of the robot system. |
| SC-07 | Implement Rapid Patch<br>Mechanism | A mechanism for rapid patch distribution and application must be established when vulnerabilities are discovered in supply chain components. |