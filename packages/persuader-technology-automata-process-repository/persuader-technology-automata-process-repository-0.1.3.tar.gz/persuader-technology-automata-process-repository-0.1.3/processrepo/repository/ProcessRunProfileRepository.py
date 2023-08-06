import logging

from cache.holder.RedisCacheHolder import RedisCacheHolder
from core.options.exception.MissingOptionError import MissingOptionError

from processrepo.ProcessRunProfile import ProcessRunProfile
from processrepo.repository.serialize.process_run_profile_deserializer import deserialize_process_run_profile
from processrepo.repository.serialize.process_run_profile_serializer import serialize_process_run_profile

PROCESS_RUN_PROFILE_KEY = 'PROCESS_RUN_PROFILE_KEY'


class ProcessRunProfileRepository:

    def __init__(self, options):
        self.log = logging.getLogger(__name__)
        self.options = options
        self.__check_options()
        self.process_run_profile_key = self.options[PROCESS_RUN_PROFILE_KEY]
        self.cache = RedisCacheHolder()

    def __check_options(self):
        if self.options is None:
            self.log.warning(f'missing option please provide options {PROCESS_RUN_PROFILE_KEY}')
            raise MissingOptionError(f'missing option please provide options {PROCESS_RUN_PROFILE_KEY}')
        if PROCESS_RUN_PROFILE_KEY not in self.options:
            self.log.warning(f'missing option please provide option {PROCESS_RUN_PROFILE_KEY}')
            raise MissingOptionError(f'missing option please provide option {PROCESS_RUN_PROFILE_KEY}')

    def build_process_run_profile_key(self, process_name, market):
        return self.process_run_profile_key.format(market, process_name)

    def store(self, process_run_profile: ProcessRunProfile):
        key = self.build_process_run_profile_key(process_run_profile.name, process_run_profile.market)
        serialized = serialize_process_run_profile(process_run_profile)
        self.cache.store(key, serialized)

    def retrieve(self, process_name, market) -> ProcessRunProfile:
        key = self.build_process_run_profile_key(process_name, market)
        raw_run_profile = self.cache.fetch(key, as_type=dict)
        return deserialize_process_run_profile(raw_run_profile, market, process_name)
