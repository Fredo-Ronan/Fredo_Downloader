import flet as ft

YtDownloader = ft.Container(
    content=ft.Column(
        [
            ft.Divider(height=50, opacity=0),
            ft.Row(
                [
                    ft.Text("Comming Soon", size=20, text_align=ft.TextAlign.CENTER, italic=True),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
        ],
    )
)