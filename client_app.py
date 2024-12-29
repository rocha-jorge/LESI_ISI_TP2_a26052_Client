from methods import *

# MAIN
def main():
    transaction_api_url = "https://bitcoinappisia26052-a4dbf7g9e3fsg8eu.spaincentral-01.azurewebsites.net/api/Transaction"
    transaction_user_api_url = "https://bitcoinappisia26052-a4dbf7g9e3fsg8eu.spaincentral-01.azurewebsites.net/api/Transaction/user"
    bitcoin_price_api_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    soap_wsdl_url = "https://bitcoinappsoap-drfmetbvf7dfcjcn.spaincentral-01.azurewebsites.net/UserBalanceSOAPService.svc?wsdl"
    auth_url = "https://conexaoexcelapi-dnhtg3b8f3f7e6fv.southeastasia-01.azurewebsites.net/Authenticate"
    jwt_token = None

    while True:
        print("\nMenu:")

        print("\tServiços que combinam SOAP, desenvolvido internamente, e API externa:")
        print("\t\t1. Obter o valor total de Bitcoin, em USD, para um idUser.")

        print("\n\tServiços SOAP internos:")
        print("\t\t2. Obter a quantidade total de Bitcoin de um idUser.")
        
        print("\n\tServiços RESTFUL internos:")
        print("\t\t3. Obter token de autenticação.")
        print("\t\t4. Autenticar com o token obtido.")   
        # print("\t\t5. Obter informação sobre as transações de um utilizador (GET/READ).")  FALTA FAZER ESTEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE
        print("\t\t6. Registar uma nova transação (POST/CREATE).")
        print("\t\t7. Obter informação sobre uma transação (GET/READ).")
        print("\t\t8. Alterar informação de uma transação (PUT/UPDATE).")
        print("\t\t9. Apagar uma transação (DELETE/DELETE).")

        print("\n\t10. Sair da script.\n")
        choice = get_validated_input("Escolha a opção: ", input_type=int, validation_fn=lambda x: 0 <= x <= 9)

        # 1. Obter o valor total de Bitcoin, em USD, para um idUser
        if choice == 1: 
            print("Inputs:")
            print(" - idUser: (ex: 1)")
            id_user = get_validated_input("Introduza idUser: ", input_type=int)
            total_bitcoins = get_total_bitcoins(soap_wsdl_url, id_user)
            if total_bitcoins is not None:
                bitcoin_price = get_bitcoin_price(bitcoin_price_api_url)
                if bitcoin_price is not None:
                    total_value = total_bitcoins * bitcoin_price
                    print(f"Valor em Bitcoin do idUser {id_user}: {total_value:.2f} USD")
                else:
                    print("Erro a obter o preço de cada Bitcoin.")
            else:
                print("Erro a obter o valor total de Bitoins do idUser.")

        # 2. Obter a quantidade total de Bitcoin de um idUser
        elif choice == 2:
            print("Inputs:")
            print(" - idUser: (ex: 1)")
            id_user = get_validated_input("Introduza o idUser: ", input_type=int)
            total_bitcoins = get_total_bitcoins(soap_wsdl_url, id_user)
            if total_bitcoins is not None:
                print(f"Total de Bitcoin do idUser {id_user}: {total_bitcoins:.8f}")
            else:
                print("Não foi possível obter o total de Bitcoins.")

        # 3. Obter token de autenticação.
        elif choice == 3:  
            jwt_token = get_jwt_token(auth_url)
            if jwt_token:
                print("Token armazenado com sucesso.")
            else:
                print("Erro ao obter o token.")

        # 4. Autenticar com o token obtido.
        elif choice == 4:  
            if jwt_token:
                print(f"Token atual: {jwt_token}")
            else:
                print("Nenhum token armazenado. Por favor requisite o token primeiro.")

        # 5. Get all transactions for a user
        elif choice == 5:  # Get all transactions for a user
            print("Inputs:")
            print(" - idUser: (ex: 1)")
            user_id = get_validated_input("Introduza o idUser: ", input_type=int)
            transactions = get_user_transactions(transaction_user_api_url, user_id)
            if transactions:
                print(f"Transações do idUser {user_id} obtidas com sucesso.")
            else:
                print("Erro ao obter as transações.")

        # 6. Obter informação sobre uma transação
        elif choice == 6:
            print("Inputs:")
            print(" - idTransaction: (ex: 1)")
            idTransaction = get_validated_input("Introduza o idTransaction da transação: ", input_type=int)
            get_transaction(transaction_api_url,idTransaction)

        # 7. Registar uma nova transação
        elif choice == 7:
            print("Inputs:")
            print(" - idUser: (ex: 1)")
            print(" - transactionType: 'buy' ou 'sell'")
            print(" - units: numero de bitcoins (ex: 3)")
            print(" - btcTimeStamp: tem de ser 2024-12-22T23:39:30.700 (unico timestamp na entidade btcTimeStamp na BD)")

            id_user = get_validated_input("Introduzir idUser: ", input_type=int)
            transaction_type = get_validated_input("Introduzir transactionType (buy/sell): ", validation_fn=lambda x: x.lower() in {"buy", "sell"}).lower()
            units = get_validated_input("Introduzir units: ", input_type=int)
            btc_timestamp = get_validated_input("Introduzir timestamp (YYYY-MM-DDTHH:MM:SS.sss). Tem de ser 2024-12-22T23:39:30.700 (unico timestamp na entidade btcTimeStamp na BD): ", validation_fn=lambda x: len(x.split("T")) == 2 and "." in x)

            post_transaction_payload = {
                "idUser": id_user,
                "transactionType": transaction_type,
                "units": units,
                "btcTimeStamp": btc_timestamp,
            }

            post_transaction(transaction_api_url, post_transaction_payload)

        # 8. Alterar informação de uma transação
        elif choice == 8:
            print("Inputs:")
            print(" - idTransaction: (ex: 1)")
            print(" - idUser: (ex: 1)")
            print(" - transactionType: 'buy' ou 'sell'")
            print(" - units: numero de bitcoins (ex: 3)")
            print(" - btcTimeStamp: (tem de ser 2024-12-22T23:39:30.700 porque é o unico timestamp na entidade btcTimeStamp na BD):")

            idTransaction = get_validated_input("Introduza o idTransaction da transação: ", input_type=int)
            idUser = get_validated_input("Introduza o idUser: ", input_type=int)
            transaction_type = get_validated_input("Introduzir transactionType (buy/sell): ", validation_fn=lambda x: x.lower() in {"buy", "sell"}).lower()
            units = get_validated_input("Introduzir units: ", input_type=int)
            btc_timestamp = get_validated_input("Introduzir timestamp (YYYY-MM-DDTHH:MM:SS.sss): ", validation_fn=lambda x: len(x.split("T")) == 2 and "." in x)

            put_transaction_payload = {
                "idTransaction": idTransaction,
                "idUser": idUser,
                "transactionType": transaction_type,
                "units": units,
                "btcTimeStamp": btc_timestamp,
            }

            put_transaction(transaction_api_url, idTransaction, put_transaction_payload)
        
        # 9. Apagar uma transação (por idTransaction).
        elif choice == 9:
            print("Inputs:")
            print(" - idTransaction: (ex: 1)")
            idTransaction = get_validated_input("Introduza o idTransaction da transação: ", input_type=int)
            delete_transaction(transaction_api_url, idTransaction)

        # 0. Sair"
        elif choice == 0:
            print("Script terminada.")
            break

if __name__ == "__main__":
    main()
