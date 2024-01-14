import tkinter as tk
from tkinter import ttk
import sqlite3
from navigator import Navigator

class RestaurantMenuFrame(tk.Frame):
    def __init__(self,master,username,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.username=username
        self.master=master
        self.navigator=Navigator(self,master,username=self.username)
        self.master.geometry("1200x600")
        self.pack(side='left')
        self.counter=0
        self.create_content()
        self.path=""
    
    

    def create_content(self):
        #labels
        color1 = '#D2E9E9'
        color2 = '#D2E9E9'
        appetMenu = tk.Frame(self,bg=color1, padx=40)
        mainMenu = tk.Frame(self,bg=color1, padx=40)
        dessertMenu = tk.Frame(self,bg=color1, padx=40)
        otherMenu = tk.Frame(self,bg=color1, padx=40)

        conn=sqlite3.connect("upEAT_1.sqlite")

        shops_data=conn.execute("SELECT name,locationID\
                                FROM GENERAL\
                                WHERE type='Restaurant'").fetchall()
        shops=[]

        conn.close()
        for i in range(len(shops_data)):
            shops.append(shops_data[i][0])
        
        select_shop=ttk.Combobox(self,width=17,values=shops)
        select_shop.insert(0,shops_data[0][0])
        select_shop.grid(column=0,row=0,columnspan=3)
        
        appetMenu.grid(column=0, row=1)
        mainMenu.grid(column=0, row=2)
        dessertMenu.grid(column=1, row=1)
        otherMenu.grid(column=1, row=2)
        
        appet_label = tk.Label(appetMenu, text = "Appetizers",bg='#D2E9E9',fg='black',font=40)
        main_label = tk.Label(mainMenu, text = "Main Course",bg='#D2E9E9',fg='black',font=40)
        dessert_label = tk.Label(dessertMenu, text = "Desserts",bg='#D2E9E9',fg='black',font=40)
        other_label = tk.Label(otherMenu, text = "Others",bg='#D2E9E9',fg='black',font=40)

        appet_label.grid(column=0, row=0)
        main_label.grid(column=0, row=0)
        dessert_label.grid(column=0, row=0)
        other_label.grid(column=0, row=0)

        if(self.counter==0):
            self.fill_shed(appetMenu,mainMenu,dessertMenu,otherMenu,select_shop.get())

        select_shop.bind("<<ComboboxSelected>>",lambda event: self.fill_shed(appetMenu,mainMenu,dessertMenu,otherMenu,select_shop.get()))

        
        
        
        back_btn=tk.Button(self,text="Back" ,font=('Calibri', 13, 'bold'), height=2, width =5,\
            command=lambda: self.back(self.username))
        back_btn.grid(column = 0, row = 3,columnspan=3)
       

    def fill_shed(self,appetMenu,mainMenu,dessertMenu,otherMenu,shopname):
        self.counter=self.counter+1
        conn=sqlite3.connect("upEAT_1.sqlite")
        shopiddata=conn.execute("SELECT locationID\
                              FROM GENERAL\
                              WHERE name=?",(shopname,)).fetchall()
        locationID=shopiddata[0][0]
        appetizer_data=conn.execute("SELECT F.itemName,O.price\
                                        FROM OFFERS_ITEM as O,FOOD_ITEM AS F\
                                        WHERE F.itemCode=O.itemCode AND O.locationID=? AND O.mealtype =?",(locationID,"Appetizer",)).fetchall()
        
        main_data=conn.execute("SELECT F.itemName,O.price\
                                        FROM OFFERS_ITEM as O,FOOD_ITEM AS F\
                                        WHERE F.itemCode=O.itemCode AND O.locationID=? AND O.mealtype =?",(locationID,"Main Course",)).fetchall()
        
        dessert_data=conn.execute("SELECT F.itemName,O.price\
                                        FROM OFFERS_ITEM as O,FOOD_ITEM AS F\
                                        WHERE F.itemCode=O.itemCode AND O.locationID=? AND O.mealtype =?",(locationID,"Dessert",)).fetchall()
        other_data=conn.execute("SELECT F.itemName,O.price\
                                        FROM OFFERS_ITEM as O,FOOD_ITEM AS F\
                                        WHERE F.itemCode=O.itemCode AND O.locationID=? AND O.mealtype =?",(locationID,"Other",)).fetchall()
        
       
        self.locationID = locationID
        appetizers = ()
        main = ()
        dessert=()
        other=()

        for j in range(len(appetizer_data)):
            appetizers += (appetizer_data[j][0]+ '| Price: '+ str(appetizer_data[j][1])+'€',)\
                    + ('--------------------------------------------------------------------------------------------',)
            
        for j in range(len(main_data)):
            main += (main_data[j][0]+ '| Price: '+ str(main_data[j][1])+'€',)\
                    + ('--------------------------------------------------------------------------------------------',)
        
        for j in range(len(dessert_data)):
            dessert += (dessert_data[j][0]+ '| Price: '+ str(dessert_data[j][1])+'€',)\
                    + ('--------------------------------------------------------------------------------------------',)
            
        for j in range(len(other_data)):
            other += (other_data[j][0]+ '| Price: '+ str(other_data[j][1])+'€',)\
                    + ('--------------------------------------------------------------------------------------------',)

        
        appetizers_var = tk.Variable(value=appetizers)
        main_var = tk.Variable(value=main)
        dessert_var=tk.Variable(value=dessert)
        other_var=tk.Variable(value=other)
        
        appetizers_listbox = tk.Listbox(
            appetMenu,
            listvariable=appetizers_var,
            height=12,
            width=80,
            selectmode=tk.EXTENDED
        )

        main_listbox=tk.Listbox(
            mainMenu,
            listvariable=main_var,
            height=12,
            width=80,
            selectmode=tk.EXTENDED
        )

        dessert_listbox=tk.Listbox(
            dessertMenu,
            listvariable=dessert_var,
            height=12,
            width=80,
            selectmode=tk.EXTENDED
        )

        other_listbox=tk.Listbox(
            otherMenu,
            listvariable=other_var,
            height=12,
            width=80,
            selectmode=tk.EXTENDED
        )
        

        appetizers_listbox.grid(row=1,column=0)
        main_listbox.grid(row=1,column=0)
        dessert_listbox.grid(row=1,column=0)
        other_listbox.grid(row=1,column=0)

        appetizers_listbox.bind("<<ListboxSelect>>", self.callback)
        main_listbox.bind("<<ListboxSelect>>", self.callback)
        dessert_listbox.bind("<<ListboxSelect>>", self.callback)
        other_listbox.bind("<<ListboxSelect>>", self.callback)


    def back(self,username):
        from home_page import WelcomeFrame
        self.destroy()
        purchase_frame=WelcomeFrame(self.master, username=username)
        purchase_frame.pack()

    def callback(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            parts=data.split('|')
            conn=sqlite3.connect("upEAT_1.sqlite")
            cursor=conn.execute("SELECT itemCode\
                                FROM FOOD_ITEM\
                                WHERE itemName=? AND locationID=?",(parts[0].strip(),self.locationID,)).fetchall()
            itemcode=cursor[0][0]
            conn.close()
            from item_window import itemWindow
            item_window=itemWindow(self,item=itemcode,locationID=self.locationID,username=self.username)
            return
        else:
            print("nothing")
            
