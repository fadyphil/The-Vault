package crypto

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"errors"
	"io"
)

func Encrypt(plaintext []byte, masterkey []byte) ([]byte, []byte, error) {
	if len(masterkey) != 32 {
		return nil, nil, errors.New("invalid master key size\nMust be exactly 256 bits/32 bytes")
	}
	cipherblock, err := aes.NewCipher(masterkey)
	if err != nil {
		return nil, nil, err
	}
	gcmmode, err := cipher.NewGCM(cipherblock)
	if err != nil {
		return nil, nil, err
	}
	nonce := make([]byte, gcmmode.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, nil, err
	}

	ciphertext := gcmmode.Seal(nil, nonce, plaintext, nil)
	clear(plaintext)

	return ciphertext, nonce, nil

}
