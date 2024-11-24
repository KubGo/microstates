from flet import (
    NavigationRail,
    NavigationRailDestination,
    Icon,
    icons,
    colors,
    padding,
    Page
)

from abc import ABC, abstractmethod

class SideBarObserver(ABC):
    def __init__(self):
        pass
    @abstractmethod
    def updateMainContent(self, window_number: int):
        pass

class SideBar(NavigationRail):
    
    def __init__(self, page: Page, app: SideBarObserver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page = page
        self.app = app
        self.selected_index=1,
        self.label_type="all",
        self.on_change=self.top_nav_change,
        self.bgcolor=colors.BLUE_GREY,
        self.extended=True,
        self.expand=True,
        
        self.elevation = 10
        self.top_nav_items = [
            
        ]
        
        self.destinations =[
                NavigationRailDestination(
                    label="Home",
                    icon=icons.HOME,
                    selected_icon_content=Icon(icons.HOME_OUTLINED),
                    padding=padding.all(5),
                    
                ),
                NavigationRailDestination(
                    label="Clustering",
                    icon=icons.GROUP_WORK,
                    selected_icon_content=Icon(icons.GROUP_WORK_OUTLINED),
                    padding=padding.all(5)
                ),
                NavigationRailDestination(
                    label="Reports",
                    icon=icons.ANALYTICS,
                    selected_icon_content=Icon(icons.ANALYTICS_OUTLINED),
                    padding=padding.all(5)
                )
            ]
        
        self.on_change= self.top_nav_change

    def top_nav_change(self, e: NavigationRailDestination):
        self.app.updateMainContent(e.control.selected_index)

