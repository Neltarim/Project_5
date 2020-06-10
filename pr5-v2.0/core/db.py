import mysql.connector

from core.reach_api import OffAPI
from core.const import HOST_ADRESS, USER_NAME, PWD, DB_NAME
from core.div import *


class Purbeurre_db():
    """ Database interface """
    def __init__(self, mode="normal"):
        self.Api = OffAPI() #Module used to reach the Open Food Fact API
        
        if mode == "normal":
            self.tags = self.get_tags()
        elif mode == "install":
            self.create() #auto start the creation of the DB
            self.tags = None #will be set in the create method

    def connectdb(self):
        """ Connection to database """
        conn = mysql.connector.connect(host=HOST_ADRESS, user=USER_NAME, password=PWD, database=DB_NAME)
        return conn

    def istable(self, table):
        """ Verify the existence of the table in parameters """
        conn = self.connectdb()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES LIKE \'" + table + "\'")
        row = cursor.fetchall()
        conn.close()

        if row == []:
            return False
        elif row[0][0] == table:
            return True

    def get_tags(self):
        """ Return all tags in rel table """
        rows = self.get_rel()

        tags = []
        for row in rows:
            tags.append(row[1])

        return tags

    def create_table_cat(self, table_name):
        """ Create a new table for the categorie in parameters """
        if self.istable(table_name) != True:
            print("Creating table \"{}\" in {}".format(table_name, DB_NAME))
            conn = self.connectdb()
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS {} (
                id int(5) NOT NULL AUTO_INCREMENT,
                generic_name varchar(300) DEFAULT NULL,
                labels_hierarchy varchar(400) NOT NULL,
                image_url varchar(100),
                categories_hierarchy varchar(400) NOT NULL,
                categories varchar(600) NOT NULL,
                nutrient_levels varchar(500) NOT NULL,
                PRIMARY KEY(id)
            );
            """.format(table_name)) #Categorie table sample

            conn.commit()
            conn.close()
            
            print("table \"{}\" created.".format(table_name))
        
        else:
            print("Table " + table_name + " already exist.")

    def get_rel(self):
        """ Return all informations of all tables stocked in rel table """
        conn = self.connectdb()
        cursor = conn.cursor()
        cursor.execute("SELECT id, cat_name, cat_table FROM rel")
        rows = cursor.fetchall()

        conn.close()
        return rows

    def add_cat(self, tag):
        """" Add a new Categorie to the DB """
        rows = self.get_rel()

        i = 1
        for row in rows:
            print("ROW 2: {}".format(row[2]))
            nbr = cat_nbr(row[2])
            print(nbr)
            if i != nbr: #Verify that no table with this number exist
                break
            i += 1
        cat_table = "cat" + str(i) #Name of the new table (ex: cat12)
        payload = {"tag": tag, "cat_table": cat_table}
        
        conn = self.connectdb()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO rel (cat_name, cat_table) VALUES (%(tag)s, %(cat_table)s)""", payload)
        conn.commit() #Saving infos of the new table into rel

        self.create_table_cat(cat_table)
        products = self.Api.dump_cat(tag) #Dump all products of the categorie from API

        for prod in products: #Insert all products in the new table
            #we need first to convert lists and dicts to str before dump it to table
            labels_str = list_to_str(prod['labels_hierarchy'])
            cat_hierarchy_str = list_to_str(prod['categories_hierarchy'])
            nutrients_str = dict_to_str(prod['nutrient_levels'])
            
            payload = {
                "generic"   :   prod['generic_name'],
                "labels"    :   labels_str,
                "img"       :   prod['image_url'],
                "hierarchy" :   cat_hierarchy_str,
                "cats"      :   prod['categories'],
                "nutrients" :   nutrients_str
            }

            cursor.execute("""
                INSERT INTO {} (generic_name, labels_hierarchy, 
                image_url, categories_hierarchy, categories, nutrient_levels)
                VALUES (%(generic)s, %(labels)s, %(img)s, %(hierarchy)s, %(cats)s, %(nutrients)s);""".format(cat_table), payload)

        conn.commit() #insertion of the product
        conn.close()

    def del_cat(self, tag):
        """ Delete table and rel infos """
        rows = self.get_rel()
        rel_id = None

        for row in rows: #find the id and table name of the categorie
            if row[1] == tag:
                
                rel_id = row[0]
                cat_table = row[2]
            else:
                pass

        if rel_id == None: #in case of mistakes
            print("Categorie {} doesn't exist.".format(tag))
        
        else:
            conn = self.connectdb()
            cursor = conn.cursor()

            cursor.execute("DELETE FROM rel WHERE id={}".format(rel_id)) #delete the table in rel
            cursor.execute("DROP TABLE {}".format(cat_table)) #delete the table in DB
            cursor.close()
        

    def create_rel_table(self):
        """ Create the relationnal table in database """
        if self.istable("rel") == False: #verify that the rel table didn't already exist
            print("Creating table \"rel\" in {}".format(DB_NAME))
            conn = self.connectdb()
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rel (
                id int(5) NOT NULL AUTO_INCREMENT,
                cat_name varchar(50) NOT NULL,
                cat_table varchar(5) NOT NULL,
                PRIMARY KEY(id)
            );
            """)
            conn.commit()
            conn.close()
            
            print("table \"rel\" created.")
        
        else:
            print("Table \'rel\' already exist.")

        conn.close()

    def create(self):
        """ Initialisation of the database, used only at installation of the program """
        self.create_rel_table() #create the relational table
        self.tags = self.Api.dump_tags() #get the categories's tag from API
        
        for tag in self.tags:
            self.add_cat(tag) #add new table for every tag dumped


    def get_cat(self, tag):
        """ Dump all data of a categorie from database """
        rels = self.get_rel()
        selected = None

        for rel in rels: #get the id and real table name of the categorie
            if rel[1] == tag:
                selected = rel[2]
            else:
                pass

        if selected == None: #in case of mistakes
            print("{} not found.".format(tag))
            return 0

        else:
            conn = self.connectdb()
            cursor = conn.cursor()

            cursor.execute("SELECT * from {}".format(selected))
            rows = cursor.fetchall() #all products is here
            conn.close()

            products = [] #the real products list we're gonna return
            
            for row in rows:
                prod = {}
                #we need for some values to first convert them into list or dict
                prod['id']                      = row[0]
                prod['generic_name']            = row[1]
                prod['labels_hierarchy']        = str_to_list(row[2])
                prod['image_url']               = row[3]
                prod['categories_hierarchy']    = str_to_list(row[4])
                prod['categories']              = row[5]
                prod['nutrient_levels']         = nutrient_to_dict(row[6])

                products.append(prod)
                
        return products

    def substitute(self, cat, prod_to_sub):
        """ Find a better product """
        products = self.get_cat(cat) #dump the products of the categorie
        prod_s_s = prod_score(prod_to_sub['nutrient_levels']) #nutrition score for the first prod
        sub = None #final object to return

        for prod in products: #Compare all products in the cat with the initial product
            if prod['id'] != prod_to_sub['id']: #prevent to compare the same product
                sub_score = prod_score(prod['nutrient_levels']) #nutrition score of the compared product

                if sub_score < prod_s_s:
                    if is_similar(prod_to_sub, prod) == True: #Verify that the substitute is similar
                        sub = prod
                        break
        print(sub)
        return sub
        

if __name__ == "__main__":
    print("ERROR:reach_api.py: This is a class file. Don't use it as main program.")
    exit(0)