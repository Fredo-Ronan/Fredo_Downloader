import flet as ft
import webbrowser

from constants.constants import APP_VERSION
from constants.constants import APP_NAME
from constants.constants import WEB_PORTO
from constants.constants import DEVELOPER

def open_web(e):
    webbrowser.open(WEB_PORTO)

About_App = ft.Container(
    content=ft.Column(
        [
            ft.Divider(height=50, opacity=0),
            ft.Row(
                [
                    ft.Text(APP_NAME, size=40, weight=ft.FontWeight.BOLD),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=50, opacity=0),
            ft.Row(
                [
                    ft.Text("Developer and Maintainer", size=30, weight=ft.FontWeight.W_600),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.Text(DEVELOPER, size=25),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.TextButton(
                        content=ft.Container(
                            content=ft.Text(WEB_PORTO, size=20)
                        ),
                        on_click=open_web
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=100, opacity=0),
            ft.Row(
                [
                    ft.Text(f"App Version {APP_VERSION}", size=18, italic=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ]
    )
)