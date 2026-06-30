# Security Policy and Cryptographic Model

This document outlines the security architecture, cryptographic safeguards, threat model, and vulnerability reporting procedures for **The Vault**.

## 🛡️ Threat Model

The Vault assumes a **zero-trust** network architecture. We operate under the assumption that:

1. The database storage layer can be compromised.
2. Network traffic can be intercepted.
3. Memory dumps may be attempted on application instances.

### Mitigations

* **Compromised Storage:** Plaintext secrets are never stored. Data is encrypted using AES-GCM (256-bit) with unique random nonces generated per secret. Compromising the database does not reveal secrets without the master key.
* **Network Interception:** All endpoints must be served over HTTPS. JWT or strong Bearer tokens are required for all non-registration endpoints.
* **RAM Dump Mitigation:** Plaintext secrets are cleared or overwritten in memory as soon as they are processed.

## 🔑 Key Management

The Vault uses a single Master Key to derive or directly encrypt data at rest.

* The Master Key is injected at runtime via environment variables or a secure key store (e.g., AWS KMS, HashiCorp Vault).
* It is **never** written to disk.
* Key rotation policies should be run periodically to re-encrypt old ciphertexts.

## 🚨 Reporting a Vulnerability

If you discover a security vulnerability within this project, please do **not** open a public issue. Instead, report it securely:

1. Send an email to `security@example.com` (replace with your secure reporting channel).
2. Include a detailed description of the vulnerability, steps to reproduce, and any proof of concept.
3. We will acknowledge receipt of your report within 24 hours and coordinate a public release timeline with you.
