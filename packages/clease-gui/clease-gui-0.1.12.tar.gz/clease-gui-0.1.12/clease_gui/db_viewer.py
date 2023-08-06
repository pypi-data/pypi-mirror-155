import logging
from IPython.display import display, clear_output
import ipywidgets as widgets
import pandas as pd
import ase
import numpy as np

from clease_gui.base_dashboard import BaseDashboard
from clease_gui import register_logger

__all__ = ["DBViewerDashboard"]

logger = logging.getLogger(__name__)
register_logger(logger)


class DBViewerDashboard(BaseDashboard):
    def initialize(self):

        self.db_select_widget = widgets.Text(description="DB name:", value="")
        db_name_help = widgets.Label(
            ("Leave empty to use database specified in the settings object.")
        )

        self.db_select_box = widgets.HBox(children=[self.db_select_widget, db_name_help])

        self.selection_parameters_widget = widgets.Text(description="Selection:", value="")

        selection_help_label = widgets.Label(
            (
                "For more information on querying, see "
                "https://wiki.fysik.dtu.dk/ase/ase/db/db.html#querying"
            )
        )
        self.selection_box = widgets.HBox(
            children=[self.selection_parameters_widget, selection_help_label]
        )

        self.draw_selection_button = self.make_event_button(
            self._draw_selection, description="Open in ASE GUI"
        )

        self.print_db_button = self.make_event_button(self._print_db, description="Show DB content")

        # Output for displaying the ASE database as a pandas DF
        self.db_content_out = widgets.Output(
            layout=dict(
                overflow="auto",
                width="100%",
                height="350px",
            )
        )
        self.max_rows_widget = widgets.BoundedIntText(
            value=50,
            min=0,
            max=99999,
            description="Rows:",
        )
        self.max_rows_help = widgets.Label(
            "Maximum number of rows to display in the table (0 for unlimited)."
        )
        self.count_rows_btn = self.make_event_button(
            self._on_count_rows_click, description="Count Selection"
        )
        self.count_label = widgets.Label(value=None)

    def _on_count_rows_click(self):
        n_rows = self._count_rows()
        self.count_label.value = f"Number of rows: {n_rows}"
        logger.info("Number of rows with selection: %d", n_rows)

    def _count_rows(self):
        con = self.get_connection()
        selection = self.get_selection_parameters()
        return con.count(selection=selection)

    def _print_db(self):
        db_name = str(self.db_name)
        selection = self.get_selection_parameters()
        con = self.get_connection()

        tot = self._count_rows()
        out = self.db_content_out
        logger.info("Querying database %s for %d entries", db_name, tot)

        rows = con.select(selection)
        df = ase_db_rows_to_df(rows, nmax=self.max_rows_widget.value)
        with out:
            clear_output(wait=True)
            with pd.option_context("display.max_rows", None, "display.max_columns", None):
                # Temporarily set display context to all of the rows
                # and columns we have.
                # We don't wanna truncate here.
                display(df)

    def display(self):
        buttons = widgets.HBox(
            children=[
                self.count_rows_btn,
                self.print_db_button,
                self.draw_selection_button,
            ]
        )
        rows_box = widgets.HBox(children=[self.max_rows_widget, self.max_rows_help])
        display(
            self.db_select_box,
            self.selection_box,
            rows_box,
            buttons,
            self.count_label,
            self.db_content_out,
        )

    @property
    def db_name(self):
        value = self.db_select_widget.value
        if value == "":
            # Use DB name from settings
            return self.get_db_name()
        return self.app_data[self.KEYS.CWD] / value

    @property
    def settings(self):
        return self.app_data[self.KEYS.SETTINGS]

    def get_connection(self):
        return ase.db.connect(self.db_name)

    def get_selection_parameters(self):
        value = self.selection_parameters_widget.value
        if value == "":
            return None
        return value

    def get_selection(self):
        selection = self.get_selection_parameters()
        con = self.get_connection()

        return [row.toatoms() for row in con.select(selection=selection)]

    def _draw_selection(self) -> None:
        from ase.visualize import view

        images = self.get_selection()
        # Remove any calculator, to remove energies, and avoid an
        # annoying error.
        # We need to keep using the ase.visualize.view, in order to have
        # it run as a subprocess (multiprocessing & threading don't work :( )
        for image in images:
            image.calc = None
        view(images)


def ase_db_rows_to_df(rows, nmax=0) -> pd.DataFrame:
    """Convert an ASE database into a pandas data frame"""
    # rows = list(rows)
    base_keys = [
        "id",
        "formula",
        "calculator",
        "energy",
        "natoms",
        "pbc",
        "volume",
        "charge",
        "mass",
    ]

    logger.debug("Reading data from database.")
    rows_list = []
    for ii, row in enumerate(rows):
        if nmax > 0 and ii > nmax:
            break
        data = {}
        for key in base_keys:
            data[key] = getattr(row, key, None)
        kvp = row.key_value_pairs
        data.update(**kvp)
        rows_list.append(data)

    logger.debug("Parsing keys...")

    # Get all keys, ensure base keys are sorted in their order
    all_keys = list(base_keys)
    all_keys_set = {key for data in rows_list for key in data}
    for key in all_keys_set:
        if key not in all_keys:
            all_keys.append(key)
    logger.debug("Constructing pandas dataframe.")
    return pd.DataFrame(rows_list, columns=all_keys).replace({np.nan: None})


def _formatter(key, value):
    """Helper function to format the value, possibly
    on the basis of the name of the key"""
    if value is None:
        value = "-"
    if key == "pbc":
        # Convert [True, True, True] => 'TTT'
        # or [True, False, False] => 'TFF'
        value = "".join([str(v)[0] for v in value])

    return value
