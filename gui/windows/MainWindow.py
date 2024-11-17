import customtkinter
from gui import AbstractWindow
from gui.language_dicts import pl, en


LANGUAGES = {
    'pl': pl,
    'en': en
}

class MainWindow(AbstractWindow):
    
    def __init__(self, master, language):
        super(AbstractWindow, self).__init__(master)
        self.current_language = LANGUAGES[language]
        self.init()
        self.refresh_text(self.current_language)

    
    def init(self):
        self.welcome_message = customtkinter.CTkLabel(self, width=250)
        self.welcome_message.pack(anchor='center')
        self.show()
    
    def refresh_text(self, language:dict):
        self.current_language = language
        self.welcome_message.configure(text=self.current_language['home_screen_text'])
    
    def show(self):
        self.grid(row=0, column=1, padx=(20, 20), pady=(20,20), sticky="nsew")
    
    def hide(self):
        self.grid_forget()
