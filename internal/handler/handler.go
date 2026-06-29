package handler

import (
	"The-Vault/internal/dto"
	"The-Vault/internal/service"
	"encoding/json"
	"log"
	"net/http"
)

/*
This is the wa dep injection looks here
there is no constructor
we declare a struct and take in the service
*/
type SecretHandler struct {
	svc service.SecretService
}

// This is how consttructor is made
func NewSecretHandler(svc service.SecretService) *SecretHandler {
	return &SecretHandler{
		svc: svc,
	}
}

func (s *SecretHandler) CreateSecret(w http.ResponseWriter, r *http.Request) {
	// we create the dto to take the json into it
	mydto := dto.CreateSecretRequest{}
	err := json.NewDecoder(r.Body).Decode(&mydto)

	// error to validate the correctness of the incoming data
	if err != nil {
		w.WriteHeader(http.StatusBadRequest)
		log.Println("wrong info sent", err)
		return
	}

	// now we get the reference to the created domain secret
	secret, err := s.svc.CreateSecret(r.Context(), mydto.Name, mydto.PlaintextValue)

	// error checking for internal errors
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Println("failed to create secret", err)
		return
	}

	// now we map the json to the dto object using the from json like struct
	response := dto.CreateSecretResponse{
		ID:   secret.ID,
		Name: secret.Name,
	}

	// update: now ik why that it is
	//    that is the universal HTTP rules
	//	  the `Content-type` is to tell the content type (img,text,etc..) since the clinet recieves raw bytes
	//    the other tells the client to use their json parser
	w.Header().Set("Content-type", "application/json")
	w.WriteHeader(http.StatusCreated)

	err = json.NewEncoder(w).Encode(response)

	if err != nil {
		log.Println("error encoding response", err)
		return
	}

}
