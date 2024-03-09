import flet as ft

from pytube import YouTube
from pytube.cli import on_progress
import time
from sys import platform
import os
import re
import requests
from pathlib import Path

from lib.instaloader2 import instaloader

# GLOBAL VARIABLES ============================================================================================================
txt_number = ft.TextField(hint_text='Enter youtube link here...', text_align=ft.TextAlign.LEFT)
download_progress = ft.ProgressBar(width=400)
progress_percent = ft.Text("Progress : 0 %")
download_speed = ft.Text("Speed : 0 Kb/s")
download_progress.value = 0
download_loc_info = ""
start_download_time = None


# UTILITIES FUNCTION ==========================================================================================================
def close_invalid_banner(e):
    invalid_link_banner.open = False
    invalid_link_banner.update()

def close_internet_error_pop(e):
    check_internet_pop.open = False
    check_internet_pop.update()

def loading_on():
    circular_loading.opacity = 1
    circular_loading.update()

def loading_off():
    circular_loading.opacity = 0
    circular_loading.update()


def clear_all_info(e):
    progress_percent.value = "0 %"
    download_progress.value = 0
    download_speed.value = "Speed : 0 Kb/s"
    global download_loc_info
    txt_number.value = ""

    download_loc_info = ""
    
    txt_number.update()
    download_speed.update()
    progress_percent.update()
    download_progress.update()
    success_pop.open = False
    success_pop.update()


# POP UP AND BANNER CONSRTUCTION ==================================================================================================
invalid_link_banner = ft.Banner(
    bgcolor=ft.colors.YELLOW_200,
    leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER_700, size=40),
    actions=[
        ft.TextButton(
            content=ft.Container(
                content=ft.Text("OK", color=ft.colors.BLACK, weight=ft.FontWeight.BOLD)
            ), 
            on_click=close_invalid_banner
        ),
    ],
)

success_pop = ft.AlertDialog(
    modal=True,
    title=ft.Text("Download Completed!"),
    actions=[
        ft.TextButton("Ok", on_click=clear_all_info),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    on_dismiss=lambda e: print("Modal dialog dismissed!"),
)

check_internet_pop = ft.AlertDialog(
    modal=True,
    title=ft.Text("Error download!"),
    content=ft.Text("Please check your internet connection and try again..."),
    actions=[
        ft.TextButton("Ok", on_click=close_internet_error_pop),
    ],
    actions_alignment=ft.MainAxisAlignment.END,
    on_dismiss=lambda e: print("Modal dismissed!"),
)

circular_loading = ft.ProgressRing()
circular_loading.opacity = 0

# DOWNLOAD OPERATION ==============================================================================================================
def download_YT(link):
    try:
        loading_on()
        youtube = YouTube(url=link, on_progress_callback=on_progress)
        # get the highest resolution stream
        video_stream = youtube.streams.get_highest_resolution()
        video_title = youtube.title + ".mp4"
        internal_storage_download_path = ""
        global download_loc_info

        # Set the custom directory name
        custom_directory = 'Download'

        # Construct the target directory path
        if platform == 'linux':
            internal_storage_download_path = os.path.join('/storage/emulated/0', custom_directory)
        elif platform == 'win32':
            home_dir = str(Path.home())
            download_dir = os.path.join(home_dir, 'Downloads')

            if os.path.exists(download_dir):
                internal_storage_download_path = download_dir
            else:
                raise Exception('Failed to find download folder')
        elif platform == 'darwin':
            # mac os platform dir implementation
            pass

        # Create the custom directory if it doesn't exist
        os.makedirs(internal_storage_download_path, exist_ok=True)

        loading_off()
        video_stream.download(output_path=internal_storage_download_path, filename=video_title)

        download_loc_info = f"Video disimpan dalam direktori {internal_storage_download_path}"
        popup_success()
    except:
        popup_internet_error()
        loading_off()

def download_youtube(e):
    # parsed_code = parse_link(txt_number.value)
    global start_download_time

    start_download_time = time.time()
    download_YT(txt_number.value)

    # if parsed_code:
    #     download_IG(parsed_code["short_code"])
    # else:
    #     popup_err_link(txt_number.value)


def on_progress(stream, chunk, bytes_remaining):
    global start_download_time
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    download_percentage = (bytes_downloaded / total_size) * 100
    speed = stream.filesize / (time.time() - start_download_time) / 1024
    download_speed_value = f"Speed: {round(speed)} Kb/s" if speed < 1000 else f"Speed : {(speed / 1000):.2f} Mb/s"
    print("UPDATE PROGRESS?")

    # Update UI elements
    download_progress.value = int(download_percentage)
    download_speed.value = download_speed_value
    progress_percent.value = f"Progress: {int(download_percentage)} %"

    download_progress.update()
    download_speed.update()
    progress_percent.update()


# POPUP =======================================================================================================================
def popup_success():
    success_pop.open = True
    success_pop.content = ft.Text(download_loc_info)
    success_pop.update()

def popup_internet_error():
    check_internet_pop.open = True
    check_internet_pop.update()

def popup_err_link(input_value):
    invalid_link_banner.content = ft.Text(f"WARNING! {input_value} is not a valid instagram link. Please provide a valid instagram link.", color=ft.colors.BLACK)
    invalid_link_banner.open = True
    invalid_link_banner.update()

# MAIN FUNCTION ===============================================================================================================
YtDownloader = ft.Container(
    content=ft.Column(
        [
            invalid_link_banner,
            success_pop,
            check_internet_pop,
            ft.Divider(height=50, opacity=0),
            ft.Row(
                [
                    ft.Text("Fredo Youtube Downloader", size=20, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=10, opacity=0),
            ft.Row(
                [
                    txt_number,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=5, opacity=0),
            ft.Row(
                [
                    ft.ElevatedButton(content=ft.Container(
                            content=ft.Text(value='Download', size=20, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.all(10),
                        ), 
                        on_click=download_youtube
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    circular_loading,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=20, opacity=0),
            ft.Row(
                [
                    download_speed,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    download_progress,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Row(
                [
                    progress_percent,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )
)