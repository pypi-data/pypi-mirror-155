import hashlib

from .mixin_base import MixinBaseClass
from ..parameters import require_bytes


class HashedIdentifierMixin(MixinBaseClass):
    HashName = "sha512_256"
    Salt = b""

    @classmethod
    def _hash_identifier(cls, identifier) -> str:
        return hashlib.new(
            cls.HashName, require_bytes(cls.Salt) + require_bytes(identifier)
        ).hexdigest()
