# System Design and Security Architecture

This document describes the design patterns, security boundaries, and data flows of **The Vault**.

## 🏗️ Architectural Overview

The Vault is designed around a **Clean Architecture** style, separating pure business logic from external frameworks, databases, and network transports.

```mermaid
graph TD
    subgraph Client ["Client Space (Flutter App)"]
        Plaintext["Plaintext Data"]
    end

    subgraph Memory ["RAM Boundary (Go Server Instance)"]
        Key["Master Key (32-bytes in-memory)"]
        Nonce["Cryptographic Nonce (Randomly generated)"]
        PlaintextText["Ephemeral Plaintext Value"]
        Sealer["AES-GCM Engine"]
        Ciphertext["Ciphertext Payload"]
    end

    subgraph Storage ["Persistent Storage (PostgreSQL)"]
        EncryptedRecord["Non-plaintext Record (Ciphertext + Nonce)"]
    end

    Plaintext -->|HTTPS Post| PlaintextText
    Key --> Sealer
    Nonce --> Sealer
    PlaintextText --> Sealer
    Sealer -->|Seal| Ciphertext
    Ciphertext -->|Write Transaction| EncryptedRecord
    Nonce -->|Write Transaction| EncryptedRecord
```

---

## 🔒 Security Guarantees & Memory Management

### Ephemeral Memory Handling

To prevent plaintext secrets from persisting in Go's managed memory (which is controlled by the Garbage Collector and may not be freed immediately), the system uses the following safeguards:

1. **Byte Arrays over Strings:** Plaintext values are stored in byte slices (`[]byte`) instead of Go `string` objects. Go strings are immutable and cannot be zeroed out in-place.
2. **Explicit Zeroing (Scrubbing):** Once the encryption/decryption process completes, the plaintext byte slices are explicitly overwritten with zeroes:

   ```go
   for i := range plaintextBytes {
       plaintextBytes[i] = 0
   }
   ```

---

## 🔄 Secret Retrieval Flow

Every secret read operation is strictly audited. An access token must be provided, and a log entry is written atomically before returning the plaintext.

```mermaid
sequenceDiagram
    autonumber
    actor C as Authorized Client
    participant API as Handler / Controller
    participant DB as PostgreSQL Repository
    participant Crypto as AES-GCM Engine

    C->>API: GET /v1/secrets/{id} (With Bearer Token)
    API->>API: Validate Token
    API->>DB: Begin DB Transaction
    DB->>DB: Fetch Encrypted Nonce & Ciphertext
    DB->>DB: Write Immutable Audit Log entry (Access Attempt)
    DB->>DB: Commit DB Transaction
    API->>Crypto: Decrypt Ciphertext using Master Key + Nonce
    Crypto-->>API: Return Decrypted Plaintext
    API-->>C: 200 OK (Plaintext Response)
```
