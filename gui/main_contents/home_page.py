from .interfaces import AbstractMainContent
from flet import Page, alignment, Markdown, MarkdownExtensionSet

class HomePageContent(AbstractMainContent):

    def __init__(self, page: Page):
        super().__init__(page)
        self.expand = True
        self.alignment = alignment.center
        self.horizontal_alignment = alignment.center

        md_text = """
# Welcome to Microstates app!
This app is a GUI for clustering of microstates. For now, it's in its development phase and there's hardly anything that works here, but I hope that one day it will be working app, that people without any programming knowledge can use to cluster and analyze microstates.
If You want to learn more about microstates, You can use this [GitHub page](https://frederic-vw.github.io/eeg-patterns/).
        """
        self.controls = [
            Markdown(
                md_text,
                extension_set=MarkdownExtensionSet.GITHUB_WEB,
                on_tap_link=lambda e: self.page.launch_url(e.data),
                fit_content=True
            )
        ]