package service

import (
	"The-Vault/internal/domain"
	"context"
)

type SecretService interface {
	CreateSecret(ctx context.Context, name string, plaintext string) (*domain.Secret, error)
}
