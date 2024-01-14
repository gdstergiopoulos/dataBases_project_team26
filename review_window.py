import tkinter as tk
from tkinter import messagebox,ttk
import sqlite3
import datetime

class reviewWindow(tk.Toplevel):
    def __init__(self,master,item,locationID,username):
        self.master=master
        super().__init__(self.master)
        self.title("Leave Review")
        self.username=username
        self.locationID=locationID
        self.item = item
        self.configure(bg='#D2E9E9')
        self.geometry("300x437")
        self.focus()
        self.create_content()
        
        

    def create_content(self):
        conn=sqlite3.connect("upEAT_1.sqlite")
        cursor=conn.execute("SELECT itemName\
                            FROM FOOD_ITEM\
                            WHERE itemCode=?",(self.item,)).fetchall()
        conn.close()
        review_label = tk.Label(self, text="Leave a Review for: " + str(cursor[0][0]),bg='#D2E9E9',fg='black',font=30)
        stars_label = tk.Label(self, text="Rate the food out of 5",bg='#D2E9E9',fg='black',font=30)
        txt_label = tk.Label(self, text="Describe your experience",bg='#D2E9E9',fg='black',font=30)
    
        review_stars=ttk.Combobox(self,values=[0.5,1,1.5,2,2.5,3,3.5,4,4.5,5], state='readonly')
        review_txt = tk.Entry(self)
        review_button = tk.Button(self,text="Review",command=lambda: self.review(review_stars.get(), review_txt.get()))
        back_btn = tk.Button(self,text="Cancel",command=lambda: self.backBtn())
        review_label.grid(column=0, row=0)
        stars_label.grid(column=0, row=1)
        review_stars.grid(column=0, row=2)
        txt_label.grid(column=0, row=3)
        review_txt.grid(column=0, row=4)
        review_button.grid(column=0, row=5)
        back_btn.grid(column=1, row=5)
        return
        
    def backBtn(self):
        self.destroy()
        return
    
    def review(self, stars, review):
        stars = float(stars)
        conn=sqlite3.connect("upEAT_1.sqlite")
        SSN = conn.execute("SELECT SSN FROM ACCOUNT WHERE username = ?", (self.username,)).fetchall()
        review_exists = conn.execute("SELECT COUNT(*) FROM REVIEWS WHERE SSN=? AND itemCode=? AND locationID=?"\
                , (SSN[0][0],self.item, self.locationID,)).fetchone()[0]
        if review_exists:
            messagebox.showerror("Couldn't Review","Already reviewed this item")
            self.destroy()
            conn.close()
        
        elif 0>stars or stars>5:
            messagebox.showerror("Couldn't Review","Invalid rating range")
            
        else:
            # print("we're here")
            conn.execute("INSERT INTO REVIEWS(stars, review, SSN, itemCode, locationID,date)\
                                        VALUES(?,?,?,?,?,?)", (stars, review, \
                                            SSN[0][0], self.item, self.locationID,datetime.date.today(),))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thank you","Your Review was Submitted")
            self.destroy()
            