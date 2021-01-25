# pushover-client

---

This package provides an easy-to-use Python 3 interface for the Pushover API.
Written in pure Python off the `requests` module.

---

## Install
```
python3 -m pip install git+https://github.com/Nythepegasus/pushover-client/
```

---

## Supported Features
### Client
* `send`: Send a Message/Glance through the API.
* `verify_user`: Verifies that the current user_token and api_key are valid and working.
* `get_limits`: Get the current api_key's limits.
* `get_receipt`: Gets the receipt of a priority 2 Message.
### Message
* `message`: The message of the notification, can contain HTML.
* `title`: An optional title message.
* `attachment`: An optional png/jpeg image attachment.
* `device`: Optionally specify a specific device to send it to.
* `url`: An optional supplementary URL.
* `url_title`: An optional title for the supplementary URL.
* `priority`: The priority at which the message is sent.
* `sound`: The sound that plays when the notification arrives.
* `timestamp`: The UNIX timestamp that the message is marked with.
* `retry`: Number of seconds to retry sending a priority 2 message.
* `expire`: Number of seconds when to stop retrying to send a priority 2 message.
### Glance
* `title`: An optional title for the Glance.
* `text`: A line of text to display with the Glance.
* `subtext`: A second line of text to display with the Glance.
* `count`: The number to display on the Glance widget.
* `percent`: The percentage to display on the Glance widget.

---

## Examples
A simple example to send a message through the API:
```python
from pushover import Client, Message
client = Client("user_token", "api_token")
msg = Message("This is a sample message!", title="Howdy!")
r = client.send(msg)
print(r.status_code)
# 200 if sent correctly 
```

A simple way to send a Glance through the API:
```python
from pushover import Client, Glance
client = Client("user_token", "api_token")
glance = Glance(title="Howdy!", count=100, percent=84)
r = client.send(glance)
print(r.status_code)
# 200 if sent correctly
```

