import hashlib
import json
import time
import base64
from secrets import compare_digest
from Crypto.Cipher import AES
from .mixin_base import MixinBaseClass
from ..parameters import timestamp2b, b2timestamp, require_bytes
from ..exceptions import DecryptionException


class DeterministicAuthenticatedEncryptionMixin(MixinBaseClass):
    """
    AesKey has to be twice the size of the key required by the underlying cipher (e.g. 64 bytes for AES-256)
    """

    AesKey = b""

    @classmethod
    def encrypt_data(cls, key, value) -> bytes:
        expire = cls.Expire if cls.Expire is not None else 0xFFFFFFFF
        expire = time.time() + expire
        aes = AES.new(require_bytes(cls.AesKey), AES.MODE_SIV)
        aes.update(require_bytes(key))
        payload = timestamp2b(expire) + require_bytes(value)
        ciphertext, tag = aes.encrypt_and_digest(payload)
        payload = {
            "c": base64.b64encode(ciphertext).decode(),
            "t": base64.b64encode(tag).decode(),
        }
        payload = json.dumps(payload).encode()
        return base64.b64encode(payload)

    @classmethod
    def decrypt_data(cls, key, value) -> bytes:
        payload = base64.b64decode(require_bytes(value))
        payload = json.loads(payload)
        for required_key in ("c", "t"):
            if required_key not in payload:
                raise DecryptionException(f"Key {required_key} not in JSON payload")

        ciphertext = base64.b64decode(payload["c"])
        tag = base64.b64decode(payload["t"])

        try:
            aes = AES.new(require_bytes(cls.AesKey), AES.MODE_SIV)
            aes.update(require_bytes(key))
            plaintext = aes.decrypt_and_verify(ciphertext, tag)
        except ValueError as e:
            raise DecryptionException("Decryption Failed")

        expire_timestamp = b2timestamp(plaintext[:8])
        dec_value = plaintext[8:]

        if time.time() > expire_timestamp:
            raise DecryptionException("Value is already marked as expired")

        return dec_value
