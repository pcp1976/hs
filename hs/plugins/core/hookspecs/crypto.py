from pluggy import HookspecMarker


hs_crypto = HookspecMarker("hs")


@hs_crypto
def plaintext(plaintext):
    """
    Encrypt a string
    :param plaintext: plaintext
    :return: str - b'ciphertext'
    """
    pass


@hs_crypto
def crypto_decrypt(ciphertext):
    """
    Encrypt a string
    :param ciphertext: b'ciphertext'
    :return: str - plaintext
    """
    pass
