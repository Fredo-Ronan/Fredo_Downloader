import flet as ft
import requests
import webbrowser

from components.instadownloader import InstaDownloader
from components.ytdownloader import YtDownloader
from components.about import About_App

from constants.constants import APP_VERSION
from constants.constants import APP_NAME
from constants.constants import FETCH_VERSION_API_LINK
from constants.constants import LATEST_VER_LINK


def get_latest_version():
    try:
        response = requests.get(FETCH_VERSION_API_LINK)
        response.raise_for_status()
        release_info = response.json()
        latest_version = release_info['tag_name']
        return latest_version
    except Exception as e:
        print(f"Error fetching latest version: {e}")
        return None

def main(page: ft.Page):
    def close_bottom_sheet_notif(e):
        new_version_bottom_sheet.open = False
        new_version_bottom_sheet.update()

    def navigate_to_update(e):
        webbrowser.open(LATEST_VER_LINK)

    page.title = APP_NAME
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.MainAxisAlignment.CENTER

    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Instagram",
                icon=ft.icons.DOWNLOAD,
                content=InstaDownloader,
            ),
            ft.Tab(
                text="Youtube",
                icon=ft.icons.DOWNLOAD,
                content=YtDownloader,
            ),
            ft.Tab(
                text="About",
                icon= ft.icons.QUESTION_MARK,
                content=About_App,
            ),
        ],
        expand=1,
    )

    page.appbar = ft.AppBar(
        title=ft.Text(APP_NAME, size=30, weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.colors.SURFACE_VARIANT,
    )

    # FETCH LATEST APP VERSION FROM GITHUB RELEASES
    latest_version = get_latest_version()

    # CREATE BOTTOM SHEET FOR NER VERSION NOTIFICATION
    new_version_bottom_sheet = ft.BottomSheet(
        ft.Container(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(f"New version {latest_version} is Available!\n\nCurrent version is {APP_VERSION}\n", text_align=ft.TextAlign.CENTER),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.ElevatedButton("Update", on_click=navigate_to_update),
                            ft.ElevatedButton("Ignore", on_click=close_bottom_sheet_notif),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                ],
                tight=True,
            ),
            padding=20,
        ),
        open=False,
        on_dismiss=close_bottom_sheet_notif,
    )

    # ADD BOTTOM SHEET NEW VERSION NOTIFICATION TO OVERLAY OF THE MAIN PAGE
    page.overlay.append(new_version_bottom_sheet)
    page.add(tabs)

    # CHECK IF THE CURRENT VERSION OF THE APP IS DIFFERENT FROM THE GITHUB RELEASE, THE THE BOTTOM SHEET WILL SLIDE UP
    if latest_version != APP_VERSION:
        new_version_bottom_sheet.open = True
        new_version_bottom_sheet.update()

ft.app(target=main, assets_dir="assets")