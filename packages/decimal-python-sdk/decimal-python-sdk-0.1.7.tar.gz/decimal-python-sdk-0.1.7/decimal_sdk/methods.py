import json

from .wallet import Wallet
from .api import DecimalAPI
from .transactions import SendCoinTransaction


def SendAllCoin(api: DecimalAPI, wallet: Wallet, receiver: str, coin_name: str, options = {}):
    ''' Send all coins from wallet '''

    try:
        wallet_data = json.loads(api.get_address(wallet.get_address()))
        balance = '0'
        denom = 'del'

        if (options.get('denom') is not None):
            denom = options['denom']

        if wallet_data["ok"]:
            balance = wallet_data["result"]["address"]["balance"][coin_name]

        balance = int(balance) * pow(10, -18)

        if denom is coin_name:
            tx = SendCoinTransaction(wallet.get_address(), receiver, coin_name, balance) #transaction for calculation commission
            balance = balance - api.estimate_tx_fee(tx, wallet, options)

        tx1 = SendCoinTransaction(wallet.get_address(), receiver, coin_name, balance - 0.00001)

        return api.send_tx(tx1, wallet, options)

    except Exception as e:
        return str(e)