import mysql

from consts import HOST_ADRESS, USER_NAME, PWD, DB_NAME

class Product():
    def __init__(self, id, name, cat, img, cats, score):
        self.id                 = id
        self.generic_name       = name
        self.categorie          = cat
        self.image_url          = img
        self.categories         = cats
        self.nutrition_grades   = score

class Categorie():
    def __init__(self, id, name, quantity):
        self.id         = id
        self.name       = name
        self.quantity   = quantity

class Table():

    def __init__(self, name):
        self.name = name

    def connectdb(self):
        """ Connection to database """
        conn = mysql.connector.connect(host=HOST_ADRESS, user=USER_NAME, password=PWD, database=DB_NAME)
        cursor = conn.cursor()
        return conn, cursor


class Products_manager(Table):
    
    def filter(self, cat, grade_under=""):
        
        if grade_under != "":
            conn, cursor = self.connectdb()

            query = "SELECT * FROM products where nutrition_grade<={};".format(grade_under)
            cursor.execute(query)
            rows = cursor.fetchall()

            prods = []

            for row in rows:
                prod = Product(row[0], row[1], row[2], row[3], row[4], row[5])
                prods.append(prod)

            return prods



class Categories_manager(Table):

    def list_cats(self):
        conn, cursor = self.connectdb()
        cursor.execute("SELECT * FROM categories;")
        rows = cursor.fetchall()
        conn.close()

        lst = []
        for cat in rows:
            temp = Categorie(cat[0], cat[1], cat[2])
            lst.append(temp)

        return lst

    def filter(self, id="", name="", nbr_products=""):

        query = "SELECT * FROM categories where "
        need_coma = False


        if id != "":
            id = str(id)
            str_id = "id=\"{}\"".format(id)
            query += str_id
            need_coma = True

        if name != "":

            if need_coma == True:
                query += ", "
                need_coma = False

            str_name = "name=\"{}\"".format(name)
            query += str_name
            need_coma = True

        if nbr_products != "":
            nbr_products = str(nbr_products)

            if need_coma == True:
                query += ", "

            str_nbr = "nbr=\"{}\"".format(nbr_products)
            query += str_nbr

        query += ";"

        conn, cursor = self.connectdb()
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()

        results = []
        for row in rows:
            cat = Categorie(row[0], row[1], row[2])
            results.append(cat)

        return results


class Substitutes(Table):
    pass


class ORM():

    def __init__(self):
        self.products       = Products("products")
        self.categories     = Categories("categories")
        self.substitutes    = Substitutes("substitutes")


DB = ORM()
DB.products.get(cat="Snacks", grade_scale="A-C")
DB.products.add(row)

DB.categories.add(cat_tag)
DB.categories.list

DB.substitutes.get("all")