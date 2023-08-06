import bech32


def verify_address(address, prefix="dx"):
    if not address:
        raise Exception("address is missing")

    try:
        decoded = bech32.bech32_decode(address)

        print(f"checked {address}, result is:")
        print(decoded[0] == prefix and decoded[1] != [])
        return decoded[0] == prefix and decoded[1] != []

    except:
        return False


def validate_data(data):
    if "from" in data:
        if data["from"] == "":
            raise Exception("Field \'from\' can not be empty")

        if not verify_address(data["from"]):
            raise Exception("Incorrect sender address format")

    if "sender" in data:
        if data["sender"] == "":
            raise Exception("Field \'sender\' can not be empty")

        if not verify_address(data["sender"]):
            raise Exception("Incorrect sender address format")

    if "to" in data:
        if data["to"] == "":
            raise Exception("Field \'to\' can not be empty")

        if not verify_address(data["to"]):
            raise Exception("Incorrect recipient address format")

    if "receiver" in data:
        if data["receiver"] == "":
            raise Exception("Field \'receiver\' can not be empty")

        if not verify_address(data["receiver"]):
            raise Exception("Incorrect receiver address format")

    if "validator_address" in data:
        if data["validator_address"] == "":
            raise Exception("Field \'validator_address\' can not be empty")

        if not verify_address(data["validator_address"], "dxvaloper"):
            raise Exception("Incorrect validator address format")

    if "delegator_address" in data:
        if data["delegator_address"] == "":
            raise Exception("Field \'delegator_address\' can not be empty")

        if not verify_address(data["delegator_address"]):
            raise Exception("Incorrect delegator address format")

    if "owners" in data:
        if not data["owners"]:
            raise Exception("Field \'owners\' can not be empty")

        for owner in data["owners"]:
            # if owner == "":
            #     raise Exception("Owner in field \'owners\' can not be empty")

            if not verify_address(owner):
                raise Exception(f"Incorrect owner address format: {owner}")

    if "sends" in data:
        if not data["sends"]:
            raise Exception("Field \'sends\' can not be empty")

        for send in data["sends"]:
            # if send == "":
            #     raise Exception("Recipient in field \'sends\' can not be empty")

            if not verify_address(send["receiver"]):
                raise Exception(f"Incorrect recipient address format: {send}")


