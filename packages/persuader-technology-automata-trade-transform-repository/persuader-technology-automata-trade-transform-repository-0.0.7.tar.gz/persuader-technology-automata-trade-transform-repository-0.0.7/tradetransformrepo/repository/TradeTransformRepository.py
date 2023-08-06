import logging
from typing import List

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError

from tradetransformrepo.TradeTransform import TradeTransform
from tradetransformrepo.repository.serialize.trade_transform_deserializer import deserialize_trade_transform
from tradetransformrepo.repository.serialize.trade_transform_serializer import serialize_trade_transform

TRADE_TRANSFORMATIONS_KEY = 'TRADE_TRANSFORMATIONS_KEY'


class TradeTransformRepository:

    def __init__(self, options):
        self.log = logging.getLogger('TradeTransformRepository')
        self.log.info('initializing')
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            self.log.warning(f'missing option please provide options {TRADE_TRANSFORMATIONS_KEY}')
            raise MissingOptionError(f'missing option please provide options {TRADE_TRANSFORMATIONS_KEY}')
        if TRADE_TRANSFORMATIONS_KEY not in self.options:
            self.log.warning(f'missing option please provide option {TRADE_TRANSFORMATIONS_KEY}')
            raise MissingOptionError(f'missing option please provide option {TRADE_TRANSFORMATIONS_KEY}')

    def append(self, transform):
        self.log.debug(f'appending trade transform:[{transform}]')
        self.__store_overwrite(transform)

    def store(self, transformations):
        self.log.debug(f'storing trade transform:[{len(transformations)}]')
        self.__store_all(transformations)

    def __store_overwrite(self, trade_transform: TradeTransform):
        all_trade_transform = self.retrieve()
        if trade_transform not in all_trade_transform:
            all_trade_transform.append(trade_transform)
            self.store(all_trade_transform)
        else:
            all_trade_transform = list([et for et in all_trade_transform if et != trade_transform])
            all_trade_transform.append(trade_transform)
            self.store(all_trade_transform)

    def __store_all(self, trade_transformations):
        key = self.options[TRADE_TRANSFORMATIONS_KEY]
        entities_to_store = list([serialize_trade_transform(trade_transform) for trade_transform in trade_transformations])
        self.cache.store(key, entities_to_store)

    def retrieve(self) -> List[TradeTransform]:
        key = self.options[TRADE_TRANSFORMATIONS_KEY]
        raw_entities = self.cache.fetch(key, as_type=list)
        entities = list([deserialize_trade_transform(raw) for raw in raw_entities])
        self.log.debug(f'retrieving trade transforms:[{len(entities)}]')
        return entities

    def remove(self, trade_transform):
        trade_transformations = self.retrieve()
        self.log.debug(f'removing trade transform [{trade_transform}]')
        trade_transformations_without_deleted = list([tt for tt in trade_transformations if tt != trade_transform])
        self.store(trade_transformations_without_deleted)
