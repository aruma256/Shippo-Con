from typing import TYPE_CHECKING

import flet as ft

from .const import APP_NAME, VERSION
from .core import Core
from .license_text_generator import get_license_text


if TYPE_CHECKING:
    from flet_core.control_event import ControlEvent


WINDOW_WIDTH = 600


async def _show_oss_license(event: 'ControlEvent') -> None:
    dialog = ft.AlertDialog(
        title=ft.Text("OSSライセンス"),
        content=ft.Column([ft.Text(get_license_text())], scroll="always"),
    )
    event.page.dialog = dialog
    dialog.open = True
    await event.page.update_async()


async def main(page: ft.Page) -> None:
    app_title = f"{APP_NAME} - {VERSION}"
    page.title = app_title
    page.window_width = WINDOW_WIDTH

    core = Core()

    async def connect_L_clicked() -> None:
        await core.connect_L()

    async def connect_R_clicked() -> None:
        await core.connect_R()

    appbar = ft.AppBar(
        title=ft.Text(app_title),
        bgcolor=ft.colors.SURFACE_VARIANT,
        actions=[ft.PopupMenuButton(items=[
            # ft.PopupMenuItem(
            #     text="ライセンスをブラウザで表示",
            #     on_click=lambda _: page.launch_url(LICENSE_LINK),
            # ),
            ft.PopupMenuItem(
                text="OSSライセンス",
                on_click=_show_oss_license,
            ),
        ])],
    )
    connect_L_button = ft.ElevatedButton(
        text="Joy-Con L を接続",
        on_click=connect_L_clicked,
    )
    connect_R_button = ft.ElevatedButton(
        text="Joy-Con R を接続",
        on_click=connect_R_clicked,
    )
    await page.add_async(
        appbar,
        connect_L_button,
        connect_R_button,
    )


ft.app(main)
