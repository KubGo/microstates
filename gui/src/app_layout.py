from flet import (
    Page,
    Row,
    Text,
    icons,
    colors,
    IconButton,
)

from sidebar import SideBar

class AppLayout(Row):
    def __init__(
        self, 
        #app,
        page: Page,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        # self.app = app
        self.page = page
        self.toggle_nav_bar = IconButton(
            icon=icons.ARROW_CIRCLE_LEFT,
            icon_color=colors.BLUE_GREY_300,
            selected=False,
            selected_icon=icons.ARROW_CIRCLE_RIGHT,
            on_click=self.toggle_nav_rail)
        self.sidebar = SideBar(page)
        self.controls = [
            self.sidebar,
            self.toggle_nav_bar,
            Text("Dupa"),
            Text("Też dupa")
        ]
        self.expand= True
        
    def toggle_nav_rail(self, e):
        self.sidebar.visible = not self.sidebar.visible
        self.toggle_nav_bar.selected = not self.toggle_nav_bar.selected
        self.page.update()