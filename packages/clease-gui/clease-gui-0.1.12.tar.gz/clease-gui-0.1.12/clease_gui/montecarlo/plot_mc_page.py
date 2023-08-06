from typing import Optional
import logging
from IPython.display import display, clear_output
import ipywidgets as widgets
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import savgol_filter
import attr
from clease_gui import register_logger, utils
from clease_gui.base_dashboard import BaseDashboard

__all__ = ["PlotMCDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


@attr.mutable
class PlotUpdater:
    tab_title: str = attr.field()
    update_fnc = attr.field()
    ax = attr.field(default=None)
    filename: Optional[str] = attr.field(default=None)

    def update_plot(self):
        if self.ax is None:
            raise ValueError("No ax object has been assigned yet.")
        self.update_fnc(self.ax)

    def get_plot_filename(self) -> str:
        """The "default" plot filename"""
        if self.filename is not None:
            return self.filename
        # Base the default value on
        return self.tab_title.replace(".", "").replace(" ", "_").lower() + ".png"


class PlotMCDashboard(BaseDashboard):
    def initialize(self):
        plt.ioff()
        self.mode_widget = widgets.Dropdown(
            description="MC mode:",
            options=[
                ("Canonical", "canonical"),
            ],
            **self.DEFAULT_STYLE_KWARGS,
        )
        plot_tabs = []
        self.plot_outputs = []
        self.figures = []

        self.plot_updaters = [
            PlotUpdater("Min. Energy", self._update_emin_plot),
            PlotUpdater("Avg. Energy", self._update_emean_plot),
            PlotUpdater("Accept Rate", self._update_accept_rate_plot),
            PlotUpdater("Heat Capacity", self._update_heat_capacity_plot),
            PlotUpdater(
                "Heat Capacity alt.",
                self._update_heat_capacity_by_diff_plot,
                filename="heat_capacity_by_differentiation.png",
            ),
            PlotUpdater("Energy Variance", self._update_energy_variance_plot),
        ]

        for updater in self.plot_updaters:
            tab = widgets.Output()
            out = widgets.Output()
            with out:
                clear_output()
                with plt.style.context("seaborn"):
                    fig, ax = plt.subplots()
            self.plot_outputs.append(out)
            plot_tabs.append(tab)
            self.figures.append(fig)
            updater.ax = ax  # Save the axis object in the updater

            # Create save fig button/text
            box = self._make_savefig_box(fig, fname=updater.get_plot_filename())
            with tab:
                clear_output()
                display(out, box)

        self.update_button = self.make_event_button(
            self._update_all_plots,
            description="Update Plots",
        )

        self.x_axis_style_widget = widgets.Dropdown(
            description="x axis scale:",
            options=[
                ("Linear", "linear"),
                ("Logarithmic", "log"),
            ],
            value="log",
        )
        self.x_axis_style_widget.observe(self._on_x_axis_change)
        self.plots_tabs = widgets.Tab(children=plot_tabs)
        for ii, updater in enumerate(self.plot_updaters):
            self.plots_tabs.set_title(ii, updater.tab_title)

        self.invert_temp_axis = widgets.Checkbox(
            value=True,
            description="Reverse temperature axis?",
            **self.DEFAULT_STYLE_KWARGS,
        )

    @property
    def axes(self):
        """List of all ax objects"""
        return [updater.ax for updater in self.plot_updaters]

    def display(self):
        top_widgets = widgets.HBox(
            children=[
                self.update_button,
                self.x_axis_style_widget,
            ]
        )
        display(top_widgets)
        display(self.invert_temp_axis, self.mode_widget)

        display(self.plots_tabs)

    def get_key(self, key):
        """Helper function which raises a more useful error message"""
        try:
            return self.app_data[key]
        except KeyError:
            raise KeyError(
                (
                    f"No key {key} available in app data. "
                    "Did you forget to load/run simulation first?"
                )
            )

    def get_data(self):
        mode = self.active_mc_mode
        if mode == "canonical":
            return self.get_key(self.KEYS.CANONICAL_MC_DATA)
        raise NotImplementedError(f"Mode not available: {mode}")

    def _on_x_axis_change(self, change):
        if utils.is_value_change(change):
            self._set_axis_type()

    def _update_all_plots(self):
        logger.info("Updating all MC plots.")
        with plt.style.context("seaborn"):
            for updater in self.plot_updaters:
                updater.update_plot()
            self._set_axis_type()

        for fig, out in zip(self.figures, self.plot_outputs):
            with out:
                clear_output(wait=True)
                display(fig)
        logger.info("Plotting complete.")

    def _update_energy_variance_plot(self, ax):
        ax.clear()
        for run_i, data in enumerate(self.get_data(), start=1):
            x = np.array(data["temperature"])
            y = np.array(data["en_var"])
            ax.plot(x, y, "o--", label=f"Run {run_i}")

        if self.invert_temp_axis.value:
            ax.invert_xaxis()  # Temp goes from high->low

        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel(r"$\langle E^2 \rangle - \langle E \rangle ^2$")
        ax.set_title("Energy Variance")
        self._post_process_ax(ax)

    def _update_heat_capacity_by_diff_plot(self, ax):
        ax.clear()
        for run_i, data in enumerate(self.get_data(), start=1):
            x = np.array(data["temperature"])
            en = _get_e_mean(data, normalize=False)
            filtered = savgol_filter(en, 5, 2)
            y = np.gradient(filtered) / np.gradient(x)
            ax.plot(x, y, "o--", label=f"Run {run_i}")

        if self.invert_temp_axis.value:
            ax.invert_xaxis()  # Temp goes from high->low

        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("Heat Capacity (eV/K)")
        ax.set_title("Heat Capacity from Avg. Energy Differentiation")
        self._post_process_ax(ax)

    def _update_heat_capacity_plot(self, ax):
        ax.clear()
        for run_i, data in enumerate(self.get_data(), start=1):
            x = np.array(data["temperature"])
            y = np.array(data["heat_capacity"])
            ax.plot(x, y, "o--", label=f"Run {run_i}")

        if self.invert_temp_axis.value:
            ax.invert_xaxis()  # Temp goes from high->low

        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("Heat Capacity (eV/K)")
        self._post_process_ax(ax)

    def _update_emin_plot(self, ax):
        ax.clear()
        # Get plot data
        for run_i, data in enumerate(self.get_data()):
            meta = data["meta"]
            natoms = meta["natoms"]
            x = np.array(data["temperature"])
            # Normalize energy to eV/atom
            y = np.array(data["emin"]) / natoms
            if run_i == 0:
                # Normalize to the first energy point of the first run
                E0 = y[0]
            y -= E0
            # Do the plot
            ax.plot(x, y, "o--", label=f"Run {run_i+1}")

        if self.invert_temp_axis.value:
            ax.invert_xaxis()  # Temp goes from high->low

        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel(r"$E_{min} - E_0$ (eV/atom)")
        self._post_process_ax(ax)

    def _update_emean_plot(self, ax):
        ax.clear()
        # Get plot data
        for run_i, data in enumerate(self.get_data()):
            x = np.array(data["temperature"])
            y = _get_e_mean(data)
            if run_i == 0:
                # Normalize to the first energy point of the first run
                E0 = y[0]
            y -= E0
            # Do the plot
            ax.plot(x, y, "o--", label=f"Run {run_i+1}")
        if self.invert_temp_axis.value:
            ax.invert_xaxis()  # Temp goes from high->low
        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel(r"$E_{mean} - E_0$ (eV/atom)")
        self._post_process_ax(ax)

    def _update_accept_rate_plot(self, ax):
        ax.clear()
        # Get plot data
        for run_i, data in enumerate(self.get_data()):
            x = np.array(data["temperature"])
            y = np.array(data["accept_rate"])

            # Do the plot
            ax.plot(x, y, "o--", label=f"Run {run_i+1}")

        if self.invert_temp_axis.value:
            ax.invert_xaxis()

        ax.set_xlabel("Temperature (K)")
        ax.set_ylabel("Accept rate")
        # Accept rate goes from [0, 1], so add a little extra
        # so the dots stay within the plot
        ax.set_ylim([-0.05, 1.05])
        self._post_process_ax(ax)

    @staticmethod
    def _post_process_ax(ax) -> None:
        """Post processing of the axis object, if the updater function choses."""
        legend = ax.legend(frameon=True)
        # This is a nicer legend color when using the seaborn dark grid
        legend.get_frame().set_facecolor("white")

    def _set_axis_type(self):
        value = self.x_axis_style_widget.value
        for ax in self.axes:
            ax.set_xscale(value)

    @property
    def active_mc_mode(self):
        return self.mode_widget.value

    def _make_savefig_box(self, fig, fname: str = "figure.png"):
        """Make an hbox with a save figure button and a text field
        to specify the figure name"""
        fig_name_text = widgets.Text(description="Filename", value=fname)

        def _on_save_click():
            cwd = self.app_data[self.KEYS.CWD]
            fname = str(cwd / fig_name_text.value)

            fig.savefig(fname)
            logger.info("Saved figure to file: %s", fname)

        savefig_button = self.make_event_button(_on_save_click, description="Save Figure")
        # savefig_button = widgets.Button(description="Save Figure")
        # savefig_button.on_click(_on_save_click)
        # Hbox placing the button and text widget side-by-side
        box = widgets.HBox(children=[savefig_button, fig_name_text])
        return box


def _get_e_mean(data: dict, normalize=True) -> np.ndarray:
    meta = data["meta"]
    en = np.array(data["mean_energy"])
    if normalize:
        # Normalize energy to eV/atom
        natoms = meta["natoms"]
        en /= natoms
    return en
