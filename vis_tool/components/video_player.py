from dash import dcc, html, callback, Input, Output
import dash_player as player

__all__ = ["video_player"]


def video_player(**kwargs):
    return html.Div(
        [
            player.DashPlayer(
                **
                {
                    "playing": False,
                    "volume": 1,
                    "controls": False,
                    "intervalCurrentTime": 400,
                    "width": "100%",
                    "height": "100%",
                    "style": {"background": "#000000"},
                } | kwargs
            ),
        ],
    )