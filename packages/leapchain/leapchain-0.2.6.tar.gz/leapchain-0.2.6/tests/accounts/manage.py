from nacl.signing import SigningKey, VerifyKey

from leapchain.accounts.manage import create_account


def test_create_account():
    signing_key, account_number = create_account()

    assert isinstance(signing_key, SigningKey)
    assert isinstance(account_number, VerifyKey)
