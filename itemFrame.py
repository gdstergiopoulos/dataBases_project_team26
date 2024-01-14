import tkinter as tk
import sqlite3


class itemFrame(tk.Frame):
    def __init__(self,master,username,item,locationID,*args,**kwargs):
        super().__init__(master,bg='#D2E9E9',padx=80,*args,**kwargs)
        self.username=username
        self.item=item
        self.master=master
        self.master.geometry("330x300")
        self.locationID=locationID
        self.create_content()
        self.path=""
        


    def create_content(self):
        back_btn=tk.Button(self,text="Back",command=lambda: self.backBtn())
        conn=sqlite3.connect("upEAT_1.sqlite")
        cursor=conn.execute("SELECT itemName\
                            FROM FOOD_ITEM\
                            WHERE itemCode=?",(self.item,)).fetchall()
        title_label = tk.Label(self, text=str(cursor[0][0]),bg='#D2E9E9',fg='black',font=25)
        ingredients_label = tk.Label(self, text="Ingredients:",bg='#D2E9E9',fg='black',font=25)
        allergens_label = tk.Label(self, text="Allergens:",bg='#D2E9E9',fg='black',font=25)
       
        
        cursor=conn.execute("SELECT avg(stars)\
                            FROM REVIEWS\
                            WHERE itemCode=? AND locationID=?",(self.item,self.locationID,))
        rate=cursor.fetchall()
        if(rate[0][0]==None):
             ratingtext="Rating: Not enough ratings"
        else:
             stars=round(rate[0][0],1)
             ratingtext="Rating: "+str(stars)+"/5"
             
        rating_label = tk.Label(self, text=ratingtext,bg='#D2E9E9',fg='black',font=30,cursor="hand2")
        rating_label.bind("<Button-1>",lambda event :self.showratings())
        rating_label.bind("<Enter>", lambda event: rating_label.config(bg="#A9D9D9"))
        rating_label.bind("<Leave>", lambda event: rating_label.config(bg="#D2E9E9"))

        cursor=conn.execute("SELECT B.categoryName\
                        FROM BELONGS_CAT AS B,FOOD_ITEM AS F\
                        WHERE B.itemCode = F.itemCode\
                        AND F.itemCode = ?",(self.item,))
                
        category_fetch=cursor.fetchall() 

         
        cursor=conn.execute("SELECT allergenID\
                            FROM IS_ALLERGIC\
                            WHERE SSN in (SELECT M.SSN\
                                          FROM MEMBER AS M,ACCOUNT AS A\
                                          WHERE A.SSN=M.SSN AND A.username=?)",(self.username,))
        userallergto=cursor.fetchall()

        cursor=conn.execute("SELECT allergenID\
                            FROM CONTAINS_AL\
                            WHERE itemCode=?",(self.item,))
        itemcontains=cursor.fetchall()

        user_allerg_list=[]
        

        food_cont_allerg=[]
        for k in range(len(userallergto)):
            user_allerg_list.append(userallergto[k][0])

        for k in range(len(itemcontains)):
            food_cont_allerg.append(itemcontains[k][0])

        for i in user_allerg_list:
             if i in food_cont_allerg:
                  allerg_lbl=tk.Label(self,text="WARNING!\nThis food may triger your allergy",bg='#D2E9E9',fg='red',font=12)
                  allerg_lbl.grid(column=0,row=12, sticky='w', columnspan=2)

        category_label = tk.Label(self, text=str(category_fetch[0][0]),bg='#D2E9E9',fg='black',font=30)

        cursor=conn.execute("SELECT I.foodIngredient\
                            FROM INGREDIENTS AS I,FOOD_ITEM AS F\
                            WHERE I.itemCode = F.itemCode\
                            AND I.itemCode = ?\
                            ",(self.item,))
        
        ingredients_fetch=cursor.fetchall() 
        
        
        ingredients = ()
        

        for k in range(len(ingredients_fetch)):
                ingredients = ingredients + (ingredients_fetch[k][0], )

        curr=conn.execute("SELECT allergen\
                                     FROM ALLERGEN\
                                     WHERE allergenID IN (SELECT allergenID\
                                                           FROM CONTAINS_AL\
                                                            WHERE itemCode=?)",(self.item,))
        allergens_fetch=curr.fetchall()
        allergens=()
        for k in range(len(allergens_fetch)):
                allergens = allergens + (allergens_fetch[k][0], )

        ingredients_var = tk.Variable(value=ingredients)
        allergens_var=tk.Variable(value=allergens)
        listbox = tk.Listbox(
                self,
                listvariable=ingredients_var,
                height=len(ingredients_fetch),
                selectmode=tk.EXTENDED
            )
        
        listbox_allerg=tk.Listbox(
             self,
             listvariable=allergens_var,
             height=len(allergens_fetch),
                selectmode=tk.EXTENDED
        )
        title_label.grid(column=0,row=0,columnspan=3, sticky='w')
        category_label.grid(column=0,row=1,columnspan=3, sticky='w')
        ingredients_label.grid(column=0,row=2,columnspan=3, sticky='w')
        listbox.grid(column = 0, row = 3, rowspan=4,columnspan=3, sticky='w')
        allergens_label.grid(column=0,row=7,columnspan=3, sticky='w')
        listbox_allerg.grid(column=0,row=8, sticky='w')
        rating_label.grid(column=0,row=9,columnspan=3, sticky='w')
        back_btn.grid(column=0, row = 13,columnspan=3, sticky='w')
        conn.close()
        return
    
    def backBtn(self):
        self.master.destroy()
    
    def showratings(self):
        self.destroy()
        from read_revies_page import ReadReviews
        reaviewspg=ReadReviews(self.master,username=self.username,item=self.item,locationID=self.locationID)
        reaviewspg.grid()