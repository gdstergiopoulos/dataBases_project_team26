import tkinter as tk
from navigator import Navigator

class InfoFrame(tk.Frame):
    def __init__(self, master,username,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.navigator=Navigator(self,master,username=username)
        self.master.geometry("500x500")
        self.username=username
        self.pack()
        self.create_content()

    def create_content(self):
    
        label = tk.Label(self, text="\t\tΒασεις Δεδομένων 2023-2024\n\
                                    Creators:\n\
                                    Panourgias Antonios up1083861@ac.upatras.gr   \n\
                                    Stergiopoulos Georgios up1083861@ac.upatras.gr\n",bg='#D2E9E9')
        label.grid(column=0,row=0)
        
        back_btn = tk.Button(self,text="Back",command=lambda: self.back(self.username),font=('Calibri', 13, 'bold'))
        back_btn.grid(row=3, column=0, pady=10)
        
        
    def back(self,username):
        from home_page import WelcomeFrame
        self.destroy()
        purchase_frame=WelcomeFrame(self.master, username=username)
        purchase_frame.pack()

        