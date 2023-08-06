from .parameters import require_string, require_bytes
from .mixins.mixin_base import MixinBaseClass


class RedisEntityMetaclass(type):
    """
    This metaclass makes sure that all MixinClasses are placed before other classes in
    the mro of the new class. This will then enable the functionality of overriding
    classmethod in the Mixin classes.
    """

    def __new__(mcs, name, bases, namespace):
        mixin_bases = tuple(
            mixin_class
            for mixin_class in bases
            if issubclass(mixin_class, MixinBaseClass)
        )
        other_bases = tuple(
            other_class for other_class in bases if other_class not in mixin_bases
        )
        bases = (*mixin_bases, *other_bases)
        return super().__new__(mcs, name, bases, namespace)


class BaseRedisEntity(metaclass=RedisEntityMetaclass):
    RedisClient = None
    Prefix = ""
    Expire = None

    @classmethod
    def _hash_identifier(cls, identifier) -> str:
        return require_string(identifier)

    @classmethod
    def build_identifier(cls, identifier):
        return f"{cls.Prefix}:{require_string(cls._hash_identifier(identifier))}"

    @classmethod
    def encrypt_data(cls, key, value) -> bytes:
        return require_bytes(value)

    @classmethod
    def decrypt_data(cls, key, value) -> bytes:
        return require_bytes(value)

    @classmethod
    def add_expiration(cls, identifier):
        if isinstance(cls.Expire, int) and cls.Expire >= 0:
            cls.RedisClient.expire(identifier, cls.Expire)
