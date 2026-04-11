# Humanoid-Specific Hardware Security Requirements

This document outlines advanced hardware-level security requirements, tailored specifically for the heterogeneous (x86-NVIDIA) board architecture and physical characteristics of humanoid robots. The detailed security requirements are as follows.

| ID | Category | Security Requirement | Detailed Requirements |
| :--- | :--- | :--- | :--- |
| **HDW-01** | Hardware Trust & Integrity | **Secure Boot** | Enforce full signature verification at all boot stages using custom keys embedded in UEFI (x86) and MB1/MB2 (NVIDIA). |
| **HDW-02** | Hardware Trust & Integrity | **Anti-Rollback** | Leverage hardware eFuses or secure counters to physically block the execution of downgraded, vulnerable firmware versions. |
| **HDW-03** | Hardware Trust & Integrity | **TEE/TPM** | Generate and store all private cryptographic keys strictly within a TEE (OP-TEE) or TPM 2.0, preventing extraction to the normal OS environment. |
| **HDW-04** | Hardware Trust & Integrity | **PUF (Physical Unclonable Function)** | Utilize unique, physical chip characteristics (PUF) to generate immutable device IDs, preventing hardware cloning and issuing tied certificates. |
| **HDW-05** | Physical Access Control & Isolation | **Disable JTAG/UART** | Physically or logically disable hardware debugging ports (via fuse blowing) in all mass-production and partner-distributed units. |
| **HDW-06** | Physical Access Control & Isolation | **Memory Isolation** | Enable the IOMMU to enforce hardware-level isolation, preventing device drivers from accessing unauthorized memory regions (e.g., between AI models and control logic). |
| **HDW-07** | Physical Access Control & Isolation | **Physical Intrusion Detection** | Equip the robot chassis with light sensors or mechanical switches. Upon unauthorized opening, automatically trigger the destruction (Self-Destruction) of cryptographic keys inside the TEE. |
| **HDW-08** | Physical Access Control & Isolation | **Fail-over Sync** | Implement independent watchdog circuits monitoring the ethernet link between NVIDIA and x86 boards at a 1ms interval. Engage hardware brakes immediately upon physical disconnection. |
