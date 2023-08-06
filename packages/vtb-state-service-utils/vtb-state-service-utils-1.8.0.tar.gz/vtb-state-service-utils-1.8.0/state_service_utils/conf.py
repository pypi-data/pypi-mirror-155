import os
import warnings

from envparse import env
from vtb_http_interaction.keycloak_gateway import KeycloakConfig
from vtb_http_interaction.services import DEFAULT_RETRY_ON_STATUSES

DEBUG = env.bool("DEBUG", default=False)
STATE_SERVICE_URL = env.str("STATE_SERVICE_URL", default=None)
STATE_SERVICE_TOKEN = env.str('STATE_SERVICE_TOKEN', default=None)
STATE_SERVICE_MOCK = env.bool('STATE_SERVICE_MOCK', default=False)

KEYCLOAK_SERVER_URL = env.str("KEY_CLOAK_SERVER_URL", default=None) or env.str("KEYCLOAK_SERVER_URL", default=None)
KEYCLOAK_REALM_NAME = env.str("KEY_CLOAK_REALM_NAME", default=None) or env.str("KEYCLOAK_REALM_NAME", default=None)
KEYCLOAK_CLIENT_ID = env.str("KEY_CLOAK_CLIENT_ID", default=None) or env.str("KEYCLOAK_CLIENT_ID", default=None)
KEYCLOAK_CLIENT_SECRET_KEY = env.str("KEY_CLOAK_CLIENT_SECRET_KEY", default=None) or env.str(
    "KEYCLOAK_CLIENT_SECRET_KEY", default=None)

# references
REFERENCES_MOCK = env.bool('REFERENCES_MOCK', default=False)
REFERENCES_MOCK_FILE = env.str('REFERENCES_MOCK_FILE', default=os.path.join(os.getcwd(), 'cache', 'enums.json'))
REFERENCES_TIMEOUT = env.int('REFERENCES_TIMEOUT', default=2)
REFERENCES_FETCH_INTERVAL = env.int('REFERENCES_FETCH_INTERVAL', default=60)
REFERENCES_HOST_URL = env.str('REFERENCES_HOST_URL').rstrip('/') + env.str(
    'REFERENCES_ENUMS_PATH', default='/api/v1/pages/?directory__name=enums'
)
SSL_VERIFY = env.bool('SSL_VERIFY', default=False)

KEYCLOAK_CONFIG = None
if KEYCLOAK_SERVER_URL and \
        KEYCLOAK_REALM_NAME and KEYCLOAK_CLIENT_ID and KEYCLOAK_CLIENT_SECRET_KEY:
    KEYCLOAK_CONFIG = KeycloakConfig(
        server_url=KEYCLOAK_SERVER_URL,
        client_id=KEYCLOAK_CLIENT_ID,
        realm_name=KEYCLOAK_REALM_NAME,
        client_secret_key=KEYCLOAK_CLIENT_SECRET_KEY
    )

LOG_FULL = 'full'
LOG_SHORT = 'short'

RETRY_ON_STATUSES = frozenset(DEFAULT_RETRY_ON_STATUSES | {502})

if not DEBUG and not (STATE_SERVICE_MOCK or STATE_SERVICE_TOKEN or KEYCLOAK_CONFIG):
    raise EnvironmentError(
        '`STATE_SERVICE_TOKEN` or `KEYCLOAK_CONFIG` is required when you`re not using `STATE_SERVICE_MOCK` or debug.')

if STATE_SERVICE_TOKEN:
    # TODO: Удалить класс в версии 2.0.0
    warnings.warn(
        'Поддержка переменной окружение STATE_SERVICE_TOKEN будет удалена в версии 1.7.0. \
Настройте интеграцию с keycloak, указав KEYCLOAK_SERVER_URL, \
KEYCLOAK_REALM_NAME, KEYCLOAK_CLIENT_ID и KEYCLOAK_CLIENT_SECRET_KEY.',
        DeprecationWarning, stacklevel=2)
