import os
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Combobox, Treeview
import pymysql

from details import *
from printing import my_cust_PDF


class Record1Class:
    def __init__(self,pwindow):
        self.window = Toplevel(pwindow)
        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        self.window.geometry("%dx%d+%d+%d"%(w-250,h-250,80,80))
        self.headlbl = Label(self.window,text="STUDENT Record",font=("Algerian",50,'bold'))
        #------------- Widgets ---------------
        self.tablearea = Frame(self.window)
        self.mytable =Treeview(self.tablearea,columns=('c1','c2','c3','c4','c5','c6','c7','c8'),height=20)
        self.mytable.heading('c1',text='Roll No')
        self.mytable.heading('c2',text='Name')
        self.mytable.heading('c3',text='Phone')
        self.mytable.heading('c4',text='Gender')
        self.mytable.heading('c5',text='DOB')
        self.mytable.heading('c6',text='Address')
        self.mytable.heading('c7',text='Department')
        self.mytable.heading('c8',text='Course')
        self.mytable['show']='headings'
        self.mytable.column("#1",width=100,anchor='center')
        self.mytable.column("#2",width=200,anchor='n')
        self.mytable.column("#3",width=100,anchor='e')
        self.mytable.column("#4",width=100,anchor='center')
        self.mytable.column("#5",width=100,anchor='center')
        self.mytable.column("#6",width=300,anchor='center')
        self.mytable.column("#7",width=200,anchor='center')
        self.mytable.column("#8",width=200,anchor='center')
        self.mytable.pack()


        self.b1 = Button(self.window,text='PRINT',command =self.get_printout)
        #------------ placements ------------------------------------
        self.headlbl.place(x=0,y=0)
        x1 = 10
        y1= 100
        x_diff=100
        y_diff=50
        self.tablearea.place(x=x1,y=y1)

        self.b1.place(x=x1+300,y=y1+500)
        self.search_all_data()
        self.window.mainloop()

    def database_connection(self):
        try:
            self.conn = pymysql.connect(host=myhost, db=mydb,user=myuser,password=mypassword)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Database connection Error : "+str(e),parent=self.window)

    def search_all_data(self):
        self.database_connection()
        try:
            qry = "select * from student"
            row_count = self.curr.execute(qry)
            data = self.curr.fetchall()
            self.print_data=[]
            print(data)
            if(data):
              for row in data:
                  self.print_data.append(row[:-1])
                  self.mytable.insert("",END,values=row)

        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def get_printout(self):
        pdf = my_cust_PDF()
        headings = ['Rollno', 'Name', 'Gender', 'Phone No', 'Address', 'Department', 'Course', 'DOB']

        pdf.print_chapter(self.print_data,  headings)
        pdf.output('pdf_file1.pdf')
        os.system('explorer.exe "pdf_file1.pdf"')


if __name__ == '__main__':
    d_window=Tk()
    Record1Class(d_window)
    d_window.mainloop()