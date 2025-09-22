
from contextlib import asynccontextmanager
from dishka import Provider, Scope, from_context, provide
from setup.config import Settings
from faststream.redis import RedisBroker, RedisRouter

class TransportProvider(Provider):

    scope =Scope.APP

    settings = from_context(Settings)
    
    redis_broker = from_context(RedisBroker)