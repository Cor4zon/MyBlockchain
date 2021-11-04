import hashlib, json, sys
import random

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





# txnBuffer = [makeTransaction() for _ in range(50)]
