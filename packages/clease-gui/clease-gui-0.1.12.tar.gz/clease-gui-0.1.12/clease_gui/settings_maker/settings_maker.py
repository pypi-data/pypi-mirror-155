import logging
import time
from datetime import timedelta
from typing import NamedTuple
from IPython.display import display, clear_output
import ipywidgets as widgets

import clease
from clease.settings import CEBulk, CECrystal, ClusterExpansionSettings
from clease.corr_func import CorrFunction

from clease_gui import register_logger, utils
from clease_gui.app_data import Notification
from clease_gui.base_dashboard import BaseDashboard
from clease_gui.status_bar import update_statusbar
from . import (
    ConcentrationDashboard,
    StructureSettingsDashboard,
    ClusterDashboard,
    CESettingsDashboard,
)

__all__ = ["SettingsMakerDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


class _SubDashboard(NamedTuple):
    dashboard: BaseDashboard  # Instance of the Dashboard
    tab_name: str

    def make_output(self) -> widgets.Output:
        """Make a new output object, and draw the dashboard on it."""
        out = widgets.Output()
        with out:
            clear_output()
            self.dashboard.display()
        return out


def _make_subtab(*sub_dashboards: _SubDashboard) -> widgets.Tab:
    """Construct the tabs in the sub-dashboards, and initialize their displays"""
    children = [sub.make_output() for sub in sub_dashboards]
    tab = widgets.Tab(children=children)
    for ii, sub in enumerate(sub_dashboards):
        tab.set_title(ii, sub.tab_name)
    return tab


class SettingsMakerDashboard(BaseDashboard):
    """Have the concentration and settings dashboard under 1 tab"""

    def initialize(self):
        self.tab = None

        self.make_settings_btn = utils.make_clickable_button(
            self._on_make_settings_click, description="Make settings"
        )

        self.delete_settings_btn = utils.make_clickable_button(
            self._on_delete_settings_click,
            description="Delete settings",
            button_style="danger",
        )

        self.save_settings_fname = widgets.Text(description="Filename:", value="settings.json")
        self.save_settings_btn = utils.make_clickable_button(
            self._on_save_settings_click, description="Save settings"
        )

        self.save_settings_box = widgets.HBox(
            children=[
                self.save_settings_btn,
                self.save_settings_fname,
            ]
        )

        self.load_settings_fname = widgets.Text(description="Filename:", value="settings.json")
        self.load_settings_btn = self.make_event_button(
            self._on_load_settings_click,
            description="Load settings",
            pass_button_event=True,
        )

        self.load_settings_box = widgets.HBox(
            children=[
                self.load_settings_btn,
                self.load_settings_fname,
            ]
        )

        self._conc_dashboard = ConcentrationDashboard(self.app_data)
        self._crystal_settings_dashboard = StructureSettingsDashboard(self.app_data)
        self._ce_settings_dashboard = CESettingsDashboard(self.app_data)
        self._cluster_dashboard = ClusterDashboard(self.app_data)

        self.tab = _make_subtab(
            _SubDashboard(self._conc_dashboard, "Concentration"),
            _SubDashboard(self._crystal_settings_dashboard, "Crystal Settings"),
            _SubDashboard(self._ce_settings_dashboard, "CE Settings"),
            _SubDashboard(self._cluster_dashboard, "Clusters"),
        )

        self.reconfig_db_button = utils.make_clickable_button(
            self._on_reconfig_click, description="Reconfigure DB"
        )
        self.reconfigure_progress = widgets.IntProgress()
        self.reconfigure_progress_label = widgets.Label()

        self.app_data.subscribe(self.KEYS.SETTINGS, self._on_settings_change)

    @update_statusbar
    @utils.disable_cls_widget("reconfig_db_button")
    def _on_reconfig_click(self, b):
        with self.event_context(logger=logger):
            self.reconfig_db()

    def reconfig_db(self):
        settings = self.settings
        if settings is None:
            raise ValueError("Settings has not been created yet, cannot reconfigure")
        # TODO: Account for CWD?
        logger.info("Reconfiguring database: %s", settings.db_name)

        cf = CorrFunction(settings)
        self.reconfigure_progress.value = 0
        self.reconfigure_progress_label.value = "Starting..."
        t_start = time.perf_counter()
        for row_id, count, total in cf.iter_reconfigure_db_entries():
            dt = timedelta(seconds=int(time.perf_counter() - t_start))
            msg = f"{count}/{total}, ID: {row_id}. Runtime: {dt}"
            self.reconfigure_progress.value = count
            self.reconfigure_progress.max = total
            self.reconfigure_progress_label.value = msg

        dt = timedelta(seconds=time.perf_counter() - t_start)
        logger.info(f"Reconfiguration complete in {dt}.")

    def display(self):
        hbox_btn = widgets.HBox(children=[self.make_settings_btn, self.delete_settings_btn])
        reconfig_widgets = widgets.HBox(
            children=[
                self.reconfig_db_button,
                self.reconfigure_progress,
                self.reconfigure_progress_label,
            ]
        )
        display(
            hbox_btn,
            self.save_settings_box,
            self.load_settings_box,
            reconfig_widgets,
            self.tab,
        )

    def get_concentration(self):
        return self._conc_dashboard.get_concentration()

    @update_statusbar
    @utils.disable_cls_widget("make_settings_btn")
    def _on_make_settings_click(self, b):
        if self.settings is not None:
            logger.error("Cannot make settings, a settings object already exists.")
            return
        logger.info("Making settings...")
        with self.event_context(logger=logger) as cm:
            self.make_settings()
        if not cm.had_error:
            logger.info("Done!")

    @update_statusbar
    @utils.disable_cls_widget("delete_settings_btn")
    def _on_delete_settings_click(self, b):
        try:
            del self.app_data[self.KEYS.SETTINGS]
            logger.info("Removed settings from app data")
        except KeyError:
            logger.info("No settings in app data, cannot delete.")

    def make_settings(self) -> None:
        """Combine the settings in the relevant dashboards, and create the settings"""
        conc = self.get_concentration()
        crystal_kwargs = self._crystal_settings_dashboard.get_settings_kwargs()
        ce_kwargs = self._ce_settings_dashboard.get_settings_kwargs()
        kwargs = dict(**crystal_kwargs, **ce_kwargs)

        settings_type = kwargs.pop("type")
        skew_threshold = kwargs.pop("skew_threshold", None)

        if settings_type == "CEBulk":
            settings = CEBulk(conc, **kwargs)
        elif settings_type == "CECrystal":
            settings = CECrystal(conc, **kwargs)
        elif settings_type == "CESlab":
            # miller = settings_type.pop('miller')
            raise NotImplementedError("Not yet implemneted, yo!")
        else:
            raise ValueError(f"Something is wrong. Got unknown settings_type {settings_type}")

        self.set_settings(settings)
        if skew_threshold is not None:
            self.settings.skew_threshold = skew_threshold

    @property
    def settings(self):
        """Get the settings from the app data"""
        return self.app_data.get(self.KEYS.SETTINGS, None)

    def set_settings(self, settings):
        """Insert settings into the app data"""
        self.app_data[self.KEYS.SETTINGS] = settings

    @property
    def cwd(self):
        return self.app_data[self.KEYS.CWD]

    def get_save_settings_fname(self):
        return self.cwd / self.save_settings_fname.value

    @update_statusbar
    @utils.disable_cls_widget("save_settings_btn")
    def _on_save_settings_click(self, b):
        with self.event_context(logger=logger):
            fname = self.get_save_settings_fname()
            logger.info("Saving settings in file: %s", str(fname))
            self.save_settings(fname)
            logger.info("Save successful.")

    def save_settings(self, fname):
        settings = self.settings
        if settings is None:
            raise RuntimeError("Settings has not been created yet.")
        settings.save(fname)

    def load_settings(self, fname) -> None:
        settings = clease.settings.settings_from_json(fname)
        logger.debug("Loaded settings: %s", settings.todict())
        self.set_settings(settings)
        self.set_settings_widget_states(settings)

    def get_load_settings_fname(self):
        return self.app_data[self.KEYS.CWD] / self.load_settings_fname.value

    def _on_load_settings_click(self, b):
        fname = self.get_load_settings_fname()
        logger.info("Loading settings from file: %s", str(fname))
        self.load_settings(fname)
        logger.info("Load successful.")

    def _on_settings_change(self, notification: Notification):
        assert notification.key == self.KEYS.SETTINGS
        new_val = notification.new_value
        if new_val is not None:
            self.set_settings_widget_states(new_val)

    def set_settings_widget_states(self, settings: ClusterExpansionSettings) -> None:
        """Set the widget states from a new settings object"""
        conc = settings.concentration
        self._conc_dashboard.set_widgets_from_load(conc)
        self._crystal_settings_dashboard.set_widgets_from_load(settings)
        self._ce_settings_dashboard.set_widgets_from_load(settings)
