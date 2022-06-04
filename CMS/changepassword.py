from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
from details import *
import pymysql
class changeClass:
    def __init__(self,pwindow,uname):
        self.uname =uname
        self.window = Toplevel(pwindow)
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        self.window.geometry("%dx%d+%d+%d"%(w-250,h-250,80,80))
        self.headlbl = Label(self.window,text="User",font=("Algerian",50,'bold'))
        #------------- Widgets ---------------
        self.L1 = Label(self.window,text='Current Password')
        self.L2 = Label(self.window,text='New Password')
        self.L3 = Label(self.window,text='Confirm Password')

        self.t1 = Entry(self.window,show='*')
        self.t2 = Entry(self.window,show='*')
        self.t3 = Entry(self.window,show='*')


        self.b1 = Button(self.window,text="Change",command=self.update_data)

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
        self.t3.place(x=x1+x_diff,y=y1)

        y1+=y_diff
        self.b1.place(x=x1+200,y=y1,width=50)
        self.clearpage()
        self.window.mainloop()

    def database_connection(self):
        try:
            self.conn = pymysql.connect(host=myhost, db=mydb,user=myuser,password=mypassword)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Database connection Error : "+str(e),parent=self.window)

    def update_data(self):
        if self.t2.get()==self.t3.get():
            self.database_connection()
            try:
                # dname cname fee duration
                qry = "update usertable set password = %s   where username = %s and password = %s"
                row_count = self.curr.execute(qry,(self.t2.get(),  self.uname  ,self.t1.get()))
                self.conn.commit()
                if row_count==1:
                    messagebox.showinfo("Success", "passsword changed successfully",parent=self.window)
                    self.clearpage()
                else:
                    messagebox.showwarning("Failure", "Wrong password",parent=self.window)
            except Exception as e:
                messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)
        else:
            messagebox.showwarning("Failure", "Confirm Password Carefully",parent=self.window)

    def clearpage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        self.t3.delete(0,END)




if __name__ == '__main__':
    d_window=Tk()
    changeClass(d_window)
    d_window.mainloop()