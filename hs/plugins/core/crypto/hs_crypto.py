from interfaces import HSPlugin
from pluggy import HookimplMarker
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import os

hs_crypto = HookimplMarker("hs")


class HSCrypto(HSPlugin):
    name = "hs_crypto"

    def __init__(self):
        super().__init__()
        self.file_dir = ""
        self.id_rsa = None
        self.id_rsa_pub = None
        self.private_keyfile = None
        self.public_keyfile = None
        self.crypto_enabled = True
        self.crypto_behaviour: CryptoBehaviour = None

    def activate(self):
        self.file_dir = self.pm.hook.filepath_get(plugin_name=self.name)[0]
        self.private_keyfile = os.path.join(self.file_dir, "id_rsa")
        self.public_keyfile = os.path.join(self.file_dir, "id_rsa.pub")
        try:
            self.load_keypair()
        except:
            self.generate_keypair()

        # == "False" to prevent accidentally turning off. "False" must be explicit
        if (
            self.pm.hook.settings_get_value(setting_name="CRYPTOGRAPHY_ENABLED")[0]
            == "False"
        ):
            self.log.warning(
                "cryptography is disabled. Sensitive data may surface in event streams"
            )
            self.crypto_enabled = False
            self.crypto_behaviour = Fake(self.id_rsa_pub, self.id_rsa)
            self.event(
                event_type="behaviour_set",
                event_data={"behaviour": "Fake"},
                event_metadata={},
            )
        else:
            self.crypto_behaviour = Real(self.id_rsa_pub, self.id_rsa)
            self.event(
                event_type="behaviour_set",
                event_data={"behaviour": "Real"},
                event_metadata={},
            )
        self.log.notice(f"activated {self.order}")

    def load_keypair(self):
        self.id_rsa = self.load_private_key()
        self.id_rsa_pub = self.load_public_key()

    def generate_keypair(self):
        p_key = self.generate_private_key()
        self.save_private_key(p_key)
        self.save_public_key(p_key.public_key())
        self.id_rsa = self.load_private_key()
        self.id_rsa_pub = self.load_public_key()

    @hs_crypto
    def crypto_encrypt(self, plaintext):
        """
        Encrypts a string using the server's key
        :param plaintext: string to encrypt
        :return: b'<encrypted string>'
        """
        return self.crypto_behaviour.encrypt(plaintext)

    @hs_crypto
    def crypto_decrypt(self, ciphertext):
        """
        Decrypts a string using the server's key
        :param ciphertext: b'<encrypted string>'
        :return: plaintext str
        """
        return self.crypto_behaviour.decrypt(ciphertext)

    @staticmethod
    def generate_private_key():
        """
        Returns a private key object
        :return:
        """
        return rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )

    def save_private_key(self, key):
        """
        Stores private key
        :param key: key to write to file
        """
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        with open(self.private_keyfile, "wb") as f:
            f.write(pem)
        self.event(
            event_type="save_private_key",
            event_data={"file": self.private_keyfile},
            event_metadata={},
        )
        self.log.notice(f"saved private key to {self.private_keyfile}")

    def save_public_key(self, key):
        """
        Stores public key
        :param key: key to write to file
        """
        pem = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        self.log.warning(
            f"New keypair generated, you can find the public key at {self.public_keyfile}"
        )
        self.log.notice(f"Public key follows:\n\n{pem.decode('utf-8')}")
        with open(self.public_keyfile, "wb") as f:
            f.write(pem)
        self.event(
            event_type="save_public_key",
            event_data={"file": self.public_keyfile, "public_key": pem},
            event_metadata={},
        )
        self.log.notice(f"saved public key to {self.public_keyfile}")

    def load_private_key(self):
        """
        Loads private key from file
        """
        with open(self.private_keyfile, "rb") as id_f:
            key = serialization.load_pem_private_key(
                id_f.read(), password=None, backend=default_backend()
            )
        self.event(
            event_type="load_private_key",
            event_data={"file": self.private_keyfile},
            event_metadata={},
        )
        self.log.notice(f"loaded private key {self.private_keyfile}")
        return key

    def load_public_key(self):
        """
        Loads public key from file
        """
        with open(self.public_keyfile, "rb") as id_pub_f:
            key = serialization.load_pem_public_key(
                id_pub_f.read(), backend=default_backend()
            )
        self.event(
            event_type="load_public_key",
            event_data={"file": self.public_keyfile, "public_key": key},
            event_metadata={},
        )
        self.log.notice(f"loaded public key {self.public_keyfile}")
        return key


class CryptoBehaviour:
    def __init__(self, id_rsa_pub, id_rsa):
        self.id_rsa_pub = id_rsa_pub
        self.id_rsa = id_rsa

    def encrypt(self, message):
        raise NotImplementedError

    def decrypt(self, message):
        raise NotImplementedError


class Real(CryptoBehaviour):
    def encrypt(self, message):
        """
        Encrypts a string using the server's key
        :param message: string to encrypt
        :return: b'<encrypted string>'
        """
        return self.id_rsa_pub.encrypt(
            message.encode("utf-8"),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    def decrypt(self, message):
        """
        Decrypts a string using the server's key
        :param message: b'<encrypted string>'
        :return: plaintext str
        """
        return self.id_rsa.decrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        ).decode("utf-8")


class Fake(CryptoBehaviour):
    def decrypt(self, message):
        """
        Stub method to conform to interface without performing cryptography
        :param message: string to not decrypt
        :return: not decrypted string
        """
        return message.decode("utf-8")

    def encrypt(self, message):
        """
         Stub method to conform to interface without performing cryptography
         :param message: string to not encrypt
         :return: not encrypted string
         """
        return message.encode("utf-8")
