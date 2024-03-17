import flet as ft

from pytube import YouTube
from pytube.cli import on_progress
# from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import time
from sys import platform
import os
import shutil
from pathlib import Path

# GLOBAL VARIABLES ============================================================================================================
txt_number = ft.TextField(hint_text='Enter youtube link here...', text_align=ft.TextAlign.LEFT)
download_progress = ft.ProgressBar(width=400)
progress_percent = ft.Text("Progress : 0 %")
download_speed = ft.Text("Speed : 0 Kb/s")
download_progress.opacity = 0
download_loc_info = ""
start_download_time = None

download_infos = ft.Markdown(
    """
    NOTE! That the progress and the speed shown on the screen is not in real time, it's update every certain time and it depends on the speed of your internet connection
    """,
    selectable=True,
    extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
    code_theme="atom-one-dark",
    code_style=ft.TextStyle(font_family="Roboto Mono"),
    width=400
)

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

def progress_bar_on():
    download_progress.opacity = 1
    download_progress.update()

def progress_bar_off():
    download_progress.opacity = 0
    download_progress.update()

def clear_all_info(e):
    progress_percent.value = "0 %"
    download_progress.value = 0
    download_speed.value = "Speed : 0 Kb/s"
    global download_loc_info
    txt_number.value = ""
    download_infos.value = """
    NOTE! That the progress and the speed shown on the screen is not in real time, it's update every certain time and it depends on the speed of your internet connection
    """

    download_loc_info = ""
    
    txt_number.update()
    download_speed.update()
    progress_percent.update()
    download_progress.update()
    success_pop.open = False
    success_pop.update()
    download_infos.update()


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
    title=ft.Text("Download Completed! ✅"),
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
    global infos
    try:
        loading_on()
        youtube = YouTube(url=link, on_progress_callback=on_progress)
        # get the highest resolution stream
        video_stream = youtube.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
        audio_stream = youtube.streams.filter(only_audio=True).first()
        video_title = youtube.title + ".mp4"
        global download_loc_info

        # Set the custom directory name
        custom_directory = 'Download'

        # Construct the target directory path
        if platform == 'linux':
            download_dir = os.path.join('/storage/emulated/0', custom_directory)
            temp_dir = os.path.join(download_dir, "temp")
            os.makedirs(temp_dir, exist_ok=True)
        elif platform == 'win32':
            home_dir = str(Path.home())
            download_dir = os.path.join(home_dir, 'Downloads')

            if os.path.exists(download_dir):
                temp_dir = os.path.join(download_dir, "temp")
                os.makedirs(temp_dir, exist_ok=True)
            else:
                raise Exception('Failed to find download folder')
        elif platform == 'darwin':
            # mac os platform dir implementation
            pass

        loading_off()
        progress_bar_on()

        audio_file_size = audio_stream.filesize / 1000000
        video_file_size = video_stream.filesize / 1000000

        # video_stream.download(output_path=internal_storage_download_path, filename=video_title)
        download_infos.value = f"""
    NOTE! That the progress and the speed shown on the screen is not in real time, it's update every certain time and it depends on the speed of your internet connection
    -------------------------------------------------------------
    Downloading Audio...
    [Audio file size => {audio_file_size:.2f} Mb]
        """
        download_infos.update()

        audio_file = audio_stream.download(output_path=temp_dir, filename='audio')

        download_infos.value = f"""
    NOTE! That the progress and the speed shown on the screen is not in real time, it's update every certain time and it depends on the speed of your internet connection
    -------------------------------------------------------------
    Audio Downloaded
    [Audio file size => {audio_file_size:.2f} Mb] | done ✅
    -------------------------------------------------------------
    Downloading Video...
    [Video file size => {video_file_size:.2f} Mb]
        """
        download_infos.update()

        video_file = video_stream.download(output_path=temp_dir, filename='video')

        # Create video clip objects
        video_clip = VideoFileClip(video_file)
        # Explicitly set the FPS for audio file
        audio_clip = AudioFileClip(audio_file)

        download_infos.value = f"""
    NOTE! That the progress and the speed shown on the screen is not in real time, it's update every certain time and it depends on the speed of your internet connection
    -------------------------------------------------------------
    Audio Downloaded
    [Audio file size => {audio_file_size:.2f} Mb] | done ✅
    -------------------------------------------------------------
    Video Downloaded
    [Video file size => {video_file_size:.2f} Mb] | done ✅
    -------------------------------------------------------------
    Merging Audio and Video on progress....
    
    * this process will utilize much of raw CPU power, so don't worry if your laptop fan or CPU load is suddenly high, it only because of this process
        """
        download_infos.update()

        # Combine audio and video
        final_clip = video_clip.set_audio(audio_clip)

        final_video_path = os.path.join(download_dir, f"{video_title}")

        # Export the final clip
        final_clip.write_videofile(final_video_path, codec='libx264', temp_audiofile=os.path.join(temp_dir, "temp_audio.mp3"))

        # Cleanup
        final_clip.close()
        video_clip.close()
        audio_clip.close()

        download_infos.value = f"""
    NOTE! That the progress and the speed shown on the screen is not in real time, it's update every certain time and it depends on the speed of your internet connection
    -------------------------------------------------------------
    Downloading Audio...
    [Audio file size => {audio_file_size:.2f} Mb] | done ✅
    -------------------------------------------------------------
    Downloading Video...
    [Video file size => {video_file_size:.2f} Mb] | done ✅
    -------------------------------------------------------------
    Merging Audio and Video | done ✅
    -------------------------------------------------------------
    Deleting temp folder....
        """
        download_infos.update()

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print("delete temp dir successfully")
        
        download_infos.value = f"""
    NOTE! That the progress and the speed shown on the screen is not in real time, it's update every certain time and it depends on the speed of your internet connection
    -------------------------------------------------------------
    Downloading Audio...
    [Audio file size => {audio_file_size:.2f} Mb] | done ✅
    -------------------------------------------------------------
    Downloading Video...
    [Video file size => {video_file_size:.2f} Mb] | done ✅
    -------------------------------------------------------------
    Merging Audio and Video | done ✅
    -------------------------------------------------------------
    Deleting temp folder | done ✅
    -------------------------------------------------------------
    Success ✅
        """
        download_infos.update()

        download_loc_info = f"Video disimpan dalam direktori {final_video_path}"
        progress_bar_off()
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
    # download_progress.value = int(download_percentage)
    download_speed.value = download_speed_value
    progress_percent.value = f"Progress: {int(download_percentage)} %"

    # download_progress.update()
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
            ft.Row(
                [
                    download_infos,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        ],
    )
)