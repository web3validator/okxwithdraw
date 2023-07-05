import os
import random
import time

# noinspection PyPackageRequirements
from okx.Funding import FundingAPI
from dotenv import load_dotenv

import config


def main():
    funding_api = FundingAPI(API_KEY, SECRET_KEY, PASSPHRASE, flag='0', debug=False)

    with open('wallets.txt', 'r') as f:
        wallets = [wallet.strip() for wallet in f.readlines() if wallet.strip() != '']
        random.shuffle(wallets)

    print('Requesting withdrawals...')

    errors = 0
    for wallet in wallets:
        amount = round(random.uniform(*config.AMOUNT), config.PRECISION)

        response = funding_api.withdrawal(
            ccy=str(config.CURRENCY),
            amt=str(amount),
            dest='4',
            toAddr=wallet,
            fee=str(config.FEE),
            chain=f'{config.CURRENCY}-{config.CHAIN}'
        )

        print(f'\n'.join([
            '',
            f'>>>\tAddress: {wallet}',
            f'\tAmount: {amount}',
            f'\tStatus: {"SUCCESS" if response["code"] == "0" else "ERROR"}'
        ]))

        if response['code'] != '0':
            errors += 1
            print(f'\tCode: {response["code"]}')
            print(f'\tMessage: {response["msg"]}')
        else:
            print(f'\tID: {response["data"][0]["wdId"]}')

        if wallet != wallets[-1]:
            time.sleep(random.uniform(*config.DELAY))

    print('\nDone')
    if errors != 0:
        print(f'Errors: {errors}')


if __name__ == '__main__':
    load_dotenv()

    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    PASSPHRASE = os.getenv('PASSPHRASE')

    main()
