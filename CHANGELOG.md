# Changelog

All notable changes to The Vault project will be documented in this file.

## [Unreleased]

### Added

- Architectural blueprint for AES-GCM cryptographic engine.
- Real Service layer implementation plan.

## [0.2.0] - Phase 2: HTTP Transport Layer

### Added

- `internal/handler`: HTTP Bouncer with JSON unmarshaling, guard clauses, and dependency injection.
- `internal/dto`: Strict network contracts (`CreateSecretRequest`, `CreateSecretResponse`).
- `cmd/api/main.go`: Composition root with `net/http` routing and Mock Service stubbing.
- Successful end-to-end POST request lifecycle (201 Created).

## [0.1.0] - Phase 1: Core Architecture & Contracts

### Added

- Standard Go Project Layout initialized (`cmd`, `internal`, `migrations`).
- `internal/domain`: Pure `Secret` entity with UUID, Ciphertext, and Nonce fields.
- `internal/service`: `SecretService` interface defining the Clean Architecture boundary.
