import mysql.connector

from core.DB_fill.reach_api import OffAPI
from core.consts import HOST_ADRESS, USER_NAME, PWD, DB_NAME
from core.div import *


class Purbeurre_db():
    """ Database interface """
    def __init__(self, mode="normal"):
        self.Api = OffAPI() #Module used to reach the Open Food Fact API
        self.conn = None
        self.cursor = None
        self.requirements_check()

    def connectdb(self):
        """ Connection to database """
        self.conn = mysql.connector.connect(
            host=HOST_ADRESS,
            user=USER_NAME,
            password=PWD,
            database=DB_NAME
            )

        self.cursor = self.conn.cursor()



    def del_cat(self, cat_name):
        self.connectdb()
        query = "SELECT cat_code FROM ta_categories WHERE cat_name={}".format(cat_name)
        self.cursor.execute(query)
        code = self.cursor.fetchall()

        query = "DELETE FROM products WHERE cat_code=" + code
        self.cursor.execute(query)
        self.conn.commit()
        self.conn.close()

    def fill(self):
        tags = self.Api.dump_tags()

        for tag in tags:
            self.add_cat(tag)



    def requirements_check(self):
        try:
            self.connectdb()

        except:
            self.install()
        

    def install(self):
        """ Initialisation of the database, used only at installation of the program """

        self.conn = mysql.connector.connect(
            host=HOST_ADRESS,
            user=USER_NAME,
            passwd=PWD
            )

        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE DATABASE " + DB_NAME)
        self.conn.close()

        self.conn = None
        self.cursor = None
        self.create_tables() #create the tables
        self.fill()

if __name__ == "__main__":
    print("ERROR:reach_api.py: This is a class file. Don't use it as main program.")
    exit(0)