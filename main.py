import tkinter
import tkinter.messagebox
import customtkinter

from gui import MainWindow, AbstractWindow
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
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Mikrostates", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Tabs navigation
        self.clustering_tab_button = customtkinter.CTkButton(self.sidebar_frame)
        self.clustering_tab_button.grid(row=1, column=0, padx=20, pady=10)
        self.reports_tab_button = customtkinter.CTkButton(self.sidebar_frame, command=self.set_window)
        self.reports_tab_button.grid(row=2, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, anchor="w")
        # App settings
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.language_label = customtkinter.CTkLabel(master=self.sidebar_frame, anchor="w")
        self.language_label.grid(row=7, column=0, padx=20, pady=(10,0))
        self.language_selector = customtkinter.CTkSegmentedButton(master=self.sidebar_frame, values=["pl", "en"], command=self.refresh_text)
        self.language_selector.grid(row=8, column=0, padx=20, pady=(5,20))
        
        # Home screen message
        self.main_window = MainWindow(self, 'en')
        self.language_handler.register(self.main_window)
        
        # set default values
        self.appearance_mode_optionemenu.set("System")
        self.language_selector.set('en')
        self.refresh_text('en')
        
        
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
