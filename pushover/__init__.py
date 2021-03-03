import requests
import mimetypes
from time import time

SOUNDS = [
    "pushover",
    "bike",
    "bugle",
    "cashregister",
    "classical",
    "cosmic",
    "falling",
    "gamelan",
    "incoming",
    "intermission",
    "magic",
    "mechanic",
    "pianobar",
    "siren",
    "spacealarm",
    "tugboat",
    "alien",
    "climb",
    "persistent",
    "echo",
    "updown",
    "vibrate",
    "none"
]

PRIORITIES = [
    -2,
    -1,
    0,
    1,
    2
]

ATTACHMENT_TYPES = [
    "image/jpeg",
    "image/png"
]


class Message:
    """
    A normal Message that can be sent through the Pushover API. To be displayed as a normal push notification.
    """

    def __init__(self, message: str, title: str = "", attachment: str = "", device: str = "", url: str = "",
                 url_title: str = "", priority: PRIORITIES = 0, sound: SOUNDS = "pushover", timestamp: float = time(),
                 retry: int = 30, expire: int = 10800):
        """
        :param message:
            (Required) A message for the client to send which can be 4096 characters long.
                        It can also have HTML formatting.

        :param title:
            (Optional) A title for the message between 250 characters long.

        :param attachment:
            (Optional) An attachment file for the message.

        :param device:
            (Optional) Specific device to send the message to.

        :param url:
            (Optional) A supplementary URL that can be 512 characters long.

        :param url_title:
            (Optional) A title for the supplementary URL that can be 100 characters long.

        :param priority:
            (Optional) The priority of a message which can be an int from PRIORITIES.
                        Note: If the priority is 2 (emergency), params retry and expire MUST be set.

        :param sound:
            (Optional) A sound for the notification to play, a str from SOUNDS.

        :param timestamp:
            (Optional) A Unix timestamp for the message to display.

        :param retry:
            (Semi-Optional) The number of seconds to retry sending the message. Minimum of 30 seconds.
                                If priority is 2, this MUST be set. Will only work when priority is 2.

        :param expire:
            (Semi-Optional) The number of seconds to stop retrying sending a message. Maximum of 10800 seconds.
                                If priority is 2, this MUST be set. Will only work when priority is 2.

        :property _api_callback:
            The API URL for this type of message.

        :property response_data:
            The requests Response of this particular message.
        """
        if message is None:
            raise ValueError("'message' cannot be None!")
        if attachment != "":
            try:
                open(attachment)
                self._mime_test = mimetypes.guess_type(attachment)[0]
                if self._mime_test not in ATTACHMENT_TYPES:
                    raise ValueError("Attachment file must be valid jpeg/png image!")
            except FileNotFoundError:
                raise FileNotFoundError("Must input a valid file!")
        self.message = str(message)[0:4096]
        self.title = str(title)[0:250]
        self._attachment = str(attachment)
        self.device = str(device)
        self.url = str(url)[0:512]
        self.url_title = str(url_title)[0:100]
        self.priority = int(priority)
        self.sound = str(sound)
        self.timestamp = float(timestamp)
        self.retry = int(retry)
        self.expire = int(expire)
        self.response_data = None
        self._api_callback = "messages.json"

    @property
    def attachment(self):
        if self._attachment != "":
            return {"attachment": (self._attachment, open(self._attachment, "rb"), self._mime_test)}
        else:
            return ""

    @property
    def json(self):
        return {k: v for k, v in (
            ("message", self.message), ("title", self.title), ("device", self.device), ("url", self.url),
            ("url_title", self.url_title), ("priority", self.priority), ("sound", self.sound),
            ("timestamp", self.timestamp), ("retry", self.retry), ("expire", self.expire)) if v != ""}


