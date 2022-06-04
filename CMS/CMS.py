from tkinter import messagebox
import pymysql
from details import *
class MainClass:
    def __init__(self):
        self.database_connection()
        try:
            qry = "select * from usertable"
            row_count = self.curr.execute(qry)
            data = self.curr.fetchall()
            if(data):
                from loginpage import loginClass
                loginClass()
            else:
                from createadmin import createAdminClass
                createAdminClass()

        except Exception as e:
            messagebox.showerror("Query Error","Query Error : "+str(e))

    def database_connection(self):
        try:
            self.conn = pymysql.connect(host=myhost, db=mydb, user=myuser, password=mypassword)
            self.curr = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Error", "Database connection Error : " + str(e))


if __name__ == '__main__':
    MainClass()