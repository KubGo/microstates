from gui.windows.AbstractWindow import AbstractWindow
from gui.language_dicts import pl, en
import customtkinter

LANGUAGES = {
    'pl': pl,
    'en': en
}

class SideBar(AbstractWindow):
    """Side bar for the application
    """
    
    def __init__(self, master, language):
        super(AbstractWindow, self).__init__(master, width=140, corner_radius=0)
        self.current_language = LANGUAGES[language]
        self.init()
        self.refresh_text(self.current_language)
        
    def init(self):
        self.logo_label = customtkinter.CTkLabel(self, font=customtkinter.CTkFont(size=20, weight="bold"), text="Microstates")
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        # Tabs navigation
        self.clustering_tab_button = customtkinter.CTkButton(self)
        self.clustering_tab_button.grid(row=1, column=0, padx=20, pady=10)
        self.reports_tab_button = customtkinter.CTkButton(self)
        self.reports_tab_button.grid(row=2, column=0, padx=20, pady=10)
        # App Settings
        self.appearance_mode_label = customtkinter.CTkLabel(self, anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10,0))
        self.appearance_mode_optionmenu = customtkinter.CTkOptionMenu(
            self, 
            values=['Light', "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionmenu.grid(row=6, column=0, padx=20,pady=10)
        self.appearance_mode_optionmenu.set('System')
        self.language_label = customtkinter.CTkLabel(self, anchor="w")
        self.language_label.grid(row=7, column=0, padx=20, pady=(10,0))
        self.language_selector = customtkinter.CTkSegmentedButton(
            self,
            values=['pl', 'en'], 
            command=self.global_refresh_text
        )
        self.language_selector.grid(row=8, column=0, padx=20, pady=(5, 20))
        self.change_appearance_mode_event('System')
        self.show()
        
    
    def refresh_text(self, language: dict):
        """Refresh texts for the language

        Args:
            language (dict): Language to change the texts to
        """
        self.current_language = language
        self.appearance_mode_label.configure(text=f"{self.current_language['appearance mode']}")
        self.language_label.configure(text=f"{self.current_language['language']}")
        self.clustering_tab_button.configure(text=self.current_language['clustering_btn'])
        self.reports_tab_button.configure(text=self.current_language['reports_btn'])
    
    def global_refresh_text(self, language: str):
        """Change texts for whole app

        Args:
            language (str): Language to change texts to
        """
        self.current_language = LANGUAGES[language]
        self.master.refresh_text(self.current_language)
    
    def show(self):
        """Show sidebar on the app
        """
        self.grid(row=0, column=0, rowspan=4, sticky="nsew")
    
    def hide(self):
        """To do hide app
        """
        pass
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change appearance mode for one of ['Light', 'Dark', 'System']
        
        Args:
            new_appearance_mode (str): appearance mode to set
        """
        customtkinter.set_appearance_mode(new_appearance_mode)
