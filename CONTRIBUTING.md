# Contributing to The Vault

Welcome! We are excited that you are interested in contributing to **The Vault**. To maintain codebase health, security standards, and documentation consistency, please adhere to these guidelines.

## 🚀 Setup & Local Development

1. **Go Toolchain:** Ensure you have Go 1.22+ installed.
2. **Environment Configuration:** Copy/create a local configuration file (e.g., `.env`) specifying the PostgreSQL connection string and the 32-byte encryption `MASTER_KEY`.
3. **Download Dependencies:**

   ```bash
   go mod tidy
   ```

## 🧪 Testing Guidelines

Before submitting any Pull Request, verify that all tests pass:

* Run unit tests: `go test ./...`
* Ensure your endpoints have corresponding integration or mock handler tests.

## ✍️ Documentation & Swagger Updates

To keep documentation from drifting away from code updates, we run a pre-commit git hook.

### Pre-commit Verification

The pre-commit hook (`scripts/check-docs.py`) automatically runs:

1. **Swagger JSON syntax checks** to ensure it remains a valid OpenAPI 3.0 file.
2. **API route consistency checks** ensuring that any route defined with `HandleFunc` in Go has matching paths and HTTP methods defined in `docs/swagger.json`.
3. **Markdown link audits** to verify that relative paths within `.md` files point to real files.
4. **Git staged checks** enforcing that changes in `cmd/` or `internal/handler/` are accompanied by changes in documentation/Swagger files in the same commit.

### Installing the Hooks

To activate the pre-commit hook locally:

```bash
./scripts/setup-hooks.sh
```

### Bypassing the Hook

If your code changes are purely internal refactoring and do not affect the public API contract, you can bypass the hook by prefixing your git commit:

```bash
BYPASS_DOCS_CHECK=1 git commit -m "refactor(service): clean up memory safety routines"
```

Or use:

```bash
git commit --no-verify
```
