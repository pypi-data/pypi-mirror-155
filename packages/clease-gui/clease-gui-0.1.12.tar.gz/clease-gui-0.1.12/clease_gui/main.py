from typing import Optional
from .app_data import AppDataKeys, AppData
from .main_dashboard import MainDashboard
from .singleton import Singleton

__all__ = ["CLEASEGui", "BaseGUI", "display_ui"]


class BaseGUI:
    """The base version of the CLEASE GUI. Not a singleton, so it is better for testing."""

    def __init__(self, app_data: Optional[dict] = None, dev_mode: bool = False):

        if app_data is None:
            # The default app data.
            app_data = AppData(**{AppDataKeys.DEV_MODE: dev_mode})
        # We "write protect" these with property tags.
        self._app_data = app_data
        self._dashboard = MainDashboard(self.app_data)

    @property
    def app_data(self) -> dict:
        return self._app_data

    @property
    def dashboard(self) -> MainDashboard:
        return self._dashboard

    def display(self) -> None:
        """Display the GUI in a notebook"""
        self.dashboard.display()

    @property
    def dev_mode(self) -> bool:
        return self.app_data.get(AppDataKeys.DEV_MODE, False)

    def __repr__(self) -> str:
        # This gets printed if it's the last line in the Jupyter cell,
        # so we don't want to populate it with too much for a regular user.
        cls_name = self.__class__.__name__
        extra_info = ""
        if self.dev_mode:
            extra_info += f"{self.app_data}"
        return f"{cls_name}({extra_info})"


class CLEASEGui(BaseGUI, metaclass=Singleton):
    """The main CLEASE GUI class.
    It is a singleton, so repeated calls to display_ui returns the exact same instance."""

    # This class is a separate class from the CLEASEGui class, in order to allow
    # non-singleton version of the test app.


def display_ui(**kwargs) -> CLEASEGui:
    """The main CLEASE GUI function.
    Add the following lines in a Jupyter notebook cell:

    from clease_gui import display_ui
    display_ui()
    """

    app = CLEASEGui(**kwargs)
    app.display()
    return app