class Glance:
    """
    A Glance message is a message that is sent to a smart watch or similar device that can display a small amount of information.
    """

    def __init__(self, title: str = None, text: str = None, subtext: str = None, count: int = 0, percent: int = 0):
        """
        :param title:
            (Optional) A title for the glance up to 100 characters.

        :param text:
            (Optional) A line of text for the glance up to 100 characters.

        :param subtext:
            (Optional) A second line of text for the glance up to 100 characters.

        :param count:
            (Optional) An integer that is displayed on the smart watch widget, can be positive or negative.

        :param percent:
            (Optional) A percentage between 0 and 100 that will display on the smart watch widget.

        :property _api_callback:
            The api url for this type of message. Marked read-only for obvious purposes.

        :property response_data:
            The requests Response of this particular message.
        """
        self.title = ""
        self.text = ""
        self.subtext = ""
        if isinstance(text, str):
            self.text = text[0:100]
        if isinstance(title, str):
            self.title = title[0:100]
        if isinstance(subtext, str):
            self.subtext = subtext[0:100]
        if not isinstance(count, int):
            raise ValueError("'count' must be an integer!")
        if not isinstance(percent, int) and not 0 <= percent <= 100:
            raise ValueError("'percent' must be an integer between 0 and 100!")
        self.count = count
        self.percent = percent
        self._api_callback = "glances.json"
        self.response_data = None

    @property
    def json(self):
        return {k: v for k, v in (
            ("title", self.title), ("text", self.text), ("subtext", self.subtext), ("count", self.count),
            ("percent", self.percent)) if v is not None or v != 0}


class Client:
    """
    The client for using the Pushover API.
    """

    def __init__(self, user_key: str, api_token: str):
        """
        :param user_key:
            (Required) The user key for the API.

        :param api_token:
            (Required) The application API token.

        :property api_url:
            The API's base URL. All API calls are built off of this URL.

        :property last_message:
            The last Message/Glance object that was sent with this client.
            Only really useful for priority 2 messages to automatically get receipt information.

        :property api_verify:
            The API path to verify user key and API token correctness.
        """
        self.user_key = user_key
        self.api_token = api_token
        self._api_url = "https://api.pushover.net/1/"
        self.last_message = None
        self._api_verify = "users/validate.json"
        self._api_limits = "apps/limits.json"
        self._api_receipts = "receipts/{}.json"

    def verify_user(self) -> requests.Response:
        """
        Take the client's current api_token and user_key and verify them with the API.

        :return:
            Returns the API request's Response.
        """
        r = requests.post(self._api_url + self._api_verify, json={"token": self.api_token, "user": self.user_key})
        if r.json()["status"] == 1:
            print("User is verified!")
        else:
            print("User is not verified!")
        return r

    def get_limits(self) -> requests.Response:
        """
        Get the current application API limits by using the current api_token.

        :return:
            Returns the API request's Response.
        """
        return requests.get(self._api_url + self._api_limits, params={"token": self.api_token})

    def send(self, msg: [Message, Glance]) -> requests.Response:
        """
        Take either a Message or Glance object and send them through the API.

        :param msg:
            Union[Message, Glance]
                Can either be a Message or Glance object to be sent.

        :return:
            Returns the API request's Response.
        """
        data = {"token": self.api_token, "user": self.user_key}
        data.update(msg.json)
        if getattr(msg, "attachment", "") == "":
            r = requests.post(self._api_url + msg._api_callback, data=data)
        else:
            r = requests.post(self._api_url + msg._api_callback, data=data,
                              files=msg.attachment)
        msg.response_data = r
        self.last_message = msg
        return r

    def get_receipt(self, receipt: str = None) -> requests.Response:
        """
        Get the receipt of a priority 2 Message object.

        :param receipt:
            (Optional) If manually set, it'll request the manual receipt from the API.
                       Otherwise, it'll try to use the client's last_message property.

        :return:
            Returns the API request's Response.
        """
        if receipt is None:
            if self.last_message is None:
                raise ValueError("No last message, please provide receipt!")
            else:
                r = requests.get(
                    self._api_url + self._api_receipts.format(self.last_message.response_data.json()["receipt"]),
                    params={"token": self.api_token})
        else:
            r = requests.get(
                self._api_url + self._api_receipts.format(receipt), params={"token": self.api_token})
        print("Acknowledged: {}".format(r.json()["acknowledged"]))
        return r
