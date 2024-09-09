import flet as ft


class Cashola(ft.Column):
    def __init__(self):
        super().__init__()
        self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        # self.views = ft.Column()

        def handle_dismissal(e):
            self.add(ft.Text("Drawer Dismissed"))

        def handle_change(e):
            self.add(ft.Text("Drawer Opened"))

        self.drawer = ft.NavigationDrawer(
            on_dismiss=handle_dismissal,
            on_change=handle_change,
            controls=[
                ft.Container(height=12),
                ft.NavigationDrawerDestination(
                    label="Home",
                    icon=ft.icons.HOME,
                    selected_icon_content=ft.Icon(ft.icons.HOME),
                ),
            ],
        )

        self.add(
            ft.ElevatedButton("Show Drawer", on_click=lambda e: self.open(self.drawer))
        )


# def main(page: ft.Page):
#     page.window_width = 500  # window's width is 200 px
#     page.window_height = 500  # window's height is 200 px
#     # page.window_resizable = False  # window is not resizable
#     page.title = "Cashola"

#     base_page = Cashola()
#     page.add(base_page)
#     page.update()


# ft.app(main)


def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # def handle_dismissal(e):
    #     page.add(ft.Text("Drawer dismissed"))

    def handle_change(e):
        page.add(ft.Text(f"Selected Index changed: {e.selected_index}"))
        # page.close(drawer)

    drawer = ft.NavigationDrawer(
        # on_dismiss=handle_dismissal,
        on_change=handle_change,
        controls=[
            ft.Container(height=12),
            ft.NavigationDrawerDestination(
                label="Item 1",
                icon=ft.icons.DOOR_BACK_DOOR_OUTLINED,
                selected_icon_content=ft.Icon(ft.icons.DOOR_BACK_DOOR),
            ),
            ft.Divider(thickness=2),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.MAIL_OUTLINED),
                label="Item 2",
                selected_icon=ft.icons.MAIL,
            ),
            ft.NavigationDrawerDestination(
                icon_content=ft.Icon(ft.icons.PHONE_OUTLINED),
                label="Item 3",
                selected_icon=ft.icons.PHONE,
            ),
        ],
    )

    page.add(ft.ElevatedButton("Show drawer", on_click=lambda e: page.open(drawer)))


ft.app(main)
