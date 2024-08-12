import flet as ft

UnderDev = ft.Container(
    content=ft.Column(
        [
            ft.Divider(height=5, opacity=0),
            ft.Row(
                [
                    ft.Text("Under Development", size=20, text_align=ft.TextAlign.CENTER),
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
        ]
    )
)