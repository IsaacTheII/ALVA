from dash import Dash
import dash_bootstrap_components as dbc


stylesheet = [dbc.themes.SLATE]

# Set up the root directory and environment variables for the Flask server and the Dash app
app = Dash(
    __name__,
    title="OC - Tool",
    update_title=None,
    assets_folder="assets",
    pages_folder="pages",
    external_stylesheets=stylesheet,
    eager_loading=False,
    serve_locally=True,
    server=True,
    suppress_callback_exceptions=True
    )