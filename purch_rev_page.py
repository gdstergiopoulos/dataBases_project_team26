import tkinter as tk
import sqlite3
from navigator import Navigator

class PurchRevFrame(tk.Frame):
    def __init__(self,master,username,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.username=username
        self.master=master
        self.navigator=Navigator(self,master,username=self.username)
        self.master.geometry("1200x600")
        self.pack(side='left')
        self.create_content()
        self.path=""
        
    

    def create_content(self):
        #labels
        color1 = '#D2E9E9'
        color2 = '#D2E9E9'
        purchase_history = tk.Frame(self,bg=color1, padx=40)
        review_history = tk.Frame(self,bg=color1, padx=40)
        purchase_history.grid(column=0, row=0)
        review_history.grid(column=1, row=0)
        
        purchase_label = tk.Label(purchase_history, text = "Purchase History",bg='#D2E9E9',fg='black',font=40)
        review_label = tk.Label(review_history, text = "Review History",bg='#D2E9E9',fg='black',font=40)
        
        purchase_label.grid(column=0, row=0)
        review_label.grid(column=0, row=0)
        back_btn=tk.Button(self,text="Back" ,font=('Calibri', 13, 'bold'), height=2, width =5,\
            command=lambda: self.back(self.username))
        back_btn.grid(column = 0, columnspan=2, row = 1, pady=15)
        conn=sqlite3.connect("upEAT_1.sqlite")
        #GET USERS SSN:
        SSN=conn.execute("SELECT SSN\
                                        FROM ACCOUNT\
                                        WHERE username = ?",(self.username,)).fetchall()
        purchase_data=conn.execute("SELECT P.transNo, F.itemName, P.date\
                                        FROM PURCHASES AS P,FOOD_ITEM AS F\
                                        WHERE P.SSN = ? AND F.itemCode=P.itemCode\
                                        ORDER BY P.date DESC",(SSN[0][0],)).fetchall()
        review_data=conn.execute("SELECT R.stars, R.review, F.itemName, R.locationID, R.date\
                                        FROM REVIEWS AS R, FOOD_ITEM AS F\
                                        WHERE F.itemCode=R.itemCode\
                                        AND R.SSN = ?\
                                        ORDER BY date DESC",(SSN[0][0],)).fetchall()

        conn.close()
        purchases = ()
        reviews = ()

        for k in range(len(purchase_data)):
            purchases = purchases + ('Transaction:' + purchase_data[k][0]+ ' |  Food Item: '+purchase_data[k][1]+ \
                ' | Date purchased: ' +purchase_data[k][2],) \
                    + ('--------------------------------------------------------------------------------------------',)
         
        for j in range(len(review_data)):
            reviews += ('Stars: ' + review_data[j][0]+ '/5 | Food Item: '+ review_data[j][2]+ ' | Date:' + review_data[j][4],)\
                + ('Review: '+review_data[j][1],) \
                    + ('--------------------------------------------------------------------------------------------',)

        
        reviews_var = tk.Variable(value=reviews)
        purchases_var = tk.Variable(value=purchases)
        
        review_listbox = tk.Listbox(
            review_history,
            listvariable=reviews_var,
            height=15,
            width=80,
            selectmode=tk.EXTENDED
        )
        
        purchase_listbox = tk.Listbox(
            purchase_history,
            listvariable=purchases_var,
            height=15,
            width=80,
            selectmode=tk.EXTENDED
        )
        
        review_listbox.grid(row=1,column=0)
        purchase_listbox.grid(row=1,column=0)
        purchase_listbox.bind("<<ListboxSelect>>", self.callback)

    def back(self,username):
        from profile_page import ProfileFrame
        self.destroy()
        purchase_frame=ProfileFrame(self.master, username=username)
        purchase_frame.pack()

    def callback(self,event):
        selection = event.widget.curselection()
        from review_window import reviewWindow
        
        if selection:
            conn=sqlite3.connect("upEAT_1.sqlite")
            index = selection[0]
            data = event.widget.get(index)
            parts=data.split(':')
            parts2 = parts[2].split('|')
            parts3=data.split(':')
            parts4 = parts[1].split('|')
            location =conn.execute("SELECT locationID FROM PURCHASES WHERE transNo = ?", (parts4[0].strip(),)).fetchall()
            conn.close()
            conn=sqlite3.connect("upEAT_1.sqlite")
            cursor=conn.execute("SELECT itemCode\
                                FROM FOOD_ITEM\
                                WHERE itemName=? AND locationID=?",(parts2[0].strip(),location[0][0],)).fetchall()
            itemcode=cursor[0][0]
            conn.close()
            from review_window import reviewWindow
            review_window=reviewWindow(self,item=itemcode,locationID = location[0][0],username=self.username)
            return
        else:
            print("nothing")