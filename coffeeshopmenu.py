import tkinter as tk
from tkinter import ttk
import sqlite3
from navigator import Navigator

class CoffeShopMenuFrame(tk.Frame):
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
        coffeeMenu = tk.Frame(self,bg=color1, padx=40)
        drinksMenu = tk.Frame(self,bg=color1, padx=40)
        handmadesnacksMenu = tk.Frame(self,bg=color1, padx=40)
        packagedsnacksMenu = tk.Frame(self,bg=color1, padx=40)

        conn=sqlite3.connect("upEAT_1.sqlite")

        shops_data=conn.execute("SELECT name,locationID\
                                FROM GENERAL\
                                WHERE type='Coffee'").fetchall()
        shops=[]

        conn.close()
        for i in range(len(shops_data)):
            shops.append(shops_data[i][0])
        
        
        
        select_shop=ttk.Combobox(self,width=17,values=shops)
        select_shop.insert(0,shops_data[0][0])
        select_shop.grid(column=0,row=0,columnspan=3)
        
        coffeeMenu.grid(column=0, row=1)
        drinksMenu.grid(column=0, row=2)
        handmadesnacksMenu.grid(column=1, row=1)
        packagedsnacksMenu.grid(column=1, row=2)
        
        coffee_label = tk.Label(coffeeMenu, text = "Coffees",bg='#D2E9E9',fg='black',font=40)
        drinks_label = tk.Label(drinksMenu, text = "Other Drinks",bg='#D2E9E9',fg='black',font=40)
        handmadesnacks_label = tk.Label(handmadesnacksMenu, text = "Handmade Snacks",bg='#D2E9E9',fg='black',font=40)
        packagedsnacks_label = tk.Label(packagedsnacksMenu, text = "Packaged Snacks",bg='#D2E9E9',fg='black',font=40)

        coffee_label.grid(column=0, row=0)
        drinks_label.grid(column=0, row=0)
        handmadesnacks_label.grid(column=0, row=0)
        packagedsnacks_label.grid(column=0, row=0)

        if(self.counter==0):
            self.fill_shed(coffeeMenu,drinksMenu,handmadesnacksMenu,packagedsnacksMenu,select_shop.get())
            

        select_shop.bind("<<ComboboxSelected>>",lambda event: self.fill_shed(coffeeMenu,drinksMenu,handmadesnacksMenu,packagedsnacksMenu,select_shop.get()))

        
        
        
        back_btn=tk.Button(self,text="Back" ,font=('Calibri', 13, 'bold'), height=2, width =5,\
            command=lambda: self.back(self.username))
        back_btn.grid(column = 0, row = 3,columnspan=3)
        

    def fill_shed(self,coffeeMenu,drinksMenu,handmadesnacksMenu,packagedsnacksMenu,shopname):
        self.counter=self.counter+1
        conn=sqlite3.connect("upEAT_1.sqlite")
        shopiddata=conn.execute("SELECT locationID\
                              FROM GENERAL\
                              WHERE name=?",(shopname,)).fetchall()
        locationID=shopiddata[0][0]
        coffees_data=conn.execute("SELECT F.itemName,O.price\
                                        FROM OFFERS_ITEM AS O,FOOD_ITEM AS F\
                                        WHERE O.locationID=? AND O.itemCode=F.itemCode AND O.itemCode IN (SELECT itemCode\
									                                        FROM BELONGS_CAT\
									                                        WHERE categoryName=?)",(locationID,"Coffee",)).fetchall()
        
        drinks_data=conn.execute("SELECT F.itemName,O.price\
                                        FROM OFFERS_ITEM AS O,FOOD_ITEM AS F\
                                        WHERE O.locationID=? AND O.itemCode=F.itemCode AND O.itemCode IN (SELECT itemCode\
									                                        FROM BELONGS_CAT\
									                                        WHERE categoryName IN (?, ?, ?, ?, ?, ?))",(locationID,"Water","Tea","Beverage","Juice","Soft Drink","Energy Drink",)).fetchall()
        
        handmadesnacks_data=conn.execute("SELECT F.itemName,O.price\
                                        FROM OFFERS_ITEM AS O,FOOD_ITEM AS F\
                                        WHERE O.locationID=? AND O.itemCode=F.itemCode AND O.itemCode IN (SELECT itemCode\
									                                        FROM BELONGS_CAT\
									                                        WHERE categoryName=?)",(locationID,"Snacks-Homemade",)).fetchall()
        packagedsnacks_data=conn.execute("SELECT F.itemName,O.price\
                                        FROM OFFERS_ITEM AS O,FOOD_ITEM AS F\
                                        WHERE O.locationID=? AND O.itemCode=F.itemCode AND O.itemCode IN (SELECT itemCode\
									                                        FROM BELONGS_CAT\
									                                        WHERE categoryName=?)",(locationID,"Snacks-Packaged",)).fetchall()
   
        self.locationID=locationID
        coffees = ()
        drinks = ()
        handmadesnacks=()
        packagedsnacks=()

        for j in range(len(coffees_data)):
            coffees += (coffees_data[j][0]+ '| Price: '+ str(coffees_data[j][1])+'€',)\
                    + ('--------------------------------------------------------------------------------------------',)
            
        for j in range(len(drinks_data)):
            drinks += (drinks_data[j][0]+ '| Price: '+ str(drinks_data[j][1])+'€',)\
                    + ('--------------------------------------------------------------------------------------------',)
        
        for j in range(len(handmadesnacks_data)):
            handmadesnacks += (handmadesnacks_data[j][0]+ '| Price: '+ str(handmadesnacks_data[j][1])+'€',)\
                    + ('--------------------------------------------------------------------------------------------',)
            
        for j in range(len(packagedsnacks_data)):
            packagedsnacks += (packagedsnacks_data[j][0]+ '| Price: '+ str(packagedsnacks_data[j][1])+'€',)\
                    + ('--------------------------------------------------------------------------------------------',)

        
        coffees_var = tk.Variable(value=coffees)
        drinks_var = tk.Variable(value=drinks)
        handmadesnacks_var=tk.Variable(value=handmadesnacks)
        packagedsnacks_var=tk.Variable(value=packagedsnacks)
        
        coffees_listbox = tk.Listbox(
            coffeeMenu,
            listvariable=coffees_var,
            height=12,
            width=80,
            selectmode=tk.EXTENDED
        )

        drinks_listbox=tk.Listbox(
            drinksMenu,
            listvariable=drinks_var,
            height=12,
            width=80,
            selectmode=tk.EXTENDED
        )

        handmadesnacks_listbox=tk.Listbox(
            handmadesnacksMenu,
            listvariable=handmadesnacks_var,
            height=12,
            width=80,
            selectmode=tk.EXTENDED
        )

        packagedsnacks_listbox=tk.Listbox(
            packagedsnacksMenu,
            listvariable=packagedsnacks_var,
            height=12,
            width=80,
            selectmode=tk.EXTENDED
        )
        

        coffees_listbox.grid(row=1,column=0)
        drinks_listbox.grid(row=1,column=0)
        handmadesnacks_listbox.grid(row=1,column=0)
        packagedsnacks_listbox.grid(row=1,column=0)

        coffees_listbox.bind("<<ListboxSelect>>", self.callback)
        drinks_listbox.bind("<<ListboxSelect>>", self.callback)
        handmadesnacks_listbox.bind("<<ListboxSelect>>", self.callback)
        packagedsnacks_listbox.bind("<<ListboxSelect>>", self.callback)


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
            
