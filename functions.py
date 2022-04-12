import constants as c
import requests
import json
import os


class EtherscanApi:
    @staticmethod
    def get_wallet_info(wallet):
        url = f'https://api.etherscan.io/api?module=account&action=txlist' \
              f'&address={wallet}&startblock=0&endblock=99999999&page=1' \
              f'&offset=10&sort=asc&apikey={c.API_KEY}'

        data = requests.get(url).json()

        return data


class Storage:
    def __init__(self):
        self.filename = c.MAIN_STORAGE

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
    
    def add_wallet(self, new_wallet, label):
        storage_data = self.read()  # Get existing wallets
        wallet_info = {'Wallet': new_wallet, 'Label': label}

        if storage_data:
            # Checking if the wallet is already registered
            for row in storage_data:
                if row['Wallet'] == new_wallet:
                    print('Wallet already exist!')

                    return None
            
            # Adding new wallet
            result = storage_data
            result.append(wallet_info)

        else:
            # if storage is empty
            result = [wallet_info]
        
        self.write(result)


class Style:
    @staticmethod
    def get_option():
        # Main menu
        text = '''
[1] Get Wallet Info 
[2] Add New Wallet
[3] My Saved Wallets
'''
        print(text)

        option = int(input('Your option --> '))

        return option
