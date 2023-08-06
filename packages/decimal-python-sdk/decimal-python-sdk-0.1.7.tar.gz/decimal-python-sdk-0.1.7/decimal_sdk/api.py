import base64
import datetime
import json
from hashlib import sha256

import base58
import bech32
import ethereum.transactions as crypto
import requests
import rlp
import sha3
from Cryptodome.Hash import SHA256
from ecdsa import SigningKey, SECP256k1
from ecdsa.util import sigencode_string_canonize

from decimal_sdk.transactions import RedeemCheckTransaction
from decimal_sdk.types import Coin
from .transactions import Transaction
from .types import FEES
from .utils.fields_validator import validate_data
from .utils.helpers import get_amount_uni, from_words
from .wallet import Wallet
from datetime import datetime, timedelta


class DecimalAPI:
    """
    Base class to perform operations on Decimal API.
    Create new instance of api with passing base URL to DecimalAPI class.
    """
    unit = 0.001

    def __init__(self, base_url: str):
        self.base_url = base_url
        if self.base_url[-1]:
            self.base_url += '/'

    def get_address(self, address: str):
        self.__validate_address(address)
        return self.__request(f'address/{address}')

    def get_coin(self, name: str):
        return self.__request(f'coin/{name}')

    def get_coins_list(self, limit: int = 10, offset: int = 0):
        options = {"limit": limit, "offset": offset}
        return self.__request('coin', 'get', None, options)

    def get_multisig(self, address: str):
        self.__validate_address(address)
        return self.__request(f'multisig/{address}')

    def get_multisigs(self, address: str, limit: int = 10, offset: int = 0):
        self.__validate_address(address)
        options = {"limit": limit, "offset": offset}
        return self.__request(f'address/{address}/multisigs', 'get', None, options)

    def get_my_transactions(self, wallet: Wallet, limit: int = 10, offset: int = 0):
        options = {"limit": limit, "offset": offset}
        return self.__request(f'address/{wallet.get_address()}/txs', 'get', None, options)

    def get_nonce(self, address: str):
        self.__validate_address(address)
        return self.__request(f'rpc/auth/accounts/{address}')

    def get_nonce_not_increasing(self, address: str):
        self.__validate_address(address)
        return self.__request(f'rpc/accounts/{address}')

    def get_stakes(self, address: str):
        self.__validate_address(address)
        return self.__request(f'address/{address}/stakes')

    def get_tx(self, tx_hash: str):
        return json.loads(self.__request("rpc/tx", "get", options={"hash": f"{tx_hash}"}))["result"]

    def get_txs_multisign(self, address: str, limit: int = 10, offset: int = 0):
        options = {"limit": limit, "offset": offset}
        self.__validate_address(address)
        return self.__request(f"multisig/{address}/txs", 'get', None, options)

    def get_validator(self, address: str):
        self.__validate_address(address)
        return self.__request(f'validator/{address}')

    def get_nft(self, id: str, wallet: Wallet):
        timestamp = int(str(datetime.datetime.now().timestamp()).split(".")[0])
        data = {
            "nftId": id,
            "timestamp": timestamp
        }

        encoded = json.dumps(data).replace(" ", "").encode()
        msg_hash = sha3.keccak_256(encoded)
        v, r, s = crypto.ecsign(msg_hash.digest(), wallet.get_private_key())

        rr = int_to_big_endian(r).hex()
        ss = int_to_big_endian(s).hex()
        vv = v-27

        options={
            "timestamp": timestamp,
            "signature": json.dumps({
                "r":rr,
                "s":ss,
                "recoveryParam":vv})
        }
        return self.__request(f'nfts/{id}', 'get', None, options)

    def get_nft_stakes(self, address: str):
        self.__validate_address(address)
        return self.__request(f'address/{address}/nfts/stakes')

    def get_tx_by_hash(self, hash: str):
        return self.__request(f'tx/{hash}')

    def estimate_tx_fee(self, tx: Transaction, wallet: Wallet, options={}, ):
        """Method to sign and send prepared transaction"""
        url = "rpc/txs-directly"

        denom = "del"
        commission_type = "base"
        if "denom" in options:
            denom = options["denom"]
            commission_type = "value"

        if "memo" in options:
            tx.memo = options["memo"]
            tx.signer.memo = options["memo"]

        message = tx.memo
        tx_data = tx.message.get_message()
        return self.__get_comission(tx, denom, FEES[tx.message.type], tx_data)["value"]

    def send_tx(self, tx: Transaction, wallet: Wallet, options={}):
        """Method to sign and send prepared transaction"""
        url = "rpc/txs-directly"

        denom = "del"
        commission_type = "base"

        if "denom" in options:
            denom = options["denom"]
            commission_type = "value"

        if "memo" in options:
            options["memo"] = options["memo"]
            tx.memo = options["memo"]
            tx.signer.memo = options["memo"]

        message = tx.memo
        tx_data = tx.message.get_message()
        validate_data(tx_data["value"])
        commission = self.__get_comission(tx, denom, FEES[tx.message.type], tx_data)
        fee_amount = Coin(denom.lower(), get_amount_uni(commission[commission_type]))

        if wallet.nonce:
            sequence = wallet.nonce["value"]["sequence"]
            wallet.nonce = json.loads(self.get_nonce_not_increasing(wallet.get_address()))["result"]

            if datetime.now() - timedelta(seconds=7) > wallet.nonce_time:
                wallet.nonce_time = datetime.now()
            else:
                wallet.nonce["value"]["sequence"] = str(int(sequence) + 1)
        else:
            wallet.nonce = json.loads(self.get_nonce_not_increasing(wallet.get_address()))["result"]
            wallet.nonce_time = datetime.now()

        if "sequence" in options:
            tx.signer.sequence = str(options["sequence"])
            wallet.nonce["value"]["sequence"] = options["sequence"]

        tx.signer.chain_id = self.get_chain_id()
        tx.signer.account_number = str(wallet.nonce["value"]["account_number"])
        tx.signer.sequence = str(wallet.nonce["value"]["sequence"])

        if denom == "del" or denom == "tdel":
            tx.fee.amount = []
            tx.signer.fee.amount = []
        else:
            tx.fee.amount = [fee_amount]
            tx.signer.fee.amount = [fee_amount]

        tx.signer.fee = tx.fee
        tx.signer.msgs = [tx.msgs[-1]]
        tx.signer.memo = tx.memo

        payload = {"tx": {}, "mode": "sync"}
        payload["tx"]["msg"] = [tx_data]

        if denom == "del" or denom == "tdel":
            payload["tx"]["fee"] = {"amount": [], "gas": "0"}
        else:
            payload["tx"]["fee"] = {"amount": [tx.signer.fee.amount[0].__dict__()], "gas": "0"}

        payload["tx"]["memo"] = message
        payload["tx"]["signatures"] = []

        tx.sign(wallet)
        tx.msgs.clear()
        tx.signer.msgs.clear()

        for sig in tx.signatures:
            payload["tx"]["signatures"].append(sig.get_signature())

        return self.__request(url, 'post', json.dumps(payload))

    def issue_check(self, wallet, data):
        new_data = {
            "coin": data["coin"].lower(),
            "amount": int(get_amount_uni(int(data["amount"]), False)),
            "nonce": data["nonce"],
            "due_block": int(data["due_block"]),
            "passphrase": data["password"],
        }

        chain_id = self.get_chain_id()

        passphrase_hash = SHA256.new(str.encode(new_data["passphrase"])).digest()
        pp = []
        for b in passphrase_hash:
            pp.append(b)

        check_hash = self.__rpl_hash([
            chain_id,
            new_data["coin"],
            new_data["amount"],
            new_data["nonce"],
            new_data["due_block"],
        ])

        ch = []
        for b in check_hash:
            ch.append(b)

        passphrase_hash = sha256(str.encode(new_data["passphrase"])).digest()

        sk = SigningKey.from_string(passphrase_hash, curve=SECP256k1)
        lock_obj = sk.sign_digest_deterministic(check_hash, hashfunc=sha256, sigencode=sigencode_string_canonize)

        bts2 = []
        for b in lock_obj:
            bts2.append(b)
        lock_signature = bytearray(65)

        i = 0
        while i < 64:
            lock_signature[i] = lock_obj[i]
            i += 1

        v, r, s = crypto.ecsign(check_hash, passphrase_hash)
        lock_signature[64] = v - 27

        check_locked_hash = self.__rpl_hash([
            chain_id,
            new_data["coin"],
            new_data["amount"],
            new_data["nonce"],
            new_data["due_block"],
            lock_signature
        ])
        clh = []
        for b in check_locked_hash:
            clh.append(b)
        pk = []
        for b in wallet.get_private_key():
            pk.append(b)
        sk = SigningKey.from_string(wallet.get_private_key(), curve=SECP256k1)
        check_obj = sk.sign_digest_deterministic(check_locked_hash, hashfunc=sha256,
                                                 sigencode=sigencode_string_canonize)
        co = []
        for b in check_obj:
            co.append(b)
        v, r, s = crypto.ecsign(check_locked_hash, wallet.get_private_key())

        rr = bytearray(32)
        ss = bytearray(32)

        i = 0
        while i < 32:
            rr[i] = crypto.int_to_32bytearray(r)[i]
            i += 1

        i = 0
        while i < 32:
            ss[i] = crypto.int_to_32bytearray(s)[i]
            i += 1

        check = rlp.encode([
            chain_id,
            new_data["coin"],
            new_data["amount"],
            new_data["nonce"],
            new_data["due_block"],
            lock_signature,
            v,
            rr,
            ss,
        ])
        chk = []
        for b in check:
            chk.append(b)
        return base58.b58encode(check).decode('utf-8')

    def redeem_check(self, data, wallet):
        passphrase_hash = SHA256.new(str.encode(data["password"])).digest()

        words = bech32.bech32_decode(wallet.get_address())
        f_words = from_words(words[1])

        f_w_buffer = bytearray()
        for b in f_words:
            f_w_buffer.append(b)

        sender_address_hash = self.__rpl_hash([f_w_buffer])
        sah = []
        for b in sender_address_hash:
            sah.append(b)

        sk = SigningKey.from_string(passphrase_hash, curve=SECP256k1)
        proof_obj = sk.sign_digest_deterministic(sender_address_hash, hashfunc=sha256,
                                                 sigencode=sigencode_string_canonize)

        po = []
        for b in proof_obj:
            po.append(b)

        proof_signature = bytearray(65)

        i = 0
        while i < 64:
            proof_signature[i] = proof_obj[i]
            i += 1

        v, r, s = crypto.ecsign(sender_address_hash, passphrase_hash)
        proof_signature[64] = v - 27

        proof = proof_signature
        proof = base64.b64encode(proof)

        transaction = RedeemCheckTransaction(wallet.get_address(), data["check"], proof.decode('utf-8'))

        return self.send_tx(transaction, wallet)

    def get_chain_id(self):
        url = "rpc/node_info"
        resp = json.loads(self.__request(url))
        chain_id = resp["node_info"]["network"]
        return chain_id

    @staticmethod
    def __validate_address(address: str):
        if len(address) < 41 or not address.startswith('dx'):
            raise Exception('Invalid address')

    @staticmethod
    def __rpl_hash(data):
        khash = sha3.keccak_256()
        khash.update(rlp.encode(data))
        return khash.digest()

    def get_coin_price(self, name: str):
        coin = json.loads(self.get_coin(name))
        if not coin["ok"]:
            raise Exception('Coin not found')
        coin = coin["result"]
        reserve = int(coin["reserve"]) * pow(10, -18)
        supply = int(coin["volume"]) * pow(10, -18)
        crr = coin["crr"] / 100

        amount = min(supply, 1)

        if supply == 0:
            return 0

        result = amount / supply
        result = 1 - result
        result = pow(result, 1 / crr)
        result = (1 - result) * reserve

        return result

    def __get_tx_size(self, tx: Transaction, denom: str):
        value = {"msg": [tx.message.get_message()]}
        value["memo"] = tx.memo
        value["fee"] = {"amount": [{"amount": "0", "denom": denom}], "gas": "0"}
        preparedTx = {
            "type": 'cosmos-sdk/StdTx',
            "value": value
        }

        signatureSize = 109
        resp = json.loads(self.__request('rpc/txs/encode', 'post', json.dumps(preparedTx)))

        encoded_tx_base64 = resp["tx"]
        encoded_tx = len(base64.b64decode(encoded_tx_base64))
        size = encoded_tx + signatureSize
        return size

    def __get_comission(self, tx: Transaction, fee_coin, operation_fee, tx_data):
        if tx.message.get_type() == 'coin/create_coin':
            ticker_length = len(tx_data['value']['symbol'])
            if ticker_length == 3:
                operation_fee = 1000000
            elif ticker_length == 4:
                operation_fee = 100000
            elif ticker_length == 5:
                operation_fee = 10000
            elif ticker_length == 6:
                operation_fee = 1000
            else:
                operation_fee = 100

        ticker = fee_coin

        text_size = self.__get_tx_size(tx, fee_coin)
        fee_for_text = text_size * 2
        fee_in_base = (operation_fee + fee_for_text + 20) / 1000

        if tx.message.get_type() == 'coin/multi_send_coin':
            number_of_participants = len(tx.message.get_message()["value"]["sends"])
            fee_for_participants = 5 * (number_of_participants - 1) / 1000
            fee_in_base = fee_in_base + fee_for_participants

        if fee_coin in ['del', 'tdel']:
            return {"coinPrice": "1", "value": fee_in_base, "base": fee_in_base}

        try:
            coin_price = self.get_coin_price(ticker)
            fee_in_custom = fee_in_base / coin_price * 1.03

        except:
            fee_in_custom = 0
            coin_price = 0

        return {"coinPrice": str(coin_price), 'value': fee_in_custom, 'base': fee_in_base}

    def __request(self, path: str, method: str = 'get', payload=None, options={}):
        url = (self.base_url + path)
        if method == 'get':
            if len(options) > 0:
                response = requests.get(url, params=options)
            else:
                response = requests.get(url)
        else:
            response = requests.post(url, payload)
        return response.text

def int_to_big_endian(value: int) -> bytes:
    return value.to_bytes((value.bit_length() + 7) // 8 or 1, "big")
