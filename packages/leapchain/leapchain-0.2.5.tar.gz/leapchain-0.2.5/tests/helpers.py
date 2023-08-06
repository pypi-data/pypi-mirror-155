from leapchain.accounts.manage import create_account
from leapchain.verify_keys.verify_key import encode_verify_key


def random_encoded_account_number():
    signing_key, account_number = create_account()
    return encode_verify_key(verify_key=account_number)
