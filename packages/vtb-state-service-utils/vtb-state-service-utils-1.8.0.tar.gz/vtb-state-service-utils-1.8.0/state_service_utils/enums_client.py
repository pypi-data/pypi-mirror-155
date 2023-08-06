import datetime
import json
import logging
import os
import shutil
from enum import Enum
from typing import Optional
from cloud_sdk.config import KeycloakConfigService
from cloud_sdk.sdk import get_sdk

from state_service_utils.conf import (
    REFERENCES_MOCK,
    REFERENCES_HOST_URL,
    SSL_VERIFY,
    REFERENCES_TIMEOUT,
    REFERENCES_FETCH_INTERVAL,
    KEYCLOAK_CONFIG,
    REFERENCES_MOCK_FILE
)
logger = logging.getLogger('default')


def _create_enums_values(data: dict) -> dict:
    return {k: v if v is not None else k.lower() for k, v in data.items()}


def _deserialize(pages: list) -> dict:
    return {page.name: Enum(page.name, _create_enums_values(page.data)) for page in pages}


class EnumsClient:  # __base__
    def __init__(self, *args, **kwargs):
        self._data = dict()

    def __getattr__(self, item):
        if item not in self._data:
            self.update()
        return self._data[item]

    def update(self):
        raise NotImplementedError


class EnumsHttpClient(EnumsClient):
    def __init__(self, sdk, fetch_interval=60, *args, **kwargs):
        super(EnumsHttpClient, self).__init__(*args, **kwargs)

        self.sdk = sdk
        self.fetch_interval = datetime.timedelta(seconds=fetch_interval)
        self.last_fetch = None

    def __getattr__(self, item):
        if self.last_fetch + self.fetch_interval <= datetime.datetime.now():
            self.update()
            return self._data[item]
        return super(EnumsHttpClient, self).__getattr__(item)

    def update(self) -> bool:
        fetching_dt = datetime.datetime.now()
        try:
            data = self.fetch_remote()
        except Exception as err:
            msg = (
                'Exception while connecting to references service. '
                f'REFERENCES_HOST_URL: {self.sdk.config.base_url}, '
                f'REFERENCES_TIMEOUT: {self.sdk.config.timeout}, '
                f'Original exception: {err}'
            )
            # if there is only the first connection attempt, then raise ConnectionError
            if not self.last_fetch:
                raise ConnectionError(msg)
            # otherwise, log it and try to reconnect after the period
            logger.warning(msg)
            self.last_fetch = fetching_dt
            return False
        self._data = _deserialize(data)
        self.last_fetch = fetching_dt
        logger.debug(f"updated: {', '.join((k for k in self._data))}")
        return True

    def fetch_remote(self) -> list:
        with self.sdk.pool_references_service.get() as client:
            if self.sdk.config.keycloak is not None:
                token = self.sdk.keycloak.get_access_token()
                client.auth(token=token)
            pages = client.pages.list(directory__name='enums')
        if not isinstance(pages, list):
            raise ValueError(f'server response should be a list.')
        return pages


class EnumsCacheFileClient(EnumsClient):
    def __init__(self, cache_file, *args, **kwargs):
        super(EnumsCacheFileClient, self).__init__(*args, **kwargs)
        self._cache_file = self._create_cache_file(cache_file)

    def update(self) -> bool:
        with open(self._cache_file) as f:
            data = json.load(f)
        self._data = _deserialize(data)
        return True

    @staticmethod
    def _create_cache_file(abs_path: Optional[str]):
        if not os.path.exists(abs_path):
            logger.warning(
                "You're using `REFERENCES_MOCK` without providing cache file.\n"
                "It will be automatically created with data from template.\n"
                "Now you can manually add or change any enums in %s" % abs_path
            )
            os.makedirs(os.path.dirname(abs_path), exist_ok=True)
            src = os.path.join(os.path.dirname(__file__), 'datafiles', 'enums_template.json')
            shutil.copy(src, abs_path)
        return abs_path


def _initialize() -> EnumsClient:
    if REFERENCES_MOCK:
        client = EnumsCacheFileClient(cache_file=REFERENCES_MOCK_FILE)
    else:
        keycloack_cfg = KeycloakConfigService(
            url=KEYCLOAK_CONFIG.server_url,
            client_id=KEYCLOAK_CONFIG.client_id,
            client_secret_key=KEYCLOAK_CONFIG.client_secret_key,
            ssl_verify=KEYCLOAK_CONFIG.verify,
            realm_name=KEYCLOAK_CONFIG.realm_name
        ) if KEYCLOAK_CONFIG else None
        sdk = get_sdk(
            url=REFERENCES_HOST_URL,
            ssl_verify=SSL_VERIFY,
            timeout=REFERENCES_TIMEOUT,
            keycloak=keycloack_cfg
        )
        client = EnumsHttpClient(
            sdk=sdk,
            fetch_interval=REFERENCES_FETCH_INTERVAL
        )
    client.update()
    return client


enums = _initialize()
