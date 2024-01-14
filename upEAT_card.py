import tkinter as tk
from tkinter import messagebox,filedialog
from PIL import Image,ImageTk

class upeatCardWindow(tk.Toplevel):
    def __init__(self,master,path):
        self.master=master
        super().__init__(self.master)
        self.title("My upEAT Card")
        self.path = path
        self.configure(bg='#D2E9E9')
        self.geometry("600x437")
        self.card_img = None  # Initialize as None
        self.focus()
        self.create_content()
        
        

    def create_content(self):

        
        back_btn=tk.Button(self,text="Back",command=lambda: self.backBtn())
        try:
            self.card = Image.open(self.path)
        except IOError as e:
            self.path = "./profpic/user-profile.jpg"
            self.card = Image.open(self.path)
        
       


        self.edit_picture = self.card
        self.edit_picture = self.edit_picture.resize((600,400))
        self.edit_pic = ImageTk.PhotoImage(self.edit_picture)  
        
        edit_pic_label = tk.Label(self,image=self.edit_pic)
        edit_pic_label.image = self.edit_pic
     
        edit_pic_label.grid(column=0,row=0,rowspan=10,columnspan=2)
        save_card_btn=tk.Button(self,text="Save upEAT Card",command=lambda: self.saveimgBtn(self.card))
        
        save_card_btn.grid(column=1,row=11,pady=3)
        back_btn.grid(column=0,row=11,pady=3)
        return
        

    def saveimgBtn(self,cardimg):
        defname="my_upEAT_card.png"
        file_path=filedialog.asksaveasfilename(title="Save your upEAT card",initialfile=defname,defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            cardimg.save(file_path)
            self.destroy()
            messagebox.showinfo("Image Saved","Your image saved successfully")

        
        return

    def backBtn(self):
        self.destroy()
        return
            