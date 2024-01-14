import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class AllergiesWindow():
    def __init__(self,ssn):
        self.alerg_win=tk.Tk()
        self.alerg_win.title("Register Allergies")
        self.ssn=ssn
        self.alerg_win.configure(bg='#D2E9E9')
        self.alerg_win.geometry("300x300")
        self.create_content(self.alerg_win)
        

    def create_content(self,alerg_win):
        #labels
        allerg_label=tk.Label(alerg_win, text="Add Allergies",bg='#D2E9E9',fg='black',font=30)
        allerg_select_label=tk.Label(alerg_win, text="Select you allergies",bg='#D2E9E9',fg='black',font=30)
        #username+password
        self.conn=sqlite3.connect('upEAT_1.sqlite')
        self.curr=self.conn.execute('SELECT allergen\
                                    FROM ALLERGEN')
        data=self.curr.fetchall()
        allergies_list=[]
        for i in range(len(data)-1):
            allergies_list.append(data[i][0])
        allergies_list.append("Other")
        self.conn.close()

        allerg_select=ttk.Combobox(alerg_win,width=17,values=allergies_list)
        
        

        allerg_entry=tk.Text(alerg_win,height=5,width=15)
        allerg_entry_label=tk.Label(alerg_win, text="Or Describe Another",bg='#D2E9E9',fg='black',font=30)
       

        allerg_label.grid(row=0,column=0,columnspan=3,pady=10)
        allerg_select_label.grid(row=1,column=0,sticky="news",pady=10,padx=5)
        allerg_select.grid(row=1,column=1)
        allerg_entry_label.grid(row=2,column=0,padx=5)
        allerg_entry.grid(row=2,column=1,pady=10)

        reg_alerg_btn=tk.Button(alerg_win,text="Register Alergies",command=lambda: self.regAlergBtn(alerg_win,allerg_select.get(),allerg_entry.get("1.0",'end-1c')))
        reg_alerg_btn.grid(row=3,column=1,pady=10)

    def regAlergBtn(self,alerg_win,aller_select,allerg_describe):
        if(self.ssn=="" or self.ssn==None):
                messagebox.showerror("ERROR SUBMITING ALLERGY","You need to fill the fields marked with (*) before registing an allergy")
                alerg_win.destroy()
                return
        
        if(aller_select==None or aller_select==""):
            messagebox.showerror("Allergy Submision Failed","You must select an allergy from the given list or select 'Other' and describe one")
            return
        else:
            if(aller_select=="Other"):
                if(allerg_describe=="" or allerg_describe==None):
                    messagebox.showerror("Describe your allergy","You selected 'Other', so please describe your allergy for our staff to add it to your account")
                    return
                else:
                    messagebox.showinfo("Submition Done","Our medical staff will review\
                                    and add your allergy to the above list")
                    alerg_win.destroy()
                    return
            else:
                self.conn=sqlite3.connect('upEAT_1.sqlite')
                self.curr=self.conn.execute('SELECT allergenID\
                                        FROM ALLERGEN\
                                        WHERE allergen=?',(aller_select,))
                allid=self.curr.fetchall()[0][0]
                self.curr=self.conn.execute('INSERT INTO IS_ALLERGIC(allergenID,SSN)\
                                        VALUES (?,?)',(allid,self.ssn))
                self.conn.commit()
                self.conn.close()
                alerg_win.destroy()
            
                return
        return
            
        


        