from gui.windows.AbstractWindow import AbstractWindow
import customtkinter

class ClusteringWindow(AbstractWindow):
    
    def __init__(self, master, language):
        super(AbstractWindow, self).__init__(master)
        self.init()
        
    def init(self):
        clustering_info = customtkinter.CTkLabel(self, text="Clustering window")
        clustering_info.grid(row=0, column=0, columnspan=3)
    
    def refresh_text(self, language):
        pass
    
    def show(self):
        self.grid(row=0, column=1, padx=(20, 20), pady=(20,20), sticky="nsew")
    
    def hide(self):
        self.grid_forget()
