from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Combobox, Treeview
from details import *
import pymysql
from tkcalendar import DateEntry
from PIL import Image,ImageTk
class StudentClass:
    default_img = "default_image2.jpg"
    def __init__(self,pwindow):
        # self.window = Tk()   # create independent window
        # self.window = pwindow  #  now both windows are same
        self.window = Toplevel(pwindow) # now pwindow acts as parent to child window (student)


        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        self.window.geometry("%dx%d+%d+%d"%(w-250,h-250,80,80))
        self.headlbl = Label(self.window,text="STUDENT",font=("Algerian",50,'bold'))
        #------------- Widgets ---------------
        self.L1 = Label(self.window,text='Rollno')
        self.L2 = Label(self.window,text='Name')
        self.L3 = Label(self.window,text='Phone')
        self.L4 = Label(self.window,text='Gender')
        self.L5 = Label(self.window,text='DOB')
        self.L6 = Label(self.window,text='Address')
        self.L7 = Label(self.window,text='Department')
        self.L8 = Label(self.window,text='Course')

        self.t1 = Entry(self.window)
        self.t2 = Entry(self.window)
        self.t3 = Entry(self.window)
        self.v1 = StringVar()
        self.r1 = Radiobutton(self.window,text='Male',value='male',variable=self.v1)
        self.r2 = Radiobutton(self.window,text='Female',value='female',variable=self.v1)
        self.t5 = DateEntry(self.window, width=12, background='darkblue', foreground='white', borderwidth=2,
                            date_pattern="y-mm-dd"  )
        self.t6 = Text(self.window,width=15,height=3)
        self.v2 = StringVar()
        self.c1 = Combobox(self.window,textvariable=self.v2)
        self.get_combobox1_data()
        self.c1.bind("<<ComboboxSelected>>", lambda e: self.get_combobox2_data())

        self.v3 = StringVar()
        self.c2 = Combobox(self.window,textvariable=self.v3)


        self.b1 = Button(self.window,text="Save",command=self.save_data)
        self.b2 = Button(self.window,text="Update",command=self.update_data)
        self.b3 = Button(self.window,text="Delete",command=self.delete_data)
        self.b4 = Button(self.window,text="Fetch",command=self.fetch_data)
        self.b5 = Button(self.window,text="Search",command=self.search_all_data)
        self.b6 = Button(self.window,text="Upload",command=self.get_image)

        self.imglbl=Label(self.window,borderwidth=2,relief='groove')
        #----------------- table--------------------------

        self.tablearea = Frame(self.window)
        self.mytable = Treeview(self.tablearea, columns=('c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8'), height=10)
        self.mytable.heading('c1', text='Roll No')
        self.mytable.heading('c2', text='Name')
        self.mytable.heading('c3', text='Phone')
        self.mytable.heading('c4', text='Gender')
        self.mytable.heading('c5', text='DOB')
        self.mytable.heading('c6', text='Address')
        self.mytable.heading('c7', text='Department')
        self.mytable.heading('c8', text='Course')
        self.mytable['show'] = 'headings'
        self.mytable.column("#1", width=80, anchor='center')
        self.mytable.column("#2", width=100, anchor='center')
        self.mytable.column("#3", width=100, anchor='center')
        self.mytable.column("#4", width=100, anchor='center')
        self.mytable.column("#5", width=100, anchor='center')
        self.mytable.column("#6", width=100, anchor='center')
        self.mytable.column("#7", width=100, anchor='center')
        self.mytable.column("#8", width=100, anchor='center')
        self.mytable.pack()
        self.mytable.bind("<ButtonRelease-1>",lambda e: self.fetch_pk())
        #------------ placements ------------------------------------
        self.headlbl.place(x=0,y=0)
        x1 = 10
        y1= 100

        x_diff=100
        y_diff=50

        self.L1.place(x=x1,y=y1)
        self.t1.place(x=x1+x_diff,y=y1)
        self.b4.place(x=x1+x_diff+x_diff+50,y=y1,width=50)
        self.tablearea.place(x=x1+x_diff+x_diff+x_diff+50,y=y1)

        y1+=y_diff
        self.L2.place(x=x1,y=y1)
        self.t2.place(x=x1+x_diff,y=y1)
        self.b5.place(x=x1+x_diff+x_diff+50,y=y1,width=50)

        y1+=y_diff
        self.L3.place(x=x1,y=y1)
        self.t3.place(x=x1+x_diff,y=y1)

        y1+=y_diff
        self.L4.place(x=x1,y=y1)
        self.r1.place(x=x1+x_diff,y=y1)
        self.r2.place(x=x1+x_diff+x_diff,y=y1)

        y1+=y_diff
        self.L5.place(x=x1,y=y1)
        self.t5.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L6.place(x=x1,y=y1)
        self.t6.place(x=x1+x_diff,y=y1)



        self.imglbl.place(x=x1+400,y=y1,width=150,height=150)
        self.b6.place(x=x1+400,y=y1+150,width=150,height=40)

        y1+=y_diff
        y1+=10
        self.L7.place(x=x1,y=y1)
        self.c1.place(x=x1+x_diff,y=y1)
        y1+=y_diff
        self.L8.place(x=x1,y=y1)
        self.c2.place(x=x1+x_diff,y=y1)

        y1+=y_diff

        self.b3.place(x=x1,y=y1,width=50)
        self.b2.place(x=x1+100,y=y1,width=50)
        self.b1.place(x=x1+200,y=y1,width=50)
        self.clearpage()
        self.window.mainloop()

    def get_image(self):
        self.filename = askopenfilename(file = [ ("All pictures","*.png;*.jpg;*.jpeg")  ,("PNG Images ","*.png"),("JPG Images ","*.jpg")  ])
        print("filename = ",self.filename)
        if self.filename!="":
            # pick image and resize it
            self.img1 = Image.open(self.filename)
            self.img1 = self.img1.resize((150,150),Image.ANTIALIAS)

            # making it photoimage for label(as label accepts only this type0
            self.img2 = ImageTk.PhotoImage(self.img1)
            self.imglbl.config(image=self.img2)

            path = self.filename.split("/")  # extracting path from whole filename
            name = path[-1]  # getting last value(i.e. name of image)
            import time
            uniqueness = str(int(time.time()))   # making timestamp as string
            self.actual_name = uniqueness+name# making it unique by adding time stamp
            print("name = ",self.actual_name)

    def database_connection(self):
        try:
            self.conn = pymysql.connect(host=myhost, db=mydb,user=myuser,password=mypassword)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error","Database connection Error : "+str(e),parent=self.window)

    def save_data(self):
        if(self.validate_check()==False):
            return   # stop this function now




        self.database_connection()

        if self.actual_name==self.default_img: # no image is selected
            #nothing to save in folder
            pass
        else:    # image is selected
            self.img1.save("student_images//"+self.actual_name)  # image saved in folder


        try:
            qry = "insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            row_count = self.curr.execute(qry,(self.t1.get(),self.t2.get(),self.t3.get(),
                                   self.v1.get(),self.t5.get_date(),self.t6.get('1.0',END),
                                   self.v2.get(),self.v3.get(),self.actual_name))
            self.conn.commit()
            if row_count==1:
                messagebox.showinfo("Success", "Data saved successfully",parent=self.window)
                self.clearpage()
            else:
                messagebox.showwarning("Failure", "Check All Values",parent=self.window)
        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def update_data(self):

        if(self.validate_check()==False):
            return   # stop this function now



        self.database_connection()


        if self.actual_name==self.old_name:     # no new image is selected
            # nothing to delete or save
            pass
        else:   # new image is selected
            self.img1.save("student_images//"+self.actual_name)  # save image
            if self.old_name==self.default_img: # no old image was given in past
                #nothing to delete
                pass
            else:   # image was given in past
                import os
                os.remove("student_images//"+self.old_name)


        try:

            qry = "update student set name = %s , phone = %s , gender = %s , dob = %s , " \
                  "address = %s , department = %s , course = %s,pic=%s  where rollno = %s"
            row_count = self.curr.execute(qry,(self.t2.get(),self.t3.get(),
                                   self.v1.get(),self.t5.get_date(),self.t6.get('1.0',END),
                                   self.v2.get(),self.v3.get(),self.actual_name,self.t1.get()))
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

            if self.old_name==self.default_img: # no old image was given in past
                #nothing to delete
                pass
            else:   # image was given in past
                import os
                os.remove("student_images//"+self.old_name)


            self.database_connection()
            try:
                qry = "delete from student where rollno = %s"
                rowcount = self.curr.execute(qry,(self.t1.get()))
                self.conn.commit()
                if rowcount==1:
                    messagebox.showinfo("Success","Student Record deleted successfully")
                    self.clearpage()
                else:
                    messagebox.showwarning("Failure","Student Record not deleted successfully\ncheck rollno",parent=self.window)

            except Exception as e:
                messagebox.showerror("Query Error","Error while deletion : "+str(e),parent=self.window)

    def fetch_pk(self):
        id = self.mytable.focus()
        # print("id = ",id)
        items = self.mytable.item(id)
        # print("item = ",items)
        myvalues = items['values']
        # print(myvalues)
        pk = myvalues[0]   # 0 index of list( values's list)
    # print("pk = ",pk)

        self.fetch_data(pk)

    def fetch_data(self,pk=None):
        if pk==None:
            rollno=self.t1.get()
        else:
            rollno=pk
        self.database_connection()
        try:
            qry = "select * from student where rollno=%s"
            row_count = self.curr.execute(qry,(rollno))
            data = self.curr.fetchone()
            print(data)
            self.clearpage()
            if(data):
                self.t1.insert(0,data[0])
                self.t2.insert(0,data[1])
                self.t3.insert(0,data[2])
                self.v1.set(data[3])
                self.t5.insert(0,data[4])
                self.t6.insert('1.0',data[5])
                self.c1.set(data[6])
                self.c2.set(data[7])
                self.actual_name = data[8]
                self.old_name = data[8]

                # add old image in label
                self.img1 = Image.open("student_images//" + self.actual_name)
                self.img1 = self.img1.resize((150, 150), Image.ANTIALIAS)
                self.img2 = ImageTk.PhotoImage(self.img1)
                self.imglbl.config(image=self.img2)




                self.b2.config(state="normal")
                self.b3.config(state="normal")
            else:
                messagebox.showwarning("Warning", "No Student Found for this rollno", parent=self.window)

        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def clearpage(self):
        self.t1.delete(0,END)
        self.t2.delete(0,END)
        self.t3.delete(0,END)
        self.v1.set(None)
        self.t5.delete(0,END)
        self.t6.delete('1.0',END)
        self.c1.set("Choose Department")
        self.c2.set("No Course")
        self.b2.config(state="disabled")
        self.b3.config(state="disabled")
        self.actual_name =self.default_img

        # add default image in label
        self.img1 = Image.open("student_images//"+self.actual_name)
        self.img1 = self.img1.resize((150, 150), Image.ANTIALIAS)
        self.img2 = ImageTk.PhotoImage(self.img1)
        self.imglbl.config(image=self.img2)

    def search_all_data(self):
        self.database_connection()
        self.mytable.delete(*self.mytable.get_children())
        try:
            qry = "select * from student where name like %s "
            row_count = self.curr.execute(qry,(self.t2.get()+"%"))
            data = self.curr.fetchall()
            if(data):
                for row in data:
                    self.mytable.insert("",END,values=row)
            else:
                messagebox.showwarning("No Record","No Record found for this name ",parent=self.window)


        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def get_combobox1_data(self):
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

    def get_combobox2_data(self):
        self.database_connection()
        try:
            qry = "select * from course where dname=%s"
            row_count = self.curr.execute(qry,(self.v2.get()))
            data = self.curr.fetchall()
            comboox_list=[]
            if(data):
                for row in data:
                    comboox_list.append(row[1])
                self.c2.set("Choose Course")
            else:
                self.c2.set("No Course")

            self.c2.config(values=comboox_list)

        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e),parent=self.window)

    def validate_check(self):
        if not(self.t1.get().isdigit()) or len(self.t1.get())==0:
            messagebox.showwarning("Validation Check", "Invalid Roll no", parent=self.window)
            return False
        elif not(self.t2.get().isalpha())   or  len(self.t2.get())<3:
            messagebox.showwarning("Validation Check", "Enter proper name (atleast 3 chracters) ", parent=self.window)
            return False
        elif not(self.t3.get().isdigit())   or  len(self.t3.get())!=10:
            messagebox.showwarning("Validation Check", "Enter valid phone no \n10 digits only", parent=self.window)
            return False
        elif not (self.v1.get() == 'male' or self.v1.get() == 'female'):
            messagebox.showwarning("Input Error", "Please Select gender ", parent=self.window)
            return False
        elif (self.t5.get() == ""):
            messagebox.showwarning("Input Error", "Please Select DOB ", parent=self.window)
            return False
        elif len(self.t6.get('1.0', END)) < 3:
            messagebox.showwarning("Input Error", "Please Enter Address ", parent=self.window)
            return False
        elif (self.v2.get() == "Choose Department")or (self.v2.get() == "No Department"):
            messagebox.showwarning("Input Error", "Please Select Department ", parent=self.window)
            return False
        elif (self.v3.get() == "Choose Course") or (self.v3.get() == "No Course"):
            messagebox.showwarning("Input Error", "Please Select Course ", parent=self.window)
            return False

        return True

if __name__ == '__main__':
    d_window=Tk()
    StudentClass(d_window)
    d_window.mainloop()