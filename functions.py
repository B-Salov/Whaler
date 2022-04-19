'''File with all classes

* EtherscanApi - api which provide blockchain information.

* Storage - read, write, add new wallet, remove wallet,
show saved wallets.

* Ethereum - Basics web3 functions, like convert from wei to eth
and check if wallet adress is exist.
'''
import requests
import json
import os


class EtherscanApi:
    '''Etherscan free API.

    * Max - 5 request per second.
    * Api key in 'constants.py'.
    '''

    def __init__(self, API_KEY):
        self.api_key = API_KEY
    
    def get_wallet_info(self, wallet):
        '''Return wallet transactions history'''

        url = f'https://api.etherscan.io/api?module=account&action=txlist' \
              f'&address={wallet}&startblock=0&endblock=99999999&page=1' \
              f'&offset=10&sort=asc&apikey={self.api_key}'

        data = requests.get(url).json()

        return data
    
    def sort_data(self, data):
        '''Return sorted data, which ready to print.

        * Count transaction fee.
        '''
        # 0 - Meane that transaction is pending or cancled
        if int(data['status']) != 0:

            result = []
            for item in data['result']:
                transaction_fee = int(item['gasUsed']) * int(item['gasPrice'])

                info = {
                    'Block Number': item['blockNumber'],
                    'Time Stamp': item['timeStamp'],
                    'Amount': Ethereum.from_wei(item['value']),
                    'Gas': item['gas'],
                    'Transaction Fee': Ethereum.from_wei(transaction_fee),
                    'From': item['from'],
                    'To': item['to'],
                    'Hash': item['hash'],
                    'Block Hash': item['blockHash']
                }

                result.append(info)

            return result

        else:
            print(data['message'])  # Error message

            return None


class Ethereum:

    @staticmethod
    def from_wei(number):
        # Return converted wei to eth
        # 1 eth - 10**18 wei
        return f'{int(number) / 10**18} eth'
    
    @staticmethod
    def check_wallet(wallet_address):
        '''Checking if the wallet exist'''
        wallet_info = EtherscanApi.get_wallet_info(wallet_address)

        if int(wallet_info['status']) != 0:
            return True

        return None


class Storage:
    def __init__(self, storage_path):
        self.filename = storage_path

        # Creating storage, if it doesn't exist
        if not os.path.exists(self.filename):
            with open(self.filename, 'w'):
                pass
    
    def read(self):
        if os.path.getsize(self.filename):
            with open(self.filename, 'r') as f:
                data = json.load(f)
            
            return data
        
        return None

    def write(self, data):
        with open(self.filename, 'w') as f:
            json.dump(data, f)

    def show_saved_wallets(self):
        storage_info = self.read()  # Get data from storage

        if storage_info is not None:
            for row in storage_info:
                print(f'Wallet: {row["Wallet"]}\nLabel:  {row["Label"]}')

        else:
            print('Storage is empty!')
    
    def add_wallet(self, new_wallet, label):
        '''Add new wallet to storage'''
        storage_data = self.read()  # Get existing wallets
        # Storage structure
        wallet_info = {'Wallet': new_wallet, 'Label': label}

        if storage_data is not None:
            # Check if the wallet is already exist
            for row in storage_data:
                if row['Wallet'] == new_wallet:
                    print('Wallet already exist!')

                    return None
            
            # If not then adding new one to other wallets
            result = storage_data
            result.append(wallet_info)

        else:
            # if storage is empty
            result = [wallet_info]
        
        self.write(result)

        print('Wallet was seccessfuly added!')
    
    def remove_wallet(self, wallet):
        storage_data = self.read()

        if storage_data is not None:
            res = []
            for item in storage_data:
                if item['Wallet'] == wallet:
                    continue

                res.append(item)
                    
            self.write(res)

        else:
            return None


class Menu:
    def __init__(self):
        self.main = '''
[1] Get Wallet Info 
[2] My Saved Wallets
[0] Exit
'''
        self.storage = '''
[1] Add New Wallet 
[2] Remove Wallet
[3] Rewrite Label
[0] Back
'''

    def get_option(self, option):
        '''Return choosed option
        
        * Option 1 - Main menu
        * Option 2 - Storage menu
        '''

        if option == 1:
            menu = self.main
        elif option == 2:
            menu = self.storage
        else:
            return None
        
        print(menu)
        user_option = int(input('Your option --> '))

        return user_option
