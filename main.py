import os
import random
import time

from okx.Funding import FundingAPI
from dotenv import load_dotenv

import config


def main():
    funding_api = FundingAPI(API_KEY, SECRET_KEY, PASSPHRASE, flag='0', debug=False)

    with open('wallets.txt', 'r') as f:
        wallets = [wallet.strip() for wallet in f.readlines()]
        random.shuffle(wallets)

    print('Requesting withdrawals...')

    errors = 0
    for wallet in wallets:
        print()

        amount = random.randint(config.AMOUNT_MIN * 100, config.AMOUNT_MAX * 100) / 100

        response = funding_api.withdrawal(
            ccy=str(config.CURRENCY),
            amt=str(amount),
            dest='4',
            toAddr=wallet,
            fee=config.FEE,
            chain=f'{config.CURRENCY}-{config.CHAIN}'
        )

        status = 'SUCCESS' if response['code'] == '0' else 'ERROR'

        print(f'\n'.join([
            f'>>>\tAddress: {wallet}',
            f'\tAmount: {amount:.2f}',
            f'\tStatus: {status}'
        ]))

        if response['code'] != '0':
            errors += 1
            print(f'\tCode: {response["code"]}')
            print(f'\tMessage: {response["msg"]}')
        else:
            print(f'\tID: {response["data"][0]["wdId"]}')

        time.sleep(1 / config.RATE_LIMIT)

    print('\nDone')
    errors = 'None' if errors == 0 else errors
    print(f'Errors: {errors}')


if __name__ == '__main__':
    load_dotenv()

    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    PASSPHRASE = os.getenv('PASSPHRASE')

    main()
