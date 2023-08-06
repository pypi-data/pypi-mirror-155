**State service tools.**

**Quickstart**

```python
from state_service_utils import enums

print(enums.EventType.KEY.value)
```

Enums can be referred to as instance attributes. On first initialization `enums_client` request to the `references` to
fetch all Enums.

---

Any missing Enum will be automatically loaded from the `references` service. If the service does not contain the
requested Enum, the client will raise an `AttributeError`

Following code raise an error, because there is no such `ImportantEnum` either on the service or in the own storage.

```python

from state_service_utils import enums

print(enums.ImportantEnum.KEY.value)  # raise AttributeError
```

---

Set the `REFERENCES_MOCK=True`, for operate without any requests to the remote server. The enumerations will be
loaded from the default template. When the package is initialized, it will be created by path `./cache/enums.json`. The
template file path can be redefined with `REFERENCES_MOCK_FILE`.

Please note that if the file already exists, it will not be overwritten or changed.

___
You need to provide following environments:

- `REFERENCES_HOST_URL` - host url to references service.
- `STATE_SERVICE_URL` - host url to state service.



Following environments are optional:

- `REFERENCES_MOCK` - if True, the client will not send requests to the server.
- `REFERENCES_MOCK_FILE` - the absolute path to templates file destination, by default: `CWD/cache/enums.json`
- `REFERENCES_TIMEOUT` - timeout for every request, by default 1.
- `REFERENCES_FETCH_INTERVAL` - interval for fetching new changes, by default: 60 seconds.
- `STATE_SERVICE_TOKEN` - state service token.
- `STATE_SERVICE_MOCK` - emulate state service.
- `KEY_CLOAK_SERVER_URL`
- `KEY_CLOAK_REALM_NAME`
- `KEY_CLOAK_CLIENT_ID`
- `KEY_CLOAK_CLIENT_SECRET_KEY`
___

```python
import uuid
from state_service_utils import utils, enums


async def test_f(*, order_action: utils.OrderAction, node: str, action_type: enums.ActionSubType, **kwargs):
    print(f"New event: {kwargs}")
    await utils.add_event(
        action=order_action,
        item_id=str(uuid.uuid4()),
        type=enums.EventType.VM.value,
        subtype=enums.EventSubType.CONFIG.value,
        data={'ip': '10.36.134.123', 'flavor': 'large'}
    )
    return {'success': True}


if __name__ == '__main__':
    utils.EventsReceiver(test_f, mq_addr='amqp://guest:guest@localhost/', mq_input_queue='test-queue').run()
```