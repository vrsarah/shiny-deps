from shiny import App, render, ui
import os
import pwd

app_ui = ui.page_fluid(
    ui.input_slider("n", "N slider", 0, 100, 20),
    ui.output_text_verbatim("txt"),
    ui.div(f"Linux user running user code: {pwd.getpwuid(os.getuid()).pw_name}"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        return f"n*2 is going to be {input.n() * 2}"


app = App(app_ui, server)
