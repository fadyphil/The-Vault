# API Integration Guide

This document provides a developer-friendly guide on how to integrate and communicate with **The Vault API**.

## 🔐 Authentication

All request paths (except endpoints marked public) require Bearer Authentication:

```http
Authorization: Bearer <your_access_token>
```

Tokens are verified at the gateway/handler layer. Failing to provide a valid token results in a `401 Unauthorized` response.

## 📁 Endpoints

### 1. Store a Secret

* **Method:** `POST`
* **Path:** `/v1/secrets`
* **Headers:** `Content-Type: application/json`
* **Body:**

  ```json
  {
    "Name": "db-connection-string",
    "PlaintextValue": "postgresql://user:pass@localhost:5432/db"
  }
  ```

* **Success Response:** `201 Created`

  ```json
  {
    "id": "abc-123-xyz",
    "name": "db-connection-string"
  }
  ```

### 2. Retrieve a Secret

* **Method:** `GET`
* **Path:** `/v1/secrets/{id}`
* **Headers:** `Authorization: Bearer <token>`
* **Success Response:** `200 OK`

  ```json
  {
    "id": "abc-123-xyz",
    "name": "db-connection-string",
    "plaintext": "postgresql://user:pass@localhost:5432/db",
    "created_at": "2026-06-29T17:27:08Z"
  }
  ```

## ⚠️ Error Handling

The API returns standardized JSON error responses for client and server errors:

```json
{
  "error": "The requested secret was not found.",
  "code": "SECRET_NOT_FOUND"
}
```

### Common Error Codes

* `INVALID_PAYLOAD`: The request body could not be decoded.
* `UNAUTHORIZED`: Invalid or missing authentication headers.
* `SECRET_NOT_FOUND`: The secret ID does not exist in the database.
* `INTERNAL_ERROR`: A server-side issue occurred during cryptographic sealing or database write.
