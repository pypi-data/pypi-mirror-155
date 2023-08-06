import logging
from typing import List

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError

from missingrepo.Missing import Missing
from missingrepo.repository.serialize.missing_deserializer import deserialize_missing
from missingrepo.repository.serialize.missing_serializer import serialize_missing

MISSING_KEY = 'MISSING_KEY'


class MissingRepository:

    def __init__(self, options):
        self.log = logging.getLogger('MissingRepository')
        self.log.info('initializing')
        self.options = options
        self.__check_options()
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            self.log.warning(f'missing option please provide options {MISSING_KEY}')
            raise MissingOptionError(f'missing option please provide options {MISSING_KEY}')
        if MISSING_KEY not in self.options:
            self.log.warning(f'missing option please provide option {MISSING_KEY}')
            raise MissingOptionError(f'missing option please provide option {MISSING_KEY}')

    def store(self, missings):
        if len(missings) > 0:
            key = self.options[MISSING_KEY]
            entities_to_store = list([serialize_missing(missing) for missing in missings])
            self.log.debug(f'Storing {len(entities_to_store)} missing')
            self.cache.store(key, entities_to_store)

    def append(self, missing):
        self.log.debug(f'appending missing:[{missing}]')
        key = self.options[MISSING_KEY]
        serialized = serialize_missing(missing)
        self.cache.append_store(key, serialized)

    def retrieve(self) -> List[Missing]:
        key = self.options[MISSING_KEY]
        raw_entities = self.cache.fetch(key, as_type=list)
        entities = list([deserialize_missing(raw) for raw in raw_entities])
        self.log.debug(f'Retrieving {len(entities)} missing')
        return entities

    def remove(self, missing):
        self.log.debug(f'removing missing:[{missing}]')
        all_missing = self.retrieve()
        self.log.debug(f'missings before remove:[{len(all_missing)}]')
        all_missing_without_missing = [serialize_missing(m) for m in all_missing if m != missing]
        self.log.debug(f'missings after remove:[{len(all_missing_without_missing)}]')
        key = self.options[MISSING_KEY]
        self.cache.overwrite_store(key, all_missing_without_missing)

    def is_already_missing(self, missing):
        all_missing = self.retrieve()
        return missing in all_missing
