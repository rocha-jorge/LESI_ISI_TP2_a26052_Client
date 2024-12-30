import requests
import json
from zeep import Client
# token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InN0cmluZyIsInJvbGUiOiJhZG1pbiIsIm5iZiI6MTczNTUxOTUwNSwiZXhwIjoxNzM1NTIwNDA1LCJpYXQiOjE3MzU1MTk1MDV9.2125UCi5iJXjWB-iVePYs3Saf05Rt_Zm6ALVCU1oESk"

# Function to get JWT Token
def get_jwt_token(auth_url):

    print("\nInputs for authentication:")
    roles = input("Indique um ou mais roles (admin/guest): ").strip()

    user_credentials = {
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "name": "string",
        "email": "string",
        "password": "string",
        "roles": [roles]
    }

    try:
        response = requests.post(auth_url, json=user_credentials)
        print("Status Code da resposta:", response.status_code)
        print("Body da resposta:", response.text)

        if response.status_code == 200:
            token = response.text.strip()
            print("JWT token obtido com sucesso.")
            return token
        else:
            print(f"Erro ao obter JWT token: {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao tentar obter JWT token: {e}")
        return None

# GET TODAS AS TRANSACOES DE UM USER
def get_user_transactions(transaction_user_api_url, idUser, headers=None):
    url = f"{transaction_user_api_url}/{idUser}"
    print(f"URL chamada: {url}")
    print(f"Headers enviados: {headers}")  # Debug header

    try:
        response = requests.get(url, headers=headers)
        print("Status Code da resposta:", response.status_code)
        print("Body da resposta:", response.text)

        if response.status_code == 200:
            transactions = response.json()
            print("Transações obtidas com sucesso:")
            print(json.dumps(transactions, indent=4, ensure_ascii=False))
            return transactions
        else:
            print(f"Erro ao obter as transações do utilizador: {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao tentar obter as transações do utilizador: {e}")
        return None

# REGISTAR TRANSACAO
def post_transaction(api_url, post_transaction_payload, headers=None):
    json_payload = json.dumps(post_transaction_payload)
    print("Payload enviada:", json_payload)
    headers = headers or {"Content-Type": "application/json"}
    response = requests.post(api_url, data=json_payload, headers=headers)

    print("Status Code da resposta:", response.status_code)
    print("Body da resposta:", response.text)

    if response.status_code == 200 or response.status_code == 201:
        print("Transacao registada com sucesso")
        print("Detalhes da resposta:", response.json())
        return response.json()
    else:
        print(f"Falha ao registar a transacao: {response.text}")
        return None

# OBTER INFORMAÇÃO SOBRE UMA TRANSAÇÃO
def get_transaction(transaction_api_url, idTransaction, headers=None):
    url = f"{transaction_api_url}/{idTransaction}"
    print(f"URL chamada: {url}")

    try:
        response = requests.get(url, headers=headers)
        print("Status Code da resposta:", response.status_code)
        print("Body da resposta:", response.text)

        if response.status_code == 200:
            print("Informação da transação obtida com sucesso:")
            transaction_info = response.json()
            print(json.dumps(transaction_info, indent=4, ensure_ascii=False))  # Pretty print JSON response
            return transaction_info
        else:
            print(f"Erro ao obter a informação da transação: {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao tentar obter a transação: {e}")
        return None

# ATUALIZAR TRANSACAO
def put_transaction(transaction_api_url, put_transaction_payload, headers=None):
    json_payload = json.dumps(put_transaction_payload)
    print("Payload enviada:", json_payload)
    headers = headers or {"Content-Type": "application/json"}
    response = requests.put(transaction_api_url, data=json_payload, headers=headers)

    print("Status Code da resposta:", response.status_code)
    print("Body da resposta:", response.text)

    if response.status_code == 204 or response.status_code == 200:
        print("Transação atualizada com sucesso")
    else:
        print(f"Falha ao atualizar a transação: {response.text}")
        return None

# APAGAR TRANSACAO
def delete_transaction(transaction_api_url, idTransaction, headers=None):
    url = f"{transaction_api_url}/{idTransaction}"
    print(f"URL chamada: {url}")

    try:
        response = requests.delete(url, headers=headers)
        print("Status Code da resposta:", response.status_code)
        print("Body da resposta:", response.text)

        if response.status_code == 200 or response.status_code == 204:
            print("Transação apagada com sucesso.")
            return None
        else:
            print(f"Erro ao apagar a transação: {response.text}")
            return None
    except Exception as e:
        print(f"Erro ao tentar apagar a transação: {e}")
        return None

# TOTAL DE BITCOIN DE UM USER
def get_total_bitcoins(soap_wsdl, idUser):
    try:
        soap_client = Client(soap_wsdl)
        response = soap_client.service.GetTotalUnitsForUser(idUser=idUser)
        return float(response)
    except Exception as e:
        print(f"Erro a obter o valor total de Bitoins do idUser: {e}")
        return None

# PREÇO DA BITCOIN
def get_bitcoin_price(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data["bitcoin"]["usd"]
        else:
            print(f"Erro a obter o preço de cada Bitcoin.: {response.text}")
            return None
    except Exception as e:
        print(f"Erro a obter o preço de cada Bitcoin.: {e}")
        return None

# VALIDAR INPUT
def get_validated_input(prompt, required=True, input_type=str, validation_fn=None):
    while True:
        user_input = input(prompt).strip()
        if required and not user_input:
            print("Input não pode ser vazio. Por favor tente novamente.")
            continue
        try:
            if input_type:
                user_input = input_type(user_input)
            if validation_fn and not validation_fn(user_input):
                print("Input inválido. Por favor tente novamente.")
                continue
            return user_input
        except ValueError:
            print(f"Input tem de ser do tipo {input_type.__name__}. Por favor tente novamente.")