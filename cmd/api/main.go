package main

import (
	"The-Vault/internal/config"
	"The-Vault/internal/handler"
	"The-Vault/internal/service"
	"log"
	"net/http"

	"github.com/joho/godotenv"
)

func main() {
	err := godotenv.Load()
	if err != nil {
		log.Println("No .env file found, relying on OS environment variables")
	}
	key, err := config.LoadMasterKey()
	if err != nil {
		log.Fatalf("failed to start vault: %v", err)
	}

	svc := service.NewSecretService(key)
	secretHandler := handler.NewSecretHandler(svc)

	mux := http.NewServeMux()
	mux.HandleFunc("POST /v1/secrets", secretHandler.CreateSecret)
	http.ListenAndServe(":8080", mux)

}
