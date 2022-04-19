import constants as c
import functions as f


def _main():
    etherscan = f.EtherscanApi(c.API_KEY)
    storage = f.Storage(c.STORAGE_PATH)
    eth = f.Ethereum()
    menu = f.Menu()

    while True:

        option = menu.get_option(1)  # Show main menu
        if option == 1:
            '''Show wallet transactions history'''

            # 0xA3390BF36e2BDeBf6d61d49E0DE910609C8F13E6
            wallet = input('Wallet adress --> ')
            wallet_data = etherscan.get_wallet_info(wallet)

            # Convert data to ready print result
            transactions = etherscan.sort_data(wallet_data)

            # Show how many transactions were found
            transactions_num = len(transactions)
            print(f'\nNumber of transactions: {transactions_num}\n')

            for row in transactions:
                for key, item in row.items():
                    print(f'{key}  -  {item}')
                print('\n')
        

        elif option == 2:
            '''Wallets Storage

            - Show wallets that tracked
            - Add new wallet
            - Remove wallet
            - Rename label
            '''
            storage.show_saved_wallets()

            storage_option = menu.get_option(2)  # Show storage menu
            if storage_option == 1:
                '''Add new wallet in storage'''

                wallet_adrress = input('Wallet adress --> ')
                wallet_label = input('Wallet label (not nocessary) --> ')
            
                # Checking the new wallet for validity
                if eth.check_wallet(wallet_adrress) is not None:
                    storage.add_wallet(wallet_adrress, wallet_label)        
                
            elif storage_option == 2:
                '''Remove Wallet'''

                deleted_wallet = input('Wallet adress --> ')
                storage.remove_wallet(deleted_wallet)

                print('Wallet was removed!')   
        
        elif option == 0:
            print('Thank you for using this program!')
            exit()

        else:
            print('Invalid option')
            option = menu.get_option(1)


if __name__ == '__main__':
    _main()
