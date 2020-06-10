import mysql.connector

from core.consts import HOST_ADRESS, USER_NAME, PWD, DB_NAME

class Product():
    def __init__(self, id, name, cat, img, cats, score):
        self.id                 = id
        self.generic_name       = name
        self.categorie          = cat
        self.image_url          = img
        self.sub_cats           = cats
        self.nutrition_grade    = score

class Categorie():
    def __init__(self, cat_name, cat_code):
        self.name = cat_name
        self.code = cat_code

class ORM():

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.categories = None

        self.get_cats()

    def connectdb(self):
        """ Connection to database """
        self.conn = mysql.connector.connect(host=HOST_ADRESS, user=USER_NAME, password=PWD, database=DB_NAME)
        self.cursor = self.conn.cursor()

    def get_cats(self):
        self.connectdb()
        self.cursor.execute("SELECT * FROM ta_categories;")
        rows = self.cursor.fetchall()
        self.conn.close()

        lst = []
        i = 1
        for cat in rows:
            temp = Categorie(i, cat[1], cat[2])
            i += 1
            lst.append(temp)

        self.categories = lst
        return lst

    def get_cat_products(self, cat_name="", cat_code=""):
        self.connectdb()
        
        if cat_name != "" and cat_code == "":
            query = "SELECT * FROM ta_categories WHERE cat_name={};".format(cat_name)
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            cat_code = rows[0][1]


        query = "SELECT * FROM products WHERE cat_code={};".format(cat_code)
        
        rows = self.cursor.execute(query)

        lst = []
        for row in rows:
            temp = Product(row[0], row[1], row[2], row[3], row[4], row[5])
            slt.append(temp)

        return lst
