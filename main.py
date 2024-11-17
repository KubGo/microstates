import tkinter
import tkinter.messagebox
import customtkinter

from gui import MainWindow, AbstractWindow, SideBar
from gui.language_dicts import pl, en, LanguageHandler

LANGUAGES = {
    'en': en,
    'pl': pl
}

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        
        # Language dict and handler
        self.active_language = LANGUAGES['en']
        self.language_handler = LanguageHandler()
        
        # Initialize main window
        self.init()


    def init(self):
        """Initialize main window of the app
        
        """
        # configure window
        self.title("Mikrostany")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.side_bar = SideBar(self, 'en')
        self.language_handler.register(self.side_bar)
        
        # home screen message
        self.main_window = MainWindow(self, 'en')
        self.language_handler.register(self.main_window)
        
        
    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change appearance mode for one of ['Light', 'Dark', 'System']
        
        Args:
            new_appearance_mode (str): appearance mode to set
        """
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    
    def refresh_text(self, lang: str):
        """Refresh texts to selected language

        Args:
            lang (str): Language to set
        """
        self.language_handler.refresh_text(lang)
        self.active_language = LANGUAGES[lang]
        self.appearance_mode_label.configure(text=f"{self.active_language['appearance mode']}")
        self.language_label.configure(text=f"{self.active_language['language']}")
        self.clustering_tab_button.configure(text=self.active_language['clustering_btn'])
        self.reports_tab_button.configure(text=self.active_language['reports_btn'])

if __name__ == "__main__":
    app = App()
    app.mainloop()
