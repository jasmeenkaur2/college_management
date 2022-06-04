from tkinter import *
from tkinter import messagebox

from Tools.scripts.serve import app

from RecordPage1 import Record1Class
from RecordPage2 import Record2Class
from StudentPage import StudentClass
from changepassword import changeClass
from coursePage import CourseClass
from departmentpage import DeptClass
from manageUser import UserClass


class HomepageClass:
    def __init__(self,utype,uname):
        self.utype =utype
        self.uname = uname
        self.window = Tk()
        self.window.title("CMS")

        w = self.window.winfo_screenwidth()
        h = self.window.winfo_screenheight()
        #method 1
        self.window.minsize(700,500)
        #method 2
        self.window.geometry("%dx%d+%d+%d"%(700,500,400,200))
        #method 3
        self.window.state('zoomed')
        #------------ background --------------------------

        from PIL import Image,ImageTk
        self.bimg1 = Image.open("myimages//bk1.jpg")
        self.bimg1 = self.bimg1.resize((w, h), Image.ANTIALIAS)
        self.bimg2 = ImageTk.PhotoImage(self.bimg1)
        self.bklbl = Label(self.window,image=self.bimg2)
        self.bklbl.place(x=0,y=0)


        #-----------------------------------------------------------

        self.window.option_add("*TearOff",False)
        #----- menus -----
        self.menubar = Menu()
        self.window.config(menu=self.menubar)

        self.menu1 = Menu()
        self.menu2 = Menu()
        self.menu3 = Menu()
        self.menu4 = Menu()
        self.menubar.add_cascade(menu=self.menu1,label='Details')
        self.menubar.add_cascade(menu=self.menu2,label='Department')
        self.menubar.add_cascade(menu=self.menu3,label='Report')
        self.menubar.add_cascade(menu=self.menu4,label='Account')

        # self.menu1.add_command(label='Student',command=lambda :  StudentClass())  # for independent window
        self.menu1.add_command(label='Student',command=lambda :  StudentClass(self.window))
        self.menu1.add_command(label='Teacher')

        self.menu2.add_command(label='Department', command=lambda: DeptClass(self.window))
        self.menu2.add_command(label='Course', command=lambda: CourseClass(self.window))


        self.menu3.add_command(label='Student Report1', command=lambda: Record1Class(self.window))
        self.menu3.add_command(label='Student Report2', command=lambda: Record2Class(self.window))

        self.menu4.add_command(label='Manage User', command=lambda:  UserClass(self.window))
        self.menu4.add_command(label='Change Password', command=lambda:  changeClass(self.window,self.uname))
        self.menu4.add_command(label='Logout', command=self.quitter)

        if(self.utype=='Employee'):
            self.menubar.entryconfig(1,state='disable')
            self.menubar.delete(2)
            self.menu1.entryconfig(0,state='disable')
            self.menu1.delete(1)
        self.window.mainloop()

    def quitter(self):
        ans = messagebox.askquestion("Confirmation", "Are you sure to LOgout??", parent=self.window)
        if ans == 'yes':
            self.window.destroy()
            from loginpage import loginClass
            loginClass()


if __name__ == '__main__':
    HomepageClass("Employee","emp")