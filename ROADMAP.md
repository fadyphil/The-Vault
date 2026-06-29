# 🗺️ The Vault: Project Roadmap

This document tracks the architectural milestones and development phases of The Vault.
The project is built iteratively, ensuring that each layer of the Clean Architecture is fully tested and conceptually sound before moving to the next.

## 🏆 Phase 1 & 2: Foundation & Transport Layer (COMPLETED)

The core skeleton of the application, focusing on strict data contracts and the HTTP network boundary.

- [x] **Project Initialization:** Standard Go Project Layout (`cmd/`, `internal/`).
- [x] **Domain Modeling:** Pure `Secret` entity with UUIDs, byte-slices for crypto, and time boundaries.
- [x] **Boundary Isolation:** Implementation of Request/Response DTOs to decouple network payloads from database models.
- [x] **Dependency Inversion:** Definition of the `SecretService` interface.
- [x] **HTTP Transport:** `SecretHandler` with streaming JSON decoding, guard clauses, and proper HTTP semantic status codes.
- [x] **Composition Root:** `main.go` wiring with `net/http` router and Mock Service stubbing for end-to-end testing.

## 🚧 Phase 3: The Cryptographic Engine (IN PROGRESS)

Replacing the Mock Service with real, memory-safe mathematics to secure data at rest.

- [ ] **Batch 1:** Build standalone AES-GCM encryption/decryption utilities (`internal/crypto`).
- [ ] **Batch 2:** Implement the real `SecretService` to orchestrate UUID generation and crypto sealing.
- [ ] **Batch 3:** Implement Environment Variable loading (`.env`) to securely inject the Master Key.

## 📅 Phase 4: The Data Access Layer (UPCOMING)

Connecting the Brain to the Muscle. Introduction of PostgreSQL and ACID transactions.

- [ ] **Database Schema:** Design the `secrets` and `audit_logs` tables.
- [ ] **Repository Pattern:** Implement the `SecretRepository` to handle SQL inserts and selects.
- [ ] **ACID Compliance:** Wrap Secret retrieval in strict database transactions (Read + Audit Log commit/rollback).
- [ ] **Dependency Wiring:** Inject the Postgres Repository into the Real Service.

## 🔮 Phase 5: Production Readiness & Security (FUTURE)

Hardening the API for real-world, hostile internet traffic.

- [ ] **Middleware:** Implement JWT Authentication to verify client identities.
- [ ] **Middleware:** Implement Rate Limiting to prevent brute-force attacks.
- [ ] **Observability:** Replace standard `log` with structured JSON logging (`slog` or `zap`).
- [ ] **Containerization:** Write a multi-stage `Dockerfile` to compile a minimal, secure Alpine image.
- [ ] **Testing:** Write Unit Tests for the Crypto engine and Integration Tests for the Repository.
