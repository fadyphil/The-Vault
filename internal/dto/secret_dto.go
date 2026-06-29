package dto

// THE comments are for me to understand WTH is going on since i've got to do it on my own

/*
# NOTE SECTION

    - Marshalling = Go struct -> JSON (to json)
	- Unmarshalling = JSON -> Go struct (from json)
	- Unlike flutter we have a dedicated DTO and 2 (from/to) methods here we only need two objects/structs
	- since structs don't hold functions we only need the structs and can implement an interface or something or manually wire it in
*/

// THIS is the unmarshal target
type CreateSecretRequest struct {
	Name           string
	PlaintextValue string
}

// in back-end it's called "UNMARSHALLING" the from json operation
// THIS is marshal source
type CreateSecretResponse struct {
	ID   string `json:"id"`
	Name string `json:"name"`
}
