from typing import Dict, Any, Callable, Union, Sequence
import logging
from collections import defaultdict
from enum import Enum, IntEnum, auto
from pathlib import Path
import attr
from clease import jsonio
from clease_gui.logging_widget import register_logger

__all__ = ["save_app_data", "load_app_data", "AppDataKeys"]

logger = logging.getLogger(__name__)
register_logger(logger)

# Sentinel object for the pop() method.
_SENTINEL = object()


class AppDataKeys(str, Enum):
    """Collection of keys which (may) be in the app_data.
    Keys starting with an '_' will not be saved in the app state."""

    # "private" keys
    CWD = "_cwd"
    STATUS = "_status"
    DEV_MODE = "_dev_mode"
    STEP_OBSERVER = "_mc_step_obs"

    # Regular app data keys
    SUPERCELL = "supercell"
    SETTINGS = "settings"
    ECI = "eci"
    CANONICAL_MC_DATA = "canonical_mc_data"

    # The evaluator cannot be saved to file, so save it as private
    # instance of an Evaluate class
    EVALUATE = "_evaluator"

    @staticmethod
    def is_key_private(key: str) -> bool:
        """Check if a given key is considered 'private'"""
        return key.startswith("_")

    @classmethod
    def is_key_public(cls, key: str) -> bool:
        """Check if a given key is considered 'public'"""
        return not cls.is_key_private(key)

    @classmethod
    def iter_public_keys(cls):
        yield from filter(cls.is_key_public, cls)

    @classmethod
    def iter_private_keys(cls):
        yield from filter(cls.is_key_private, cls)


class Notifier(IntEnum):
    """Type of notification"""

    SET = auto()
    DELETE = auto()
    POP = auto()


@attr.define
class Notification:
    """A notification that something changed in the AppData"""

    key: str = attr.field()
    old_value: Any = attr.field()
    new_value: Any = attr.field()
    notifier: Notifier = attr.field()


class AppData(dict):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Shortcut to AppDataKeys
        self.app_keys = AppDataKeys
        self._subscribers = defaultdict(list)

    def subscribe(self, key: str, func: Callable[[Notification], None]) -> None:
        """Attach a callback function to a key. Whenever a change to the AppData is made
        with that key, the callback function is called. The function should take in a Notification
        object as its only parameter, from which it can also determine if it needs
        to take any action.

        This does not check whether a given key in the app data already exists."""
        self._subscribers[key].append(func)

    def subscribe_many(self, keys: Sequence[str], func: Callable[[Notification], None]) -> None:
        """Subscribe the same callback function to multiple keys."""
        for key in keys:
            self.subscribe(key, func)

    def notify_subscribers(self, key: str, change: Notification) -> None:
        """Notify all subscribers to the given key about the event"""
        for ii, func in enumerate(self._subscribers[key]):
            logger.debug(
                "Notifying subscriber %d '%s' to key '%s' from %s",
                ii,
                func.__name__,
                key,
                change.notifier,
            )
            func(change)

    def pop(self, key: str, default: Any = _SENTINEL) -> Any:
        """Pop an item like in dict.pop(), and then notify anyone who subscribes to that key.
        Notificattion only occurs after the delete."""
        old_value = self.get(key, None)
        if default is _SENTINEL:
            # No default value was provided
            ret_val = super().pop(key)
        else:
            # The user provided _any_ kind of default value
            ret_val = super().pop(key, default)
        change = Notification(key, old_value, None, Notifier.POP)
        self.notify_subscribers(key, change)
        return ret_val

    def __setitem__(self, key: str, value: Any) -> None:
        """Change an item, and then notify anyone who subscribes to that key.
        Notificattion only occurs after the set."""
        old_value = self.get(key, None)
        ret_val = super().__setitem__(key, value)
        change = Notification(key, old_value, value, Notifier.SET)
        self.notify_subscribers(key, change)
        return ret_val

    def __delitem__(self, key: str) -> None:
        """Delete an item, and then notify anyone who subscribes to that key.
        Notificattion only occurs after the delete."""
        old_value = self.get(key, None)
        ret_val = super().__delitem__(key)
        change = Notification(key, old_value, None, Notifier.DELETE)
        self.notify_subscribers(key, change)
        return ret_val

    def update(self, *dicts, **kwargs):
        """Override the built-in update() dict method, to
        use the custom __setitem__ methods."""

        def _update(dct):
            for key, value in dct.items():
                self[key] = value

        # First update over all dictonaries
        for dct in dicts:
            _update(dct)
        # Then iterate each explicit kwarg
        _update(kwargs)


def save_app_data(app_data: Dict[str, Any], fname) -> None:
    """Save entries in the app data which aren't considered private.
    This will not save any subcribed events either."""
    fname = Path(fname)
    data = app_data.copy()
    to_remove = []
    for key in data:
        # Find keys which we don't want to save
        # Any keys starting with a "_" we say
        # we don't want to save
        if AppDataKeys.is_key_private(key):
            to_remove.append(key)
    for key in to_remove:
        data.pop(key, None)

    with fname.open("w") as file:
        jsonio.write_json(file, data)


def load_app_data(fname, as_dict: bool = False) -> Union[AppData, dict]:
    fname = Path(fname)
    with fname.open() as file:
        data = jsonio.read_json(file)
    if as_dict:
        return data
    return AppData(**data)
