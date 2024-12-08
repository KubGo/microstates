from flet import (
    Page,
    FletApp,
    View
)
from main_contents.home_page import HomePageContent
from main_contents.clustering_page import ClusteringPageContent
from main_contents.reports_page import ReportsPage
from app_layout import AppLayout
from sidebar import SideBar, SideBarObserver
from main_contents.controllers.clustering_controllers import WholeSignalClusteringControler

class MicrostatesApp(SideBarObserver):
    
    def __init__(self, page: Page):
        super().__init__()
        self.page = page
        # Main views
        self.side_bar = SideBar(self.page, self)
        self.home_page = HomePageContent(self.page)
        self.clustering_page = ClusteringPageContent(self.page)
        self.reporting_page = ReportsPage(self.page)
        # Controllers
        self.current_page_number = 0
        self.clustering_controller = WholeSignalClusteringControler(self.clustering_page)
        self.pages = {
            0: self.home_page,
            1: self.clustering_page,
            2: self.reporting_page
        }

        self.currennt_page = AppLayout(self.page, self.side_bar, self.pages[self.current_page_number])
        self.page.add(self.currennt_page)
        self.page.update()

    def updateMainContent(self, window_number):
        if window_number == self.current_page_number:
            return
        self.currennt_page.body.content = self.pages[window_number]
        self.current_page_number = window_number
        self.currennt_page.update()


    
        