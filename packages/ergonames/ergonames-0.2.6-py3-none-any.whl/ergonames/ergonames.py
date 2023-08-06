import requests
import math
import datetime

EXPLORER_API_URL = "https://api-testnet.ergoplatform.com/"
 
MINT_ADDRESS = "3WwKzFjZGrtKAV7qSCoJsZK9iJhLLrUa3uwd4yw52bVtDVv6j5TL"

class Token:

    def __init__(self, id, boxId, name):
        self.id = id
        self.boxId = boxId
        self.name = name

def _get_address_data(address, explorerUrl = EXPLORER_API_URL):
    url = explorerUrl + "api/v1/addresses/" + str(address) + "/balance/confirmed"
    data = requests.get(url).json()
    return data

def _create_address_data(address):
    tokens = _get_address_data(address)["tokens"]
    return tokens

def _create_address_tokens_array(tokenData):
    tokenArray = []
    for i in tokenData:
        tk = Token(i['tokenId'], "none", i['name'])
        tokenArray.append(tk)
    return tokenArray

def _remove_wrong_names_tokens(tokenArray):
    newArr = []
    for i in tokenArray:
        if i.name[0] == "~" and " " not in i.name:
            newArr.append(i)
    return newArr

def _check_correct_ownership(tokenArray, address):
    ownedErgoNames = []
    for i in tokenArray:
        ownerAddress = resolve_ergoname(i.name)
        if ownerAddress == address:
            ownedErgoNames.append(i)
    return ownedErgoNames

def _get_token_data(tokenName, limit, offset, explorerUrl = EXPLORER_API_URL):
    url = explorerUrl + "api/v1/tokens/search?query=" + str(tokenName) + "&limit=" + str(limit) + "&offset=" + str(offset)
    data = requests.get(url).json()
    return data

def _create_token_data(tokenName):
    total = _get_token_data(tokenName, 1, 0)['total']
    neededCalls = math.floor(total / 500) + 1
    tokenData = []
    offset = 0
    if total > 0:
        for i in range(neededCalls):
            data = _get_token_data(tokenName, 500, offset)['items']
            tokenData += data
        return tokenData
    else:
        return None

def _convert_token_data_to_token(data):
    tokenArray = []
    for i in data:
        tk = Token(i['id'], i['boxId'], i['name'])
        tokenArray.append(tk)
    return tokenArray

def _get_box_address(boxId, explorerUrl = EXPLORER_API_URL):
    url = explorerUrl + "api/v1/boxes/" + (str(boxId))
    data = requests.get(url).json()
    return data['address']

def _check_box_address(address):
    if address == MINT_ADDRESS:
        return True
    return False

def _get_asset_minted_at_address(tokenArray):
    for i in tokenArray:
        address = _get_box_address(i.boxId)
        if (_check_box_address(address)):
            return i.id
    return None

def _get_token_transaction_data(tokenId, explorerUrl = EXPLORER_API_URL):
    total = _get_max_transactions_for_token(tokenId)
    url = explorerUrl + "api/v1/assets/search/byTokenId?query=" + str(tokenId) + "&limit=1&offset=" + str(total-1)
    data = requests.get(url).json()['items']
    return data

def _get_max_transactions_for_token(tokenId, explorerUrl = EXPLORER_API_URL):
    url = explorerUrl + "api/v1/assets/search/byTokenId?query=" + str(tokenId) + "&limit=1"
    total = requests.get(url).json()['total']
    return total

def _get_box_by_id(boxId, explorerUrl = EXPLORER_API_URL):
    url = explorerUrl + "api/v1/boxes/" + str(boxId)
    data = requests.get(url).json()
    return data

def _get_last_transaction(data):
    length = len(data)
    return data[length-1]

def _get_first_transaction(data):
    return data[0]

def _get_box_id_from_transaction_data(data):
    return data['boxId']

def _get_settlement_height_from_box_data(data):
    return data['settlementHeight']

def _get_block_id_from_box_data(data):
    return data['blockId']

def _get_block_by_block_height(height, explorerUrl = EXPLORER_API_URL):
    url = explorerUrl + "api/v1/blocks/" + str(height)
    data = requests.get(url).json()
    return data

def _get_timestamp_from_block_data(data):
    return data["block"]["header"]["timestamp"]

def convert_timestamp_to_date(timestamp):
    date = datetime.datetime.fromtimestamp(timestamp/1000.0)
    return date

def resolve_ergoname(name):
    name = reformat_name(name)
    tokenData = _create_token_data(name)
    if tokenData != None:
        tokenArray = _convert_token_data_to_token(tokenData)
        tokenId = _get_asset_minted_at_address(tokenArray)
        tokenTransactions = _get_token_transaction_data(tokenId)
        tokenLastTransaction = _get_last_transaction(tokenTransactions)
        tokenCurrentBoxId = _get_box_id_from_transaction_data(tokenLastTransaction)
        address = _get_box_address(tokenCurrentBoxId)
        return address
    return None

def check_already_registered(name):
    name = reformat_name(name)
    address = resolve_ergoname(name)
    if address != None:
        return True
    return False

def reverse_search(address):
    tokenData = _create_address_data(address)
    tokenArray = _create_address_tokens_array(tokenData)
    tokenArray = _remove_wrong_names_tokens(tokenArray)
    owned = _check_correct_ownership(tokenArray, address)
    return owned

def get_total_amount_owned(address):
    owned = reverse_search(address)
    return len(owned)

def check_name_price(name):
    name = reformat_name(name)
    return None

def get_block_id_registered(name):
    name = reformat_name(name)
    tokenData = _create_token_data(name)
    if tokenData != None:
        tokenArray = _convert_token_data_to_token(tokenData)
        tokenId = _get_asset_minted_at_address(tokenArray)
        tokenTransactions = _get_token_transaction_data(tokenId)
        tokenFirstTransactions = _get_first_transaction(tokenTransactions)
        tokenMintBoxId = _get_box_id_from_transaction_data(tokenFirstTransactions)
        tokenMintBox = _get_box_by_id(tokenMintBoxId)
        blockId = _get_block_id_from_box_data(tokenMintBox)
        return blockId
    return None

def get_block_registered(name):
    name = reformat_name(name)
    tokenData = _create_token_data(name)
    if tokenData != None:
        tokenArray = _convert_token_data_to_token(tokenData)
        tokenId = _get_asset_minted_at_address(tokenArray)
        tokenTransactions = _get_token_transaction_data(tokenId)
        tokenFirstTransactions = _get_first_transaction(tokenTransactions)
        tokenMintBoxId = _get_box_id_from_transaction_data(tokenFirstTransactions)
        tokenMintBox = _get_box_by_id(tokenMintBoxId)
        height = _get_settlement_height_from_box_data(tokenMintBox)
        return height
    return None

def get_timestamp_registered(name):
    name = reformat_name(name)
    blockRegistered = get_block_id_registered(name)
    if blockRegistered != None:
        blockData = _get_block_by_block_height(blockRegistered)
        timestamp = _get_timestamp_from_block_data(blockData)
        return timestamp
    return None

def get_date_registered(name):
    name = reformat_name(name)
    blockRegistered = get_block_id_registered(name)
    if blockRegistered != None:
        blockData = _get_block_by_block_height(blockRegistered)
        timestamp = _get_timestamp_from_block_data(blockData)
        date = convert_timestamp_to_date(timestamp)
        return date
    return None

def reformat_name(name):
    name = name.lower()
    return name

def check_name_valid(name):
    for i in name:
        asciiCode = int(ord(i))
        if asciiCode <= 44:
            return False
        elif asciiCode == 47:
            return False
        elif asciiCode >= 58 and asciiCode <= 94:
            return False
        elif asciiCode == 96:
            return False
        elif asciiCode >= 123 and asciiCode <= 125:
            return False
        elif asciiCode >= 127:
            return False
    return True

print(resolve_ergoname("~balb"))