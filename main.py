import functions as f
"""
* Add pretty output (option 1)
* Add exit button
* Add func that can rewrite wallet label
* Add func that delete wallet from storage
* Add func that can show all transactions from saved wallets 
"""

def first_option(serverApi, wallet):
    data = serverApi.get_wallet_info(wallet)

    if int(data['status']) != 0:  # 0 - Something gone wrong, 1 - ok
        
        for item in data['result']:
            info = {
                'Block Number': item['blockNumber'],
                'Time Stamp': item['timeStamp'],
                'Amount': item['value'],
                'Gas': item['gas'],
                'Gas Used': item['gasUsed'],
                'Gas Price': item['gasPrice'],
                'From': item['from'],
                'To': item['to'],
                'Hash': item['hash'],
                'Block Hash': item['blockHash']
            }

            for key, item in info.items():
                print(f"{key}  -  {item}")
            
            print('\n')

        # How many transactions were found
        amount = len(data['result'])
        print(f'Number of transactions: {amount}')

    else:
        print(data['message'])  # Error message


def second_option(serverApi, storage, new_wallet, label=None):
    # Checking the new wallet for validity
    wallet_info = serverApi.get_wallet_info(new_wallet)

    if int(wallet_info['status']) != 0:
        result = storage.add_wallet(new_wallet, label)
        
        if result:
            print('Wallet was successfully added!')

    else:
        print('Invalid wallet!')


def third_option(storage):
    storage_data = storage.read()  # Get data from storage

    if storage_data:
        for wallet in storage_data:
            print(wallet)

    else:
        print('Storage is empty!')


def _main():
    storage = f.Storage()
    serverApi = f.EtherscanApi()
    while True:
        option = f.Style.get_option()  # Get option

        if option == 1:
            '''Get wallet history of transactions'''

            # 0xA3390BF36e2BDeBf6d61d49E0DE910609C8F13E6
            wallet = input('Wallet adress --> ')
            first_option(serverApi, wallet)

        elif option == 2:
            '''Add new wallet for tracking'''

            new_wallet = input('Wallet adress --> ')
            label = input('Wallet label (not nocessary) --> ')
            second_option(serverApi, storage, new_wallet, label)

        elif option == 3:

            '''Return wallets that tracked'''
            third_option(storage)

        else:
            print('Invalid option')
            option = f.Style.get_option()


if __name__ == '__main__':
    _main()
