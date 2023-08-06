import logging
from typing import List

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError

from exchangetransformrepo.ExchangeTransform import ExchangeTransform
from exchangetransformrepo.repository.serialize.exchange_transform_deserializer import deserialize_exchange_transform
from exchangetransformrepo.repository.serialize.exchange_transform_serializer import serialize_exchange_transform

EXCHANGE_TRANSFORMATIONS_KEY = 'EXCHANGE_TRANSFORMATIONS_KEY'


class ExchangeTransformRepository:

    def __init__(self, options):
        self.log = logging.getLogger('ExchangeTransformRepository')
        self.log.info('initializing')
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            self.log.warning(f'missing option please provide options {EXCHANGE_TRANSFORMATIONS_KEY}')
            raise MissingOptionError(f'missing option please provide options {EXCHANGE_TRANSFORMATIONS_KEY}')
        if EXCHANGE_TRANSFORMATIONS_KEY not in self.options:
            self.log.warning(f'missing option please provide option {EXCHANGE_TRANSFORMATIONS_KEY}')
            raise MissingOptionError(f'missing option please provide option {EXCHANGE_TRANSFORMATIONS_KEY}')

    def append(self, exchange_transform):
        self.log.debug(f'appending exchange transform [{exchange_transform}]')
        self.__store_overwrite(exchange_transform)

    def store(self, exchange_transform):
        if type(exchange_transform) is ExchangeTransform:
            self.log.debug(f'append exchange transform [{exchange_transform}]')
            self.__store_overwrite(exchange_transform)
        elif type(exchange_transform) is list:
            self.log.debug(f'overwriting exchange transforms [{len(exchange_transform)}]')
            self.__store_all(exchange_transform)

    def __store_overwrite(self, exchange_transform: ExchangeTransform):
        all_exchange_transform = self.retrieve()
        if exchange_transform not in all_exchange_transform:
            self.log.debug(f'append new exchange transform [{exchange_transform}]')
            all_exchange_transform.append(exchange_transform)
            self.store(all_exchange_transform)
        else:
            self.log.debug(f'append replace exchange transform [{exchange_transform}]')
            all_exchange_transform = list([et for et in all_exchange_transform if et != exchange_transform])
            all_exchange_transform.append(exchange_transform)
            self.store(all_exchange_transform)

    def __store_all(self, exchange_transformations):
        key = self.options[EXCHANGE_TRANSFORMATIONS_KEY]
        entities_to_store = list([serialize_exchange_transform(exchange_transform) for exchange_transform in exchange_transformations])
        self.cache.store(key, entities_to_store)

    def retrieve(self) -> List[ExchangeTransform]:
        key = self.options[EXCHANGE_TRANSFORMATIONS_KEY]
        raw_entities = self.cache.fetch(key, as_type=list)
        entities = list([deserialize_exchange_transform(raw) for raw in raw_entities])
        return entities
