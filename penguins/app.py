import plotly.express as px
from shiny.express import input, ui
from shinywidgets import render_plotly
from shiny import render, reactive
from palmerpenguins import load_penguins
import seaborn as sns

# Use the built-in function to load the Palmer Penguins dataset
penguins = load_penguins()

ui.page_opts(title="Palmer Penguin's Data: Josiah Randleman", fillable=True)

with ui.sidebar(bg="#f8f8f8", open="open"):
    ui.h2("Sidebar")

    # Dropdown for selecting the attribute to display in the histogram
    # Setting default value to 'bill_length_mm'
    ui.input_selectize(
        "selected_attribute",
        "Choose A Selected Attribute:",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
        multiple=False,
    )

    ui.input_numeric("plotly_bin_count", "Plotly Histogram Bins:", 10)

    ui.input_slider("seaborn_bin_count", "Seaborn Bins:", min=0, max=100, value=25)

    ui.input_checkbox_group(
        "selected_species_list",
        "Choose Species:",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie"],
        inline=False,
    )

    ui.hr()

    ui.a("GitHub", href="https://github.com/jrandl/cintel-02-data", target="_blank")

with ui.navset_card_underline():
    with ui.nav_panel("DataTable"):

        @render.data_frame
        def penguins_DataTable():
            return render.DataTable(penguins)

    with ui.nav_panel("DataGrid"):

        @render.data_frame
        def penguins_DataGrid():
            return render.DataGrid(penguins)


with ui.navset_card_underline():
    with ui.nav_panel("Plotly Histogram"):

        @render_plotly
        def Plotly_Histogram():
            return px.histogram(
                data_frame=filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            )

    with ui.nav_panel("Seaborn Histogram"):

        @render.plot(alt="A Seaborn histogram on penguin body mass in grams.")
        def Seaborn_Histogram():
            return sns.histplot(
                data=filtered_data(),
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
                hue="species",
            )

    with ui.nav_panel("Plotly Scatterplot"):

        @render_plotly
        def Plotly_Scatterplot():
            return px.scatter(
                filtered_data(),
                x=input.selected_attribute(),
                y="body_mass_g",
                color="species",
                title="Plotly Scatterplot: Species",
                labels={"bill_length_mm": "Bill Length", "body_mass_g": "Body Mass"},
                size_max=5,
            )


# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.

@reactive.calc
def filtered_data():
    isSpeciesMatch = penguins["species"].isin(input.selected_species_list())
    return penguins[isSpeciesMatch]
