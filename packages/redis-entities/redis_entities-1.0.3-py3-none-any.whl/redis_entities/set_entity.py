from .base_entity import BaseRedisEntity


class RedisSetEntity(BaseRedisEntity):
    @classmethod
    def add(cls, identifier, *values):
        identifier = cls.build_identifier(identifier)
        values = [cls.encrypt_data(identifier, value) for value in values]
        cls.RedisClient.sadd(identifier, *values)
        cls.add_expiration(identifier)

    @classmethod
    def delete(cls, identifier, *values):
        identifier = cls.build_identifier(identifier)
        values = [cls.encrypt_data(identifier, value) for value in values]
        cls.RedisClient.srem(identifier, *values)

    @classmethod
    def clear(cls, identifier):
        cls.RedisClient.delete(cls.build_identifier(identifier))

    @classmethod
    def exists(cls, identifier, value):
        identifier = cls.build_identifier(identifier)
        value = cls.encrypt_data(identifier, value)
        return bool(cls.RedisClient.sismember(identifier, value))

    @classmethod
    def list_all(cls, identifier):
        return cls.RedisClient.smembers(cls.build_identifier(identifier))

    @classmethod
    def length(cls, identifier):
        return cls.RedisClient.scard(cls.build_identifier(identifier))
