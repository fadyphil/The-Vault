package domain

import (
	"time"
)

type Secret struct {
	ID         string
	Name       string
	Ciphertext []byte
	Nonce      []byte
	CreatedAt  time.Time
	ExpiresAt  time.Time
}
