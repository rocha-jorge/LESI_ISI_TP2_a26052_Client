import requests
import json
from zeep import Client

# Function to send Bitcoin transaction
def send_transaction(api_url, payload):
    json_payload = json.dumps(payload)
    print("Payload being sent:", json_payload)  # Debugging the payload
    headers = {"Content-Type": "application/json"}  # Explicitly set content type
    response = requests.post(api_url, data=json_payload, headers=headers)

    print("Response Status Code:", response.status_code)
    print("Response Body:", response.text)

    if response.status_code == 200 or response.status_code == 201:
        print("Transaction registered successfully.")
        print("Response details:", response.json())
        return response.json()  # Return the API response if needed
    else:
        print(f"Failed to register transaction: {response.text}")
        return None

# Function to get total Bitcoins for an idUser
def get_total_bitcoins(soap_wsdl, id_user):
    try:
        soap_client = Client(soap_wsdl)
        response = soap_client.service.GetTotalUnitsForUser(idUser=id_user)
        return float(response)
    except Exception as e:
        print(f"Error fetching total Bitcoins: {e}")
        return None

# Function to get current Bitcoin price
def get_bitcoin_price(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            return data["bitcoin"]["usd"]
        else:
            print(f"Failed to fetch Bitcoin price: {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching Bitcoin price: {e}")
        return None

# Utility function to get validated input
def get_validated_input(prompt, required=True, input_type=str, validation_fn=None):
    while True:
        user_input = input(prompt).strip()
        if required and not user_input:
            print("Input cannot be blank. Please try again.")
            continue
        try:
            if input_type:
                user_input = input_type(user_input)
            if validation_fn and not validation_fn(user_input):
                print("Invalid input. Please try again.")
                continue
            return user_input
        except ValueError:
            print(f"Input must be of type {input_type.__name__}. Please try again.")

# Main menu function
def main():
    transaction_api_url = "https://bitcoinappisia26052-a4dbf7g9e3fsg8eu.spaincentral-01.azurewebsites.net/api/Transaction"
    bitcoin_price_api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    soap_wsdl_url = "https://bitcoinappsoap-drfmetbvf7dfcjcn.spaincentral-01.azurewebsites.net/UserBalanceSOAPService.svc?wsdl"

    while True:
        print("\nChoose an option:")
        print("1. Get the total value of Bitcoin for an idUser")
        print("2. Get the total amount of Bitcoin for an idUser")
        print("3. Register a new transaction")
        print("4. Exit")
        choice = get_validated_input("Enter your choice (1/2/3/4): ", input_type=int, validation_fn=lambda x: 1 <= x <= 4)

        if choice == 1:
            print("\nTemplate for Option 1: Get the total value of Bitcoin for an idUser")
            id_user = get_validated_input("Enter idUser: ", input_type=int)
            total_bitcoins = get_total_bitcoins(soap_wsdl_url, id_user)
            if total_bitcoins is not None:
                bitcoin_price = get_bitcoin_price(bitcoin_price_api_url)
                if bitcoin_price is not None:
                    total_value = total_bitcoins * bitcoin_price
                    print(f"Total value of Bitcoin for idUser {id_user}: {total_value:.2f} USD")
                else:
                    print("Unable to fetch Bitcoin price.")
            else:
                print("Unable to fetch total Bitcoins.")

        elif choice == 2:
            print("\nTemplate for Option 2: Get the total amount of Bitcoin for an idUser")
            id_user = get_validated_input("Enter idUser: ", input_type=int)
            total_bitcoins = get_total_bitcoins(soap_wsdl_url, id_user)
            if total_bitcoins is not None:
                print(f"Total amount of Bitcoin for idUser {id_user}: {total_bitcoins:.8f}")
            else:
                print("Unable to fetch total Bitcoins.")

        elif choice == 3:
            print("\nTemplate for Option 3: Register a new transaction")
            id_user = get_validated_input("Enter idUser: ", input_type=int)
            transaction_type = get_validated_input("Enter transaction type (buy/sell): ", validation_fn=lambda x: x.lower() in {"buy", "sell"}).lower()
            units = get_validated_input("Enter units of Bitcoin: ", input_type=int)
            btc_timestamp = get_validated_input("Enter timestamp (YYYY-MM-DDTHH:MM:SS.sss): ", validation_fn=lambda x: len(x.split("T")) == 2 and "." in x)

            transaction_payload = {
                "idUser": id_user,
                "transactionType": transaction_type,
                "units": units,
                "btcTimeStamp": btc_timestamp,
            }

            send_transaction(transaction_api_url, transaction_payload)

        elif choice == 4:
            print("Exiting program.")
            break

if __name__ == "__main__":
    main()
