from abc import ABC, abstractmethod
from clease_gui.app_data import AppData, AppDataKeys


class DashboardInterface(ABC):
    def __init__(self, app_data: AppData, initialize=True):
        """Base class for dashboards.

        :param app_data: Dictionary with application data, which will be passed around
            to all dashboards, and possibly widgets if they need them.
        :param initialize: Bool, toggle whether the ``initialize`` function is called.
            Mainly useful for testing purposes. Should generally be set to True.
        """
        # We make app_data a property, as to protect it, so it's not changed into
        # a new object. Can still be mutated.
        if not isinstance(app_data, AppData):
            raise TypeError(f"Expected AppData type, got {app_data!r}")
        self._app_data = app_data
        # Create access to the constant app data keys through ".KEYS.<some-key>"
        self.KEYS = AppDataKeys
        if initialize:
            self.initialize()

    @abstractmethod
    def initialize(self) -> None:
        """Initialize any widgets related to the dashboard"""

    @abstractmethod
    def display(self) -> None:
        """Display the dashboard"""

    @property
    def app_data(self) -> AppData:
        """Return the app data"""
        return self._app_data
