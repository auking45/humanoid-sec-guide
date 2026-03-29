# Humanoid Security Guide (HSG) 🤖🛡️

> **Technical Security Specification for High-End Humanoid Robots.**
> Fully adopted from the **KISA Robot Security Model (2025)** framework.

---

## 🌟 Overview

The **Humanoid Security Guide (HSG)** defines critical security requirements and architectural blueprints for the design and operation of humanoid robots. This project translates high-level regulatory guidelines into technical specifications for high-performance robotic systems.

By aligning with South Korea's official **KISA Robot Security Model**, this guide provides a robust baseline for securing hardware-software convergence in robotics.

---

## 🏛️ Security Framework (Fully Adopted)

HSG categorizes security controls into four core domains, as defined by the national guidelines, with a specialized focus on humanoid-specific attack vectors.

### 1. Hardware Security
* **Root of Trust (RoT)**: Establishing a chain of trust from the hardware level (Secure Boot).
* **Cryptographic Isolation**: Secure storage for identity keys using TPM 2.0 or TEE (TrustZone).
* **Physical Hardening**: Disabling debug interfaces (JTAG/UART) and implementing chassis intrusion detection.

### 2. Network Security
* **Cloud Communication**: Implementing Mutual TLS (mTLS 1.3) for secure data exchange with Cloud AI (VLM) platforms.
* **Local Network Isolation**: Establishing strict access control between the User PC (UPC) and the Robot PC (RPC) to prevent lateral movement.

### 3. System Software Security
* **Integrity Monitoring**: Real-time auditing of system calls, source code access, and core control binaries.
* **Secure Logging**: Enforcing immutable audit logs and defined storage quotas for forensic reliability.

### 4. Application Security
* **Control Integrity**: Digital signing and verification of remote control commands.
* **Data Privacy**: Edge-side de-identification of sensor data (Vision/Audio) before cloud transmission.

---

## 📊 Project Ecosystem

* **[humanoid-sec (Dashboard)](https://github.com/auking45/humanoid-sec)**: A real-time monitoring dashboard designed to visualize the security events and compliance status defined in this guide.

---

## 🚀 Getting Started

This guide is built with **MkDocs**. To browse the documentation locally:

```bash
# Install dependencies
pip install mkdocs-material

# Run local server
mkdocs serve
