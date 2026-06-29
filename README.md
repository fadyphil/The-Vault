# The Vault 🔐

**The Vault** is a centralized, zero-trust Secrets Management System built in Go.
Instead of hardcoding sensitive API keys, passwords, and encryption keys into application source code, The Vault provides a secure, highly available API to fetch them at runtime.

## 🏗️ Architecture

The project strictly follows **Clean Architecture** principles to ensure separation of concerns, testability, and maintainability. The codebase is isolated into the following layers:

* **Handler (Transport Layer):** Speaks HTTP. Validates incoming JSON, checks auth headers, and formats responses.
* **Service (Business Logic Layer):** The brain. Orchestrates encryption/decryption, handles cryptographic keys in RAM, and enforces business rules.
* **Repository (Data Access Layer):** The muscle. Translates domain objects into SQL queries for PostgreSQL.
* **Domain (Core Entities):** Pure business structs (e.g., `Secret`) with zero external dependencies.

### Security Guarantees

* **Data at Rest:** The database *never* stores plaintext secrets. It only stores AES-GCM encrypted ciphertexts and cryptographic nonces.
* **Memory Safety:** Plaintext variables are dropped/overwritten in RAM immediately after encryption.
* **ACID Compliance:** Secret retrieval is wrapped in strict database transactions. It is mathematically impossible to decrypt and return a secret without simultaneously writing an immutable record to the Audit Log.

## 🛠️ Tech Stack

* **Language:** Go (1.22+)
* **Database:** PostgreSQL
* **Cryptography:** AES-GCM (Standard Library `crypto/cipher`)
* **Architecture:** Clean Architecture / Hexagonal Architecture

## 📁 Project Structure

```text
vault/
├── cmd/api/        # Application entrypoint and dependency wiring
├── internal/       # Private application code (enforced by Go compiler)
│   ├── domain/     # Core business entities
│   ├── dto/        # Data Transfer Objects (Network payloads)
│   ├── handler/    # HTTP Controllers
│   ├── service/    # Business logic and cryptography
│   ├── repository/ # Database interactions
│   └── crypto/     # Encryption utilities
└── migrations/     # SQL database migrations
```

## 🚀 Getting Started

*(Note: Instructions for running the app will be added once the `cmd/api/main.go` server is fully wired.)*

```bash
# Clone the repository
git clone https://github.com/yourusername/the-vault.git
cd the-vault

# Install dependencies
go mod tidy

# Run the server (Coming soon)
go run cmd/api/main.go
```

## 📖 API Endpoints

*(Note: Full Swagger/OpenAPI documentation will be generated as endpoints are built.)*

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/v1/secrets` | Securely encrypt and store a new secret. |
| `GET` | `/v1/secrets/{id}` | Retrieve and decrypt a secret (Requires Auth). |

---
