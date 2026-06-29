# Current State: Class Diagram (Clean Architecture)

This shows how your layers interact and how the Mock vs. Real service will plug into the interface.

```mermaid
classDiagram
    class SecretHandler {
        -svc SecretService
        +CreateSecret(w http.ResponseWriter, r *http.Request)
        +NewSecretHandler(svc SecretService) *SecretHandler
    }
    
    class SecretService {
        <<interface>>
        +CreateSecret(ctx context.Context, name string, plaintext string) (*domain.Secret, error)
    }
    
    class MockSecretService {
        +CreateSecret(ctx, name, plaintext) (*domain.Secret, error)
    }
    
    class RealSecretService {
        -masterKey []byte
        +CreateSecret(ctx, name, plaintext) (*domain.Secret, error)
    }

    SecretHandler --> SecretService : depends on abstraction
    MockSecretService ..|> SecretService : implements (Phase 2)
    RealSecretService ..|> SecretService : implements (Phase 3)
```

## Upcoming State: Sequence Diagram (The Cryptographic Flow)

This maps out the exact data flow we are about to implement in Phase 3.

```mermaid
sequenceDiagram
    participant C as Flutter Client
    participant H as Handler (Bouncer)
    participant S as Real Service (Brain)
    participant Crypto as AES-GCM Engine

    C->>H: POST /v1/secrets (JSON Payload)
    H->>H: Unmarshal JSON to CreateSecretRequest DTO
    H->>S: CreateSecret(ctx, name, plaintext)
    
    S->>Crypto: Generate random Nonce
    Crypto-->>S: Return []byte Nonce
    
    S->>Crypto: Seal(plaintext, Nonce, MasterKey)
    Crypto-->>S: Return []byte Ciphertext
    
    S->>S: Map to domain.Secret
    S-->>H: Return *domain.Secret, nil
    
    H->>H: Map to CreateSecretResponse DTO
    H->>C: 201 Created (JSON with ID & Name)
```
