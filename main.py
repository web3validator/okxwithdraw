import os
import random
import time

# noinspection PyPackageRequirements
from okx.Funding import FundingAPI
from dotenv import load_dotenv

import config


def rand_decimal(mn, mx):
    return random.randint(mn * 100, mx * 100) / 100


def main():
    funding_api = FundingAPI(API_KEY, SECRET_KEY, PASSPHRASE, flag='0', debug=False)

    with open('wallets.txt', 'r') as f:
        wallets = [wallet.strip() for wallet in f.readlines() if wallet.strip() != '']
        random.shuffle(wallets)

    print('Requesting withdrawals...')

    errors = 0
    for wallet in wallets:
        print()

        amount = rand_decimal(config.AMOUNT_MIN, config.AMOUNT_MAX)

        response = funding_api.withdrawal(
            ccy=str(config.CURRENCY),
            amt=str(amount),
            dest='4',
            toAddr=wallet,
            fee=config.FEE,
            chain=f'{config.CURRENCY}-{config.CHAIN}'
        )

        print(f'\n'.join([
            f'>>>\tAddress: {wallet}',
            f'\tAmount: {amount:.2f}',
            f'\tStatus: {"SUCCESS" if response["code"] == "0" else "ERROR"}'
        ]))

        if response['code'] != '0':
            errors += 1
            print(f'\tCode: {response["code"]}')
            print(f'\tMessage: {response["msg"]}')
        else:
            print(f'\tID: {response["data"][0]["wdId"]}')

        time.sleep(rand_decimal(config.DELAY_MIN, config.DELAY_MAX))

    print('\nDone')
    if errors != 0:
        print(f'Errors: {errors}')


if __name__ == '__main__':
    load_dotenv()

    API_KEY = os.getenv('API_KEY')
    SECRET_KEY = os.getenv('SECRET_KEY')
    PASSPHRASE = os.getenv('PASSPHRASE')

    main()
