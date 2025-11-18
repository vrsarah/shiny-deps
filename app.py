from shiny import App, reactive, render, ui
import numpy as np
import matplotlib.pyplot as plt

# Define UI
app_ui = ui.page_sidebar(
    ui.sidebar(
        ui.h3("Test Controls"),
        ui.input_slider("n", "Number of points", min=10, max=100, value=50),
        ui.input_select("plot_color", "Plot Color",
                        choices=["blue", "red", "green", "purple", "orange"],
                        selected="blue"),
        ui.input_checkbox("show_line", "Show Trend Line", True),
        ui.input_text("title", "Plot Title", "Test Scatter Plot"),
        ui.input_action_button("update", "Update Plot"),
        ui.hr(),
        ui.input_action_button("reset", "Reset All")
    ),
    ui.card(
        ui.card_header("Test Scatter Plot"),
        ui.output_plot("scatter_plot")
    ),
    ui.card(
        ui.card_header("Input Echo"),
        ui.output_text("input_summary")
    )
)


# Define server
def server(input, output, session):
    @reactive.effect
    @reactive.event(input.reset)
    def _():
        ui.update_slider("n", value=50)
        ui.update_select("plot_color", selected="blue")
        ui.update_checkbox("show_line", value=True)
        ui.update_text("title", value="Test Scatter Plot")

    @output
    @render.plot
    @reactive.event(input.update, ignore_none=False)
    def scatter_plot():
        np.random.seed(42)
        n = input.n()
        x = np.random.rand(n)
        y = x + 0.2 * np.random.randn(n)

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.scatter(x, y, color=input.plot_color(), alpha=0.7)

        if input.show_line():
            # Add trend line
            m, b = np.polyfit(x, y, 1)
            ax.plot(x, m * x + b, color="black", linestyle="--")

        ax.set_xlabel("X values")
        ax.set_ylabel("Y values")
        ax.set_title(input.title())

        return fig

    @output
    @render.text
    def input_summary():
        return (
            f"Current Settings:\n"
            f"• Number of points: {input.n()}\n"
            f"• Selected color: {input.plot_color()}\n"
            f"• Show trend line: {'Yes' if input.show_line() else 'No'}\n"
            f"• Plot title: {input.title()}"
        )


# Create the app
app = App(app_ui, server)
