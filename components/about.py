import flet as ft
import webbrowser

from constants.constants import APP_VERSION
from constants.constants import APP_NAME
from constants.constants import WEB_PORTO
from constants.constants import DEVELOPER
from constants.constants import DONATION_LINK

def open_web(e):
    webbrowser.open(WEB_PORTO, new=2)

def open_support(e):
    webbrowser.open(DONATION_LINK, new=2)

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
            ft.Divider(height=40, opacity=0),
            ft.Row(
                [
                    ft.Text("Support developer to give some fuel to maintain this app", size=16),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    ft.TextButton(
                        content=ft.Container(
                            content=ft.Text("Support Developer")
                        ),
                        on_click=open_support
                    )
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