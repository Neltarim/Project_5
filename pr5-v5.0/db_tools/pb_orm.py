import mysql.connector

from db_tools.mysql_tools import execute_query, sub_cats_to_list
from off_api.reach_engine import OffAPI


class Categorie():

    def __init__(self):
        self.id   = None
        self.name = None

class Product():
    def __init__(self):
        self.id                 = None
        self.generic_name       = None
        self.categorie          = None
        self.image_url          = None
        self.nutrition_grade    = None

        self.subs               = None
        self.sim_subs_score     = None

class ORM():
    """ ORM for accesssing to the purbeurre database """

    def __init__(self):
        self.api = OffAPI()
        self.api.test_connectivity()
        self.integrity_check()


    def integrity_check(self):
        """ Check if the database exist """

        print("Integrity check.")
        rows = execute_query("SHOW DATABASES;", fetch=True, no_db=True)
        db_exist = False

        for row in rows:

            if row[0] != 'purbeurre_db':
                pass

            else:
                db_exist = True
        
        if db_exist == False:

            print("Creating database ...")
            self.create()

            rows = execute_query("SELECT * FROM products", fetch=True)

            if rows == []:
                self.auto_fill()


    def create(self):
        """ Start the MYSQL script used to create the DB """

        execute_query("CREATE DATABASE IF NOT EXISTS purbeurre_db;", no_db=True)

        print("Database created.")

        execute_query("""
        CREATE TABLE IF NOT EXISTS `purbeurre_db`.`products` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `generic_name` VARCHAR(200) NOT NULL,
            `dumped_from` VARCHAR(200) NOT NULL,
            `image_url` VARCHAR(200) NULL,
            `nutrition_grade` CHAR(1) NOT NULL,
            PRIMARY KEY (`id`));

        CREATE TABLE IF NOT EXISTS `purbeurre_db`.`substitutions` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `primary_prod_rel` INT NOT NULL,
            `final_prod_rel` INT NOT NULL,
            PRIMARY KEY (`id`, `primary_prod_rel`),
            INDEX `fk_prime_prod_idx` (`primary_prod_rel` ASC),
            INDEX `fk_sub_prod_idx` (`final_prod_rel` ASC),
            CONSTRAINT `fk_prime_prod`
                FOREIGN KEY (`primary_prod_rel`)
                REFERENCES `purbeurre_db`.`products` (`id`)
                ON DELETE CASCADE
                ON UPDATE NO ACTION,
            CONSTRAINT `fk_sub_prod`
                FOREIGN KEY (`final_prod_rel`)
                REFERENCES `purbeurre_db`.`products` (`id`)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);

        CREATE TABLE IF NOT EXISTS `purbeurre_db`.`categories_dumped` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `cat_name` VARCHAR(95) NOT NULL,
            PRIMARY KEY (`id`));

        CREATE TABLE IF NOT EXISTS `purbeurre_db`.`sub_cats` (
            `id` INT NOT NULL AUTO_INCREMENT,
            `prod_rel_id` INT NOT NULL,
            `cat_name` VARCHAR(95) NOT NULL,
            PRIMARY KEY (`id`, `prod_rel_id`),
            INDEX `fk_prod_idx` (`prod_rel_id` ASC),
            CONSTRAINT `fk_prod`
                FOREIGN KEY (`prod_rel_id`)
                REFERENCES `purbeurre_db`.`products` (`id`)
                ON DELETE CASCADE
                ON UPDATE NO ACTION);
        """)

        print("Tables created.")


    def auto_fill(self):
        
        print("filling database ...")
        tags = self.api.dump_tags()

        for tag in tags:
            print("Dumping {} ...".format(tag))
            self.add_cat(tag)
        
        print("database filled.")


    def add_cat(self, cat_name):
        """ Add the data dumped from OFF api to the DB """

        prods = self.api.dump_cat(cat_name) #dump

        for prod in prods :

            query = """
            INSERT INTO purbeurre_db.products(generic_name, dumped_from, image_url, nutrition_grade)
            VALUES(%(generic_name)s, %(categorie)s, %(image_url)s, %(nutrition_grade)s);
            """
            execute_query(query, payload=prod, commit=True)
        
            formatted = sub_cats_to_list(prod['sub_cats'])

            for sub in formatted:

                sub_query = """
                INSERT INTO sub_cats(prod_rel_id, cat_name)
                VALUES(
                    (SELECT id FROM products WHERE generic_name='{}'),
                    '{}');""".format(prod['generic_name'], sub)

                execute_query(sub_query, commit=True, no_except=True)

        query = """INSERT INTO categories_dumped(cat_name)
                    VALUES(%(cat_name)s);"""
        payload = {
            "cat_name" : cat_name,
        }
        execute_query(query, payload=payload, commit=True)
        print("categorie {} added.".format(cat_name))

    def del_cat(self, cat_name):
        """ Delete a categorie """

        payload = {"cat_name" : cat_name}
        query = "SELECT id FROM products WHERE dumped_from=%(cat_name)s;"
        prods_to_delete = execute_query(query, payload=payload, fetch=True)

        for prod in prods_to_delete:
            id = prod[0]
            execute_query("DELETE FROM products WHERE id={};".format(id), commit=True)

        query = "DELETE FROM categories_dumped WHERE cat_name=%(cat_name)s;"
        execute_query(query, payload=payload, commit=True)

    def get_all_cats(self):
        """ Return all categories dumped """

        cats = execute_query("SELECT * FROM categories_dumped;", fetch=True)
    
        lst = []

        for cat in cats:
            temp = Categorie()
            
            temp.id = cat[0]
            temp.name = cat[1]

            lst.append(temp)

        return lst

    def prod_transform_obj(self, prod_wild):
        prod = Product()

        prod.id              = prod_wild[0]
        prod.generic_name    = prod_wild[1]
        prod.categorie       = prod_wild[2]
        prod.image_url       = prod_wild[3]
        prod.nutrition_grade = prod_wild[4]

        return prod

    def get_all_by_cat(self, cat_name):
        """ Return all products from a categorie """

        query = "SELECT * FROM products WHERE dumped_from=%(cat_name)s;"
        payload = {
            "cat_name" : cat_name
        }
        prods = execute_query(query, payload=payload, fetch=True)
        lst = []

        for prod in prods:
            temp = self.prod_transform_obj(prod)
            lst.append(temp)

        return lst

    def subs_compare(self, prime_prod, sub_prod):
        score = 0

        for sub_p in prime_prod.subs:
            for sub_s in sub_prod.subs:
                if sub_p == sub_s:
                    score += 1

        return score

    def substitute(self, primary_prod):
        """ Select the best substitute for a product """
        payload = {
            "prime_rel_id" : primary_prod.id,
            "cat_to_scrap" : primary_prod.categorie
        }
        gsub_query = "SELECT cat_name FROM sub_cats WHERE prod_rel_id=%(prime_rel_id)s;"
        primary_prod.subs = execute_query(gsub_query, payload=payload, fetch=True)

        query = "SELECT * FROM products WHERE dumped_from=%(cat_to_scrap)s;"
        rows = execute_query(query, payload=payload, fetch=True)
        
        similars_prods = []
        for row in rows:
            prod = self.prod_transform_obj(row)
            similars_prods.append(prod)

        bis = primary_prod
        bis.sim_subs_score = 0

        for prod in similars_prods:
            
            if prod.nutrition_grade < bis.nutrition_grade:
                prod.subs = execute_query(gsub_query, payload=payload, fetch=True)
                prod.sim_subs_score = self.subs_compare(primary_prod, prod)
                
                if prod.sim_subs_score > bis.sim_subs_score:
                    bis = prod

        query = """INSERT INTO substitutions (primary_prod_rel, final_prod_rel)
                    VALUES (
                        (SELECT id FROM products WHERE id=%(prime)s),
                        (SELECT id FROM products WHERE id=%(final)s)
                        );"""
        payload['prime'] = primary_prod.id
        payload['final'] = bis.id
        execute_query(query, payload=payload, commit=True)

        return bis

    def get_substitutions(self):
        
        query = """SELECT * FROM substitutions;"""
        subs = execute_query(query, fetch=True)

        form = []

        for sub in subs:
            temp_lst = []

            payload = {
                'id' : sub[1],
                'id2': sub[2],
            }
            query = "SELECT * FROM products WHERE id=%(id)s;"
            query2 = "SELECT * FROM products WHERE id=%(id2)s;"
            pr_wild = execute_query(query, payload=payload, fetch=True)
            pr2_wild = execute_query(query2, payload=payload, fetch=True)

            temp_prod = self.prod_transform_obj(pr_wild[0])
            temp_prod2 = self.prod_transform_obj(pr2_wild[0])
            temp_lst.append(temp_prod)
            temp_lst.append(temp_prod2)

            form.append(temp_lst)

        return form