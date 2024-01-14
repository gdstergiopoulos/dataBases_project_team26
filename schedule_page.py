import tkinter as tk
import datetime
import sqlite3
from navigator import Navigator

class ScheduleFrame(tk.Frame):
    def __init__(self,master,username,**kwargs):
        super().__init__(master,bg='#D2E9E9',**kwargs)
        self.username=username
        self.master=master
        self.navigator=Navigator(self,master,username=self.username)
        self.master.geometry("850x650")
        self.pack(side='left')
        self.create_content()
        self.path=""
        
    

    def create_content(self):
        self.current_date = datetime.datetime.today().date()
        self.new_date = self.current_date
        self.create_window(self.current_date)

    def callback(self,event):
        selection = event.widget.curselection()
        if selection:
            index = selection[0]
            data = event.widget.get(index)
            conn=sqlite3.connect("upEAT_1.sqlite")
            cursor=conn.execute("SELECT itemCode\
                                FROM FOOD_ITEM\
                                WHERE itemName=? AND locationID=?",(data,1,)).fetchall()
            itemcode=cursor[0][0]
            conn.close()
            from item_window import itemWindow
            item_window=itemWindow(self,item=itemcode,locationID=1,username=self.username)
            return
        else:
            print("nothing")
        
        
    def create_window(self,new_date):
        if((self.current_date - new_date).days>21 or (self.current_date - new_date).days<-21):
            return
        else:
            
            self.new_date = new_date
            #labels
            color1 = '#D2E9E9'
            color2 = '#D2E9E9'
            current_date = datetime.date.today()
            #new_date=datetime.date(2023,12,25)
            week_day = new_date.weekday()
            #week_day= 0
            week_frame = [0]*7 
            break_label = [0]*7
            lunch_label = [0]*7
            dinner_label = [0]*7
            listbox = [0]*7*3
            for i in range(7):
                week_frame[i] = tk.Frame(self, bg=color1)
            
            weekdays = ["Monday - ", "Tuesday - ", "Wednesday - ", "Thursday - ", "Friday - ", "Saturday - ", "Sunday - "]
            i=0
            mon_label=tk.Label(week_frame[i], text="Monday - "+ \
                str(new_date+ datetime.timedelta(days=-week_day + i)),bg='#D2E9E9',fg='black',font=('Calibri', 13, 'bold'))
            week_frame[i].grid(row = 0, column = 0, padx=10)
            i +=1
            tue_label=tk.Label(week_frame[i], text="Tuesday - "+\
                str(new_date+ datetime.timedelta(days=-week_day + i)),bg='#D2E9E9',fg='black',font=('Calibri', 13, 'bold'))
            week_frame[i].grid(row = 0, column = 1, padx=10)
            i +=1
            wed_label=tk.Label(week_frame[i], text="Wednesday - "+\
                str(new_date+ datetime.timedelta(days=-week_day + i)),bg='#D2E9E9',fg='black',font=('Calibri', 13, 'bold'))
            week_frame[i].grid(row = 0, column = 2, padx=10)
            i +=1
            thu_label=tk.Label(week_frame[i], text="Thursday - "+\
                            str(new_date+ datetime.timedelta(days=-week_day + i)),bg='#D2E9E9',fg='black',font=('Calibri', 13, 'bold'))
            week_frame[i].grid(row = 1, column = 0, padx = 30)
            i +=1
            fri_label=tk.Label(week_frame[i], text="Friday - "+\
                str(new_date+ datetime.timedelta(days=-week_day + i)),bg='#D2E9E9',fg='black',font=('Calibri', 13, 'bold'))
            week_frame[i].grid(row = 1, column = 1)
            i +=1
            sat_label=tk.Label(week_frame[i], text="Saturday - "+\
                str(new_date+ datetime.timedelta(days=-week_day + i)),bg='#D2E9E9',fg='black',font=('Calibri', 13, 'bold'))
            week_frame[i].grid(row = 1, column = 2)
            i +=1
            sun_label=tk.Label(week_frame[i], text="Sunday - "+\
                str(new_date+ datetime.timedelta(days=-week_day + i)),bg='#D2E9E9',fg='black',font=('Calibri', 13, 'bold'))
            week_frame[i].grid(row = 1, column = 3)
            i=0
            
            prev_btn = tk.Button(self,text="Previous Week",command=lambda: self.create_window(self.new_date-datetime.timedelta(days=7)))
            next_btn = tk.Button(self,text="Next Week",command=lambda: self.create_window(self.new_date+datetime.timedelta(days=7)))
            back_btn = tk.Button(self,text="Back",command=lambda: self.back(self.username))
            back_btn.grid(row=2, column=2, pady=10)
            prev_btn.grid(column=0, row=2, pady=10)
            next_btn.grid(row=2, column=3, pady=10)
            for i in range(7): 
                break_label[i]=tk.Label(week_frame[i], text="Breakfast",bg='#D2E9E9',fg='black',font=30)
                lunch_label[i]=tk.Label(week_frame[i], text="Lunch",bg='#D2E9E9',fg='black',font=30)
                dinner_label[i]=tk.Label(week_frame[i], text="Dinner",bg='#D2E9E9',fg='black',font=30)
                break_label[i].grid(row=1,column=0)
                lunch_label[i].grid(row=3,column=0)
                dinner_label[i].grid(row=5,column=0)
                
                formatted_date = new_date + datetime.timedelta(days=-week_day + i)
                formatted_date_str = formatted_date.strftime("%Y-%m-%d")
                # formatted_date_str=("2023-12-24")
                conn=sqlite3.connect("upEAT_1.sqlite")
                cursor=conn.execute("SELECT itemName\
                                    FROM FOOD_ITEM\
                                    WHERE itemCode IN (SELECT I.itemCode\
                                    FROM OFFERS_SCHEDULE AS O,SCHEDULE AS S,INCLUDES_FOOD AS I\
                                    WHERE O.scheduleID=S.scheduleID AND O.scheduleID=I.scheduleID AND O.locationID=1 AND O.date=?\
                                    AND O.meal='breakfast')",(formatted_date_str,))
                breakfast_fetch=cursor.fetchall() 
                
                cursor=conn.execute("SELECT itemName\
                                    FROM FOOD_ITEM\
                                    WHERE itemCode IN (SELECT I.itemCode\
                                    FROM OFFERS_SCHEDULE AS O,SCHEDULE AS S,INCLUDES_FOOD AS I\
                                    WHERE O.scheduleID=S.scheduleID AND O.scheduleID=I.scheduleID AND O.locationID=1 AND O.date=?\
                                    AND O.meal='lunch')",(formatted_date_str,))
                lunch_fetch=cursor.fetchall() 
                
                cursor=conn.execute("SELECT itemName\
                                    FROM FOOD_ITEM\
                                    WHERE itemCode IN (SELECT I.itemCode\
                                    FROM OFFERS_SCHEDULE AS O,SCHEDULE AS S,INCLUDES_FOOD AS I\
                                    WHERE O.scheduleID=S.scheduleID AND O.scheduleID=I.scheduleID AND O.locationID=1 AND O.date=?\
                                    AND O.meal='dinner')",(formatted_date_str,))
                dinner_fetch=cursor.fetchall() 
                conn.close()
                breakfast = ()
                lunch = ()
                dinner = ()
                for k in range(len(breakfast_fetch)):
                    breakfast = breakfast + (breakfast_fetch[k][0], )
                
                
                    
                for j in range(len(lunch_fetch)):
                    lunch += (lunch_fetch[j][0], )

                for q in range(len(dinner_fetch)):
                    dinner += (dinner_fetch[q][0], )
                
                break_var = tk.Variable(value=breakfast)
                lunch_var = tk.Variable(value=lunch)
                dinner_var = tk.Variable(value=dinner)
                
                listbox[3*i] = tk.Listbox(
                    week_frame[i],
                    listvariable=break_var,
                    height=3,
                    selectmode=tk.EXTENDED
                )
                listbox[3*i+1] = tk.Listbox(
                    week_frame[i],
                    listvariable=lunch_var,
                    height=3,
                    selectmode=tk.EXTENDED
                )
                listbox[3*i+2] = tk.Listbox(
                    week_frame[i],
                    listvariable=dinner_var,
                    height=3,
                    selectmode=tk.EXTENDED
                )

                listbox[3*i].grid(row=2,column=0)
                listbox[3*i+1].grid(row=4,column=0)
                listbox[3*i+2].grid(row=6,column=0)

                

                listbox[3*i].bind("<<ListboxSelect>>", self.callback)
                listbox[3*i+1].bind("<<ListboxSelect>>", self.callback)
                listbox[3*i+2].bind("<<ListboxSelect>>", self.callback)

            

            mon_label.grid(row=0,column=0,columnspan=3,pady=10)
            tue_label.grid(row=0,column=0,columnspan=3,pady=10)
            wed_label.grid(row=0,column=0,columnspan=3,pady=10)
            thu_label.grid(row=0,column=0,columnspan=3,pady=10)
            fri_label.grid(row=0,column=0,columnspan=3,pady=10)
            sat_label.grid(row=0,column=0,columnspan=3,pady=10)
            sun_label.grid(row=0,column=0,columnspan=3,pady=10)


    def back(self,username):
        from home_page import WelcomeFrame
        self.destroy()
        purchase_frame=WelcomeFrame(self.master, username=username)
        purchase_frame.pack()