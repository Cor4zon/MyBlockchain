import hashlib, json, sys
import random
import copy

random.seed(0)


def hash_me(msg=""):
    """For convenience, this is a helper function that
    wraps out hashing algorithm
    """

    if type(msg) != str:
        msg = json.dumps(msg, sort_keys=True)

    return hashlib.sha256(str(msg).encode('utf-8')).hexdigest()


def makeTransaction(maxValue=100):
    sign = int(random.getrandbits(1))*2 - 1     # 1 or -1
    amount = random.randint(1, maxValue)
    TinaPays = sign * amount
    MonyaPays = -1 * TinaPays

    return {u'Tina': TinaPays, u'Monya': MonyaPays}


def updateState(txn, state):
    state = state.copy()
    for key in txn:
        if key in state.keys():
            state[key] += txn[key]
        else:
            state[key] = txn[key]
    return state


def isValidTxn(txn, state):
    """
    >>> state = {u'Alice':5,u'Bob':5}
    >>> isValidTxn({u'Alice': -3, u'Bob': 3},state)
    True
    >>> isValidTxn({u'Alice': -4, u'Bob': 3},state)
    False
    >>> isValidTxn({u'Alice': -6, u'Bob': 6},state)
    False
    >>> isValidTxn({u'Alice': -4, u'Bob': 2,'Lisa':2},state)
    True
    >>> isValidTxn({u'Alice': -4, u'Bob': 3,'Lisa':2},state)
    False
    """
    if sum(txn.values()) != 0:
        return False

    for key in txn.keys():
        if key in state.keys():
            acctBalance = state[key]
        else:
            acctBalance = 0
        if (acctBalance + txn[key]) < 0:
            return False

    return True


def makeBlock(txns, chain):
    parentBlock = chain[-1]
    parentHash = parentBlock[u'hash']
    blockNumber = parentBlock[u'contents'][u'blockNumber'] + 1
    txnCount = len(txns)
    blockContents = {
        u'blockNumber': blockNumber,
        u'parentHash': parentHash,
        u'txnCount': txnCount,
        'txns': txns
    }

    blockHash = hash_me( blockContents )
    block = {u'hash': blockHash, u'contents': blockContents}

    return block


def checkBlockHash(block):
    # Raise an exception if the hash not match the block contents
    expectedHash = hash_me( block['contents'] )
    if block['hash'] != expectedHash:
        raise Exception(f"Hash does not match contents"
                        f" of block {block['contents']['blockNumber']}")


def checkBlockValidity(block, parent, state):
    """
    We want to check the following conditions:
        - Each of the transactions are valid updates to the system state
        - Block hash is valid for the block contents
        - Block number increments the parent block number by 1
        - Accurately references the parent block's hash
    """
    parentNumber = parent['contents']['blockNumber']
    parentHash   = parent['hash']
    blockNumber  = block['contents']['blockNumber']

    for txn in block['contents']['txns']:
        if isValidTxn(txn, state):
            state = updateState(txn, state)
        else:
            raise Exception(f"Invalid transaction in block {blockNumber}: {txn}")

    checkBlockHash(block)

    if blockNumber != (parentNumber + 1):
        raise Exception(f"Hash does not match contents of block {blockNumber}")

    return state


def checkChain(chain):
    if type(chain) != str:
        try:
            chain = json.loads(chain)
            assert(type(chain) == list)
        except:
            False
    elif type(chain) != list:
        return False

    state = {}

    for txn in chain[0]['contents']['txns']:
        state = updateState(txn, state)
    checkBlockHash(chain[0])
    parent = chain[0]

    for block in chain[1:]:
        state = checkBlockValidity(block, parent, state)
        parent = block

    return state


state = {u'Alice':50,u'Bob':50}     # Define the initial state
genesisBlockTxns = [state]
genesisBlockContents = {
    u'blockNumber': 0,
    u'parentHash': None,
    u'txnCount': 1,
    u'txns': genesisBlockTxns
}
genesisHash = hash_me( genesisBlockContents )
genesisBlock = {
    u'hash': genesisHash,
    u'contents': genesisBlockContents
}
genesisBlockStr = json.dumps(genesisBlock, sort_keys=True)


# The first element of the Chain
chain = [genesisBlock]

print(checkChain(chain))


"""
blockSizeLimit = 5
txnBuffer = []

while len(txnBuffer) > 0:
    bufferStartSize = len(txnBuffer)

    txnList = []
    while (len(txnBuffer) > 0) & (len(txnList) < blockSizeLimit):
        newTxn = txnBuffer.pop()
        validTxn = isValidTxn(newTxn, state)

        if validTxn:
            txnList.append(newTxn)
            state = updateState(newTxn, state)
        else:
            print("ignored transaction")
            sys.stdout.flush()
            continue

    myBlock = makeBlock(txnList, chain)
    chain.append(myBlock)

"""




# Node A mines the block
nodeBchain = copy.copy(chain)
nodeBtxns = [makeTransaction() for _ in range(5)]
newBlock = makeBlock(nodeBtxns, nodeBchain)
