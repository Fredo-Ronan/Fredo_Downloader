import flet as ft
from kivy.utils import platform

import os
import re
import requests
from pathlib import Path

from lib.instaloader2 import instaloader

# GLOBAL VARIABLES ============================================================================================================
txt_number = ft.TextField(hint_text='Enter instagram link here...', text_align=ft.TextAlign.LEFT)
download_progress = ft.ProgressBar(width=400)
progress_percent = ft.Text("0 %")
download_progress.value = 0
download_loc_info = ""


# UTILITIES FUNCTION ==========================================================================================================
def close_invalid_banner(e):
    invalid_link_banner.open = False
    invalid_link_banner.update()


def clear_all_info(e):
    progress_percent.value = "0 %"
    download_progress.value = 0
    global download_loc_info
    txt_number.value = ""

    download_loc_info = ""
    
    txt_number.update()
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


# DOWNLOAD OPERATION ==============================================================================================================
def parse_link(link):
    clean_up_pattern = re.compile(r'https://www\.instagram\.com/([^/]+)/([^/?]+)/\?.*')
    match = re.search(clean_up_pattern, link)

    if match:
        type = match.group(1)
        short_code = match.group(2)
        print(type)
        print(short_code)
        return {"type": type, "short_code": short_code}
    else:
        return None

def download_IG(short_code):
    loader = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(loader.context, short_code)
    internal_storage_download_path = ""
    global download_loc_info

    # Set the custom directory name
    custom_directory = 'Download'

    # Construct the target directory path
    if platform == 'android':
        internal_storage_download_path = os.path.join('/storage/emulated/0', custom_directory)
    elif platform == 'win':
        home_dir = str(Path.home())
        download_dir = os.path.join(home_dir, 'Downloads')

        if os.path.exists(download_dir):
            internal_storage_download_path = download_dir
        else:
            raise Exception('Failed to find download folder')
    elif platform == 'ios':
        # ios platform dir implementation
        pass
    elif platform == 'linux':
        # linux platform dir implementation
        pass
    elif platform == 'macosx':
        # mac os platform dir implementation
        pass

    # Create the custom directory if it doesn't exist
    os.makedirs(internal_storage_download_path, exist_ok=True)

    if post.is_video:
        video_url = post.video_url
        response = requests.get(video_url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        chunk_size = 1024
        bytes_downloaded = 0

        # Set the download path in the custom directory
        download_path = os.path.join(internal_storage_download_path, f"{post.owner_username}_{post.shortcode}.mp4")

        with open(download_path, 'wb') as f:
            for data in response.iter_content(chunk_size=chunk_size):
                f.write(data)
                bytes_downloaded += len(data)
                progress = (bytes_downloaded / total_size) * 1
                download_progress.value = progress
                progress_percent.value = f"{round(progress * 100)} %"
                download_progress.update()
                progress_percent.update()

        download_loc_info = f"Video disimpan dalam direktori {download_path}"
        popup_success()
    else:
        # Set the download path in the custom directory
        download_path = os.path.join(internal_storage_download_path, f"{post.owner_username}_{post.shortcode}")

        loader.download_post(post, target=download_path)

def download_instagram(e):
    parsed_code = parse_link(txt_number.value)

    if parsed_code:
        download_IG(parsed_code["short_code"])
    else:
        popup_err_link(txt_number.value)

# POPUP =======================================================================================================================
def popup_success():
    success_pop.open = True
    success_pop.content = ft.Text(download_loc_info)
    success_pop.update()

def popup_err_link(input_value):
    invalid_link_banner.content = ft.Text(f"WARNING! {input_value} is not a valid instagram link. Please provide a valid instagram link.", color=ft.colors.BLACK)
    invalid_link_banner.open = True
    invalid_link_banner.update()

# MAIN FUNCTION ===============================================================================================================
InstaDownloader = ft.Container(
    content=ft.Column(
        [
            invalid_link_banner,
            success_pop,
            ft.Divider(height=50, opacity=0),
            ft.Row(
                [
                    ft.Text("Fredo Instagram Downloader", size=20, text_align=ft.TextAlign.CENTER),
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
                        on_click=download_instagram
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Divider(height=20, opacity=0),
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