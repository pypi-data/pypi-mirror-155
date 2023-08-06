from abc import ABC
import logging
import functools
from pathlib import PurePath
import ipywidgets as widgets

import clease
from clease_gui.style_mixin import WidgetStyleMixin
from clease_gui.status_bar import update_app_data_statusbar
from clease_gui.event_context import EventContextManager, log_error
from clease_gui.dashboard_interface import DashboardInterface
from clease_gui import utils
from clease_gui.logging_widget import register_logger

__all__ = ["BaseDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


class BaseDashboard(DashboardInterface, WidgetStyleMixin, ABC):
    def get_cwd(self):
        return self.app_data[self.KEYS.CWD]

    @property
    def dev_mode(self) -> bool:
        """Are we in developer mode?"""
        return self.app_data.get(self.KEYS.DEV_MODE, False)

    @property
    def debug(self) -> bool:
        """Alternative name for dev mode"""
        return self.dev_mode

    def log_error(self, logger, *args, **kwargs) -> None:
        """Log as exception if we're in dev mode, otherwise only log as error"""
        log_error(*args, logger=logger, dev_mode=self.dev_mode, **kwargs)

    def event_context(self, logger=None) -> EventContextManager:
        """Context where events which shouldn't
        crash the GUI even on an exception are run"""
        return EventContextManager(logger=logger, dev_mode=self.dev_mode)

    @property
    def settings(self) -> clease.settings.ClusterExpansionSettings:
        """Short-cut for accessing settings, since this is a common operation.
        Raises a KeyError if it doesn't exist."""
        try:
            return self.app_data[self.KEYS.SETTINGS]
        except KeyError:
            # Raise a better message
            raise KeyError("No settings present. Create/load a settings object first.") from None

    def get_db_name(self) -> PurePath:
        """Return the DB name form the settings, and prepend the current
        working directory"""
        settings = self.settings
        cwd = self.app_data[self.KEYS.CWD]
        return cwd / settings.db_name

    def make_event_button(
        self,
        *click_event,
        description="",
        lock_button: bool = True,
        pass_button_event: bool = False,
        **button_kwargs,
    ) -> widgets.Button:
        events = [
            self._event_wrapper(event, pass_button_event=pass_button_event) for event in click_event
        ]
        button = utils.make_clickable_button(
            *events,
            description=description,
            lock_button=lock_button,
            **button_kwargs,
        )
        return button

    def _event_wrapper(self, func, pass_button_event=False):
        @functools.wraps(func)
        @update_app_data_statusbar(self.app_data)
        def _wrapper(b):
            # Include the button argument passed in by the click event,
            # and discard it.
            with self.event_context(logger=logger):
                if pass_button_event:
                    return func(b)
                return func()

        return _wrapper
