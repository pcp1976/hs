from pluggy import HookspecMarker


hs_crypto = HookspecMarker("hs")


class Crypto:
    @hs_crypto
    def crypto_encrypt(self, plaintext):
        """
        Encrypt a string
        :param string: plaintext
        :return: str - b'ciphertext'
        """
        pass

    @hs_crypto
    def crypto_encrypt(self, ciphertext):
        """
        Encrypt a string
        :param ciphertext: b'ciphertext'
        :return: str - plaintext
        """
        pass
