package config

import (
	"encoding/hex"
	"errors"
	"os"
)

func LoadMasterKey() ([]byte, error) {
	key, ok := os.LookupEnv("VAULT_MASTER_KEY")
	if !ok {
		return nil, errors.New("config: missing VAULT_MASTER_KEY environment variable")
	}
	keyInBytes, err := hex.DecodeString(key)
	if err != nil {
		return nil, err
	}
	if len(keyInBytes) != 32 {
		return nil, errors.New("config: master key must be exactly 256 bits/32 bytes")
	}
	return keyInBytes, nil
}
