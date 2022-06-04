from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
from details import *
import pymysql
class createAdminClass:
    def __init__(self):
        self.window = Tk()
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        self.window.geometry("%dx%d+%d+%d"%(650,450,300,250))
        self.headlbl = Label(self.window,text="Welcome to CMS",font=("Algerian",50,'bold'))
        #------------- Widgets ---------------
        self.L1 = Label(self.window,text='User Name')
        self.L2 = Label(self.window,text='Password')
        self.L3 = Label(self.window,text='User Type')

        self.t1 = Entry(self.window)
        self.t2 = Entry(self.window,show='*')
        self.v1 = StringVar()
        self.c1 = Combobox(self.window,values=["Admin","Employee"] , textvariable=self.v1)
        self.c1.current(0)
        self.c1.config(state='disable')

        self.b1 = Button(self.window,text="Create Admin",command=self.save_data)

        #------------ placements ------------------------------------
        self.headlbl.place(x=0,y=0)
        x1 = 10
        y1= 100

        x_diff=120
        y_diff=50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff,y=y1)

        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)

        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)

        y1+=y_diff
        self.b1.place(x=x1+x_diff,y=y1,width=150)
        self.window.mainloop()

    def database_connection(self):
        try:
            self.conn = pymysql.connect(host=myhost, db=mydb,user=myuser,password=mypassword)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Database connection Error : "+str(e),parent=self.window)

    def save_data(self):
        self.database_connection()
        try:
            qry = "insert into usertable values(%s,%s,%s)"
            row_count = self.curr.execute(qry,(self.t1.get(),self.t2.get(),self.v1.get()))
            self.conn.commit()
            if row_count==1:
                messagebox.showinfo("Success", "Admin Created successfully",parent=self.window)
                self.window.destroy()
                from loginpage import loginClass
                loginClass()
            else:
                messagebox.showwarning("Failure", "Check All Values",parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)


if __name__ == '__main__':
    createAdminClass()