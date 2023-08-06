from abc import abstractmethod
from datetime import datetime
from http.client import HTTPResponse
from typing import Dict, TYPE_CHECKING
from typing import Protocol

from pkm.utils.functionals import run_once

if TYPE_CHECKING:
    from pkm.utils.http.http_client import FetchInfoConfig

TF_HTTP = '%a, %d %b %Y %H:%M:%S GMT'
TF_PACKAGE_UPLOAD_TIME = '%Y-%m-%dT%H:%M:%S'


class CacheDirective(Protocol):

    @abstractmethod
    def is_cache_valid(self, fetch_info: "FetchInfoConfig") -> bool:
        ...

    def add_headers(self, fetch_info: "FetchInfoConfig", headers: Dict[str, str]):
        ...

    def store_result(self, resp: HTTPResponse) -> bool:
        return True

    @classmethod
    @run_once
    def allways(cls) -> "CacheDirective":
        class _Allways(CacheDirective):
            def is_cache_valid(self, fetch_info: "FetchInfoConfig") -> bool:
                return True

        return _Allways()

    @classmethod
    @run_once
    def ask_for_update(cls):
        class _AskUpdate(CacheDirective):
            def is_cache_valid(self, fetch_info: "FetchInfoConfig") -> bool:
                return False

            def add_headers(self, fetch_info: "FetchInfoConfig", headers: Dict[str, str]):
                etag = fetch_info.etag
                if etag:
                    headers['If-None-Match'] = etag
                else:
                    fetch_time = fetch_info.fetch_time
                    if fetch_time is not None:
                        headers['If-Modified-Since'] = fetch_time

        return _AskUpdate()

    @classmethod
    def if_retrieved_after(cls, dt: datetime):
        class _After(CacheDirective):
            def is_cache_valid(self, fetch_info: "FetchInfoConfig") -> bool:
                fetch_time = fetch_info.fetch_time
                if fetch_time is None:
                    return False

                fetch_time = datetime.strptime(fetch_time, TF_HTTP)
                return fetch_time >= dt

        return _After()

    @classmethod
    @run_once
    def never(cls) -> "CacheDirective":
        class _Never(CacheDirective):
            def is_cache_valid(self, fetch_info: "FetchInfoConfig") -> bool:
                return False

            def store_result(self, resp: HTTPResponse) -> bool:
                return False

        return _Never()
