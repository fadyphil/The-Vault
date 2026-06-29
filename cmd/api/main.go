package main

import (
	"The-Vault/internal/domain"
	"The-Vault/internal/handler"
	"context"
	"net/http"
	"time"
)

type MockSecretService struct {
}

func (m *MockSecretService) CreateSecret(ctx context.Context, name string, plaintext string) (*domain.Secret, error) {
	return &domain.Secret{
		ID:         "isub",
		Name:       "anytihing",
		Ciphertext: []byte{},
		CreatedAt:  time.Now(),
		ExpiresAt:  time.Now(),
		Nonce:      []byte{},
	}, nil

}

func main() {
	mockservice := MockSecretService{}

	myhandler := handler.NewSecretHandler(&mockservice)

	mux := http.NewServeMux()
	mux.HandleFunc("POST /v1/secrets", myhandler.CreateSecret)
	http.ListenAndServe(":8080", mux)

}
