# Description

Provide a clear description of what this Pull Request does, why it is needed, and any related issue link (e.g., Closes #123).

## Type of Change

- [ ] 🐛 Bug fix (non-breaking change which fixes an issue)
- [ ] ✨ New feature (non-breaking change which adds functionality)
- [ ] 💥 Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] 📝 Documentation / Swagger update
- [ ] ⚙️ CI/CD, tooling, or repository scripts

## 🔐 Security & Cryptographic Checklist

*This section is mandatory for any changes touching internal/crypto, internal/service, or database schemas.*

- [ ] **No Plaintext Leakage:** Plaintext values are zeroed out or dropped from memory as soon as encryption/decryption finishes.
- [ ] **Nonce Uniqueness:** AES-GCM nonces are cryptographically random and unique for every single encryption.
- [ ] **Audit Trail Integrity:** Any access or decryption of a secret is tied atomically to a write operation in the Audit Log database repository.
- [ ] **Sanitized Logs:** No plaintext secrets or master keys are printed in error messages, stack traces, or logger outputs.

## 🧪 How Has This Been Tested?

Describe the tests you ran to verify your changes. Provide instructions so we can reproduce.

- [ ] **Unit Tests:** `go test ./...`
- [ ] **Integration Tests:** (e.g., PostgreSQL DB tests)
- [ ] **Documentation Verification:** `python3 scripts/check-docs.py` ran successfully.

## Checklist

- [ ] My code follows the style guidelines of this project.
- [ ] I have performed a self-review of my own code.
- [ ] I have commented my code, particularly in hard-to-understand areas.
- [ ] I have updated the documentation / Swagger spec (`docs/swagger.json`) accordingly.
- [ ] My changes generate no new warnings or lint errors.
- [ ] I have added tests that prove my fix is effective or that my feature works.
