from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
from details import *
import pymysql
class CourseClass:
    def __init__(self,pwindow):
        self.window = Toplevel(pwindow)
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        self.window.geometry("%dx%d+%d+%d"%(w-250,h-250,80,80))
        self.headlbl = Label(self.window,text="Course",font=("Algerian",50,'bold'))
        #------------- Widgets ---------------
        self.L1 = Label(self.window,text='Department Name')
        self.L2 = Label(self.window,text='Course Name')
        self.L3 = Label(self.window,text='Fee')
        self.L4 = Label(self.window,text='Duration')


        self.v1 = StringVar()
        self.c1 = Combobox(self.window,textvariable=self.v1)
        self.get_combobox_data()
        self.t2 = Entry(self.window)
        self.t3 = Entry(self.window)
        self.t4 = Entry(self.window)



        self.b1 = Button(self.window,text="Save",command=self.save_data)
        self.b2 = Button(self.window,text="Update",command=self.update_data)
        self.b3 = Button(self.window,text="Delete",command=self.delete_data)
        self.b4 = Button(self.window,text="Fetch",command=self.fetch_data)
        self.b5 = Button(self.window,text="Search",command=self.search_all_data)
        #----------------- table--------------------------

        self.tablearea = Frame(self.window)
        self.mytable = Treeview(self.tablearea, columns=('c1', 'c2', 'c3', 'c4'), height=15)
        self.mytable.heading('c1', text='Department')
        self.mytable.heading('c2', text='Course')
        self.mytable.heading('c3', text='Fee')
        self.mytable.heading('c4', text='Duration')
        self.mytable['show'] = 'headings'
        self.mytable.column("#1", width=200, anchor='center')
        self.mytable.column("#2", width=200, anchor='center')
        self.mytable.column("#3", width=100, anchor='center')
        self.mytable.column("#4", width=100, anchor='center')
        self.mytable.pack()
        self.mytable.bind("<ButtonRelease-1>",lambda e: self.fetch_pk())
        #------------ placements ------------------------------------
        self.headlbl.place(x=0,y=0)
        x1 = 10
        y1= 100

        x_diff=120
        y_diff=50

        self.L1.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)
        self.b5.place(x=x1+x_diff+x_diff+50,y=y1,width=50)
        self.tablearea.place(x=x1+x_diff+x_diff+x_diff+50,y=y1)

        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        self.b4.place(x=x1+x_diff+x_diff+50,y=y1,width=50)

        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.t3.place(x=x1+x_diff,y=y1)

        y1+=y_diff
        self.L4.place(x=x1,y=y1)
        self.t4.place(x=x1+x_diff,y=y1)


        y1+=y_diff

        self.b3.place(x=x1,y=y1,width=50)
        self.b2.place(x=x1+100,y=y1,width=50)
        self.b1.place(x=x1+200,y=y1,width=50)
        self.clearpage()
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
            qry = "insert into course values(%s,%s,%s,%s)"
            row_count = self.curr.execute(qry,(self.v1.get(),self.t2.get(),self.t3.get(),
                                   self.t4.get()))
            self.conn.commit()
            if row_count==1:
                messagebox.showinfo("Success", "Data saved successfully",parent=self.window)
                self.clearpage()
            else:
                messagebox.showwarning("Failure", "Check All Values",parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def update_data(self):
        self.database_connection()
        try:
            # dname cname fee duration
            qry = "update course set dname = %s , fee = %s , duration =  %s where cname = %s"
            row_count = self.curr.execute(qry,(self.v1.get(),self.t3.get(),self.t4.get() ,self.t2.get()))
            self.conn.commit()
            if row_count==1:
                messagebox.showinfo("Success", "Data updated successfully",parent=self.window)
                self.clearpage()
            else:
                messagebox.showwarning("Failure", "Check All Values",parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def delete_data(self):
        ans = messagebox.askquestion("Confirmation","Are you sure to delete??",parent=self.window)
        if ans=='yes':
            self.database_connection()
            try:
                qry = "delete from course where cname = %s"
                rowcount = self.curr.execute(qry,(self.t2.get()))
                self.conn.commit()
                if rowcount==1:
                    messagebox.showinfo("Success","Course Record deleted successfully")
                    self.clearpage()
                else:
                    messagebox.showwarning("Failure","Course Record not deleted successfully\ncheck course name",parent=self.window)

            except Exception as e:
                messagebox.showerror("Query Error","Error while deletion : "+str(e),parent=self.window)

    def fetch_pk(self):
        id = self.mytable.focus()
        items = self.mytable.item(id)
        myvalues = items['values']
        pk = myvalues[1]
        self.fetch_data(pk)

    def fetch_data(self,pk=None):
        if pk==None:
            cn=self.t2.get()
        else:
            cn=pk
        self.database_connection()
        try:
            qry = "select * from course where cname=%s"
            row_count = self.curr.execute(qry,(cn))
            data = self.curr.fetchone()
            print(data)
            self.clearpage()
            if(data):
                self.c1.set(data[0])
                self.t2.insert(0,data[1])
                self.t3.insert(0,data[2])
                self.t4.insert(0,data[3])

                self.b2.config(state="normal")
                self.b3.config(state="normal")
            else:
                messagebox.showwarning("Warning", "No Course Found for this course name", parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def clearpage(self):
        self.c1.set("Choose Department")
        self.t2.delete(0,END)
        self.t3.delete(0,END)
        self.t4.delete(0,END)
        self.b2.config(state="disabled")
        self.b3.config(state="disabled")

    def search_all_data(self):
        self.database_connection()
        self.mytable.delete(*self.mytable.get_children())
        try:
            qry = "select * from course where dname like %s "
            row_count = self.curr.execute(qry,(self.v1.get()+"%"))
            data = self.curr.fetchall()
            if(data):
                for row in data:
                    self.mytable.insert("",END,values=row)
            else:
                messagebox.showwarning("No Record","No Record found for this name ",parent=self.window)


        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def get_combobox_data(self):
        self.database_connection()
        try:
            qry = "select * from department"
            row_count = self.curr.execute(qry)
            data = self.curr.fetchall()
            comboox_list=[]
            if(data):
                for row in data:
                    comboox_list.append(row[0])
                self.c1.set("Choose Department")
            else:
                self.c1.set("No Department")

            self.c1.config(values=comboox_list)

        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)


if __name__ == '__main__':
    d_window=Tk()
    CourseClass(d_window)
    d_window.mainloop()