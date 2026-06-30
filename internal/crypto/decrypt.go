package crypto

import (
	"crypto/aes"
	"crypto/cipher"
	"errors"
)

const masterKeySize = 32
const nonceSize = 12

func Decrypt(ciphertext []byte, masterkey []byte, nonce []byte) ([]byte, error) {

	if len(masterkey) != masterKeySize {
		return nil, errors.New("crypto: master key must be exactly 256 bits/32 bytes")
	}

	if len(nonce) != nonceSize {
		return nil, errors.New("crypto: Nonce must be 96 bits/12 bytes")
	}
	cipherblock, err := aes.NewCipher(masterkey)
	if err != nil {
		return nil, err
	}

	gcmmode, err := cipher.NewGCM(cipherblock)
	if err != nil {
		return nil, err
	}

	plaintext, err := gcmmode.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return nil, err
	}
	return plaintext, nil
}
