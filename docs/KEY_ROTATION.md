# Master Key Rotation Runbook

This document describes the operational procedure to rotate the Master Key used by **The Vault** for database encryption at rest.

## 🔄 Overview

Key rotation is critical for compliance and security hygiene. Because The Vault uses envelope/symmetric encryption, we support **Online Zero-Downtime Key Rotation** using a transitional dual-key configuration.

---

## 🏃 Rotation Procedure

### Phase 1: Dual-Key Mode Injection

When introducing a new master key, configure the Vault instance with both keys:

1. **`MASTER_KEY_PRIMARY`**: The new master key to use for all new write operations.
2. **`MASTER_KEY_SECONDARY`**: The previous master key, used as a fallback to decrypt old secrets when reading.

During this phase, any `GET` request will check if decryption with the primary key fails; if so, it falls back to the secondary key, decrypts it, and optionally updates the row in the background with the primary key.

### Phase 2: Batch Re-encryption (Migration)

Run the migration CLI tool to re-encrypt all legacy database records:

```bash
go run cmd/cli/main.go rotate-keys --old-key-env MASTER_KEY_SECONDARY --new-key-env MASTER_KEY_PRIMARY
```

This tool:

1. Iterates over all secrets in the repository.
2. Decrypts each secret ciphertext with the secondary key.
3. Generates a new cryptographically random nonce.
4. Encrypts the plaintext using the primary key.
5. Saves the updated ciphertext and nonce back to the database.

### Phase 3: Primary-Only Cleanup

Once all secrets have been re-encrypted:

1. Revoke the secondary key.
2. Update the environment configuration, setting the new primary key as the sole `MASTER_KEY`.
3. Restart the Vault instances.
