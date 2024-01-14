import tkinter as tk
import sqlite3
import time

class ReadReviews(tk.Frame):
    def __init__(self,master,username,item,locationID,*args,**kwargs):
        super().__init__(master,bg='#D2E9E9',*args,**kwargs)
        self.username=username
        self.item=item
        self.master=master
        self.locationID=locationID
        
        self.master.geometry("650x500")
        
        self.create_content()
        self.path=""
      
        
    

    def create_content(self):
        #labels
        
        color1 = '#D2E9E9'
      
        review_history = tk.Frame(self,bg=color1, padx=40)
        
        review_history.grid(column=0, row=0)
        
       
        review_label = tk.Label(review_history, text = "Review History",bg='#D2E9E9',fg='black',font=40)
        
       
        review_label.grid(column=0, row=0)
        back_btn=tk.Button(self,text="Back" ,font=('Calibri', 13, 'bold'), height=2, width =5,\
            command=lambda: self.back(self.username))
        back_btn.grid(column = 0, row = 3,pady=10)
        start_time = time.time()
        conn=sqlite3.connect("upEAT_1.sqlite")
        review_data=conn.execute("SELECT R.stars, R.review,F.itemName,R.locationID, R.date\
                                        FROM REVIEWS AS R, FOOD_ITEM AS F\
                                        WHERE F.itemCode=R.itemCode\
                                        AND R.itemCode=? AND R.locationID=?\
                                        ORDER BY R.date DESC",(self.item,self.locationID,)).fetchall()

        conn.close()
        end_time = time.time()
        print("Elapsed time: " + str(end_time-start_time))
        reviews = ()
        for j in range(len(review_data)):
            reviews += ('Stars: ' + review_data[j][0]+ '/5 | Food Item: '+ review_data[j][2]+ ' | Date:' + review_data[j][4],)\
                + ('Review: '+review_data[j][1],) \
                    + ('--------------------------------------------------------------------------------------------',)

        
        reviews_var = tk.Variable(value=reviews)
        
        
        review_listbox = tk.Listbox(
            review_history,
            listvariable=reviews_var,
            height=15,
            width=80,
            selectmode=tk.EXTENDED
        )
        

        
        review_listbox.grid(row=1,column=0)


    def back(self,username):
        self.destroy()
        from itemFrame import itemFrame
        itemframe=itemFrame(self.master,username=self.username,item=self.item,locationID=self.locationID)
        itemframe.grid()
        