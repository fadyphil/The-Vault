package service

import (
	"The-Vault/internal/crypto"
	"The-Vault/internal/domain"
	"context"
	"time"

	"github.com/google/uuid"
)

type SecretService interface {
	CreateSecret(ctx context.Context, name string, plaintext string) (*domain.Secret, error)
}

type secretService struct {
	masterkey []byte
}

func NewSecretService(masterkey []byte) SecretService {
	return &secretService{
		masterkey: masterkey,
	}
}

func (s *secretService) CreateSecret(ctx context.Context, name string, plaintext string) (*domain.Secret, error) {
	key := s.masterkey
	textBytes := []byte(plaintext)
	cypherText, nonce, err := crypto.Encrypt(textBytes, key)
	if err != nil {
		return nil, err
	}
	secret := domain.Secret{
		ID:         uuid.NewString(),
		Name:       name,
		Ciphertext: cypherText,
		Nonce:      nonce,
		CreatedAt:  time.Now(),
		ExpiresAt:  time.Now().Add(time.Hour),
	}
	return &secret, nil
}
