import tkinter as tk

class itemWindow(tk.Toplevel):
    def __init__(self,master,item,locationID,username):
        self.master=master
        super().__init__(self.master)
        self.title("Item Details")
        self.username=username
        self.locationID=locationID
        self.item = item
        self.configure(bg='#D2E9E9')
        self.geometry("300x437")
        self.focus()
        self.startframe=tk.Frame(self,bg='#D2E9E9')
        self.create_content()
        
        

    def create_content(self):
        from itemFrame import itemFrame
        itemframe=itemFrame(self,username=self.username,item=self.item,locationID=self.locationID)
        itemframe.grid()
        return
        
    def backBtn(self):
        self.destroy()
        return
    
    def showratings(self):
         from read_revies_page import ReadReviews
         self.startframe.destroy()
         readreviewspg=ReadReviews(self,username=self.username,item=self.item,locationID=self.locationID)
         readreviewspg.grid()
            