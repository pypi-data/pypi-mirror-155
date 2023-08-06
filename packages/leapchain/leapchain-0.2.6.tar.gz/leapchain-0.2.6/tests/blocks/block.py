from tests.helpers import random_encoded_account_number

from leapchain.accounts.manage import create_account
from leapchain.blocks.block import generate_block
from leapchain.constants.network import BANK, PRIMARY_VALIDATOR, SIGNATURE_LENGTH
from leapchain.verify_keys.verify_key import encode_verify_key


def test_generate_block():
    signing_key, account_number = create_account()
    encoded_account_number = encode_verify_key(verify_key=account_number)

    transactions = [
        {
            'amount': 1,
            'fee': BANK,
            'recipient': random_encoded_account_number(),
        },
        {
            'amount': 1,
            'fee': PRIMARY_VALIDATOR,
            'recipient': random_encoded_account_number(),
        },
        {
            'amount': 5,
            'memo': 'Hello there I am 123 years old',
            'recipient': random_encoded_account_number(),
        }
    ]

    block = generate_block(
        account_number=account_number,
        balance_lock=encoded_account_number,
        signing_key=signing_key,
        transactions=transactions
    )

    assert block['account_number'] == encoded_account_number
    assert block['message']['balance_key'] == encoded_account_number
    assert len(block['message']['txs']) == 3
    assert len(block['signature']) == SIGNATURE_LENGTH
