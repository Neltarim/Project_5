from core.ORM.classes import ORM
from core.DB_fill.db_init import Purbeurre_db

class main():
    """ Main loop program """
    def __init__(self):
        self.db_fill = Purbeurre_db()
        self.orm = ORM()
        self.loop = True
        
        
        while self.loop == True:
            self.menu() #loop menu

########################## PRIMARY OPTIONS LAUNCHER ################################

    def pick_option(self, options):
        """ Start the function selected by the user from the list in parameters """
        self.clear_screen() #print 100 lines
        i = 1 #use to know what function to start
        for option in options:
            print("{}. {}".format(i, option['desc'])) #print the description and 'id' of all func
            i += 1

        res = input("Tap the number of the option you want to go :")
        res = int(res)
        res -= 1 #because a list start at 0, not 1

        if res <= i-1 and res >= 0:
            self.clear_screen()
            options[res]['func']() #call the function
        
        else:
            print("Wrong argument.")
            self.pick_option(options) #restart recursively


    def menu(self):
        """ Redirection function to pick option with options's payload """
        options = [
            {'desc': 'open a categorie',    'func': self.open_cat},
            {'desc': 'add a categorie',     'func': self.add_cat},
            {'desc': 'delete a categorie',  'func': self.del_cat},
            {'desc': 'quit',                'func': exit}
        ]
        self.pick_option(options)

####################################################################################



########################### DISPAY ENHANCEMENT #####################################

    def clear_screen(self):
        """ Clear the terminal """
        print("\n" * 100)

    def wait(self):
        """ Press ENTER to continue """
        input("press \"ENTER\" to continue ...")

    def question(self, str_to_print):

        str_to_print += " (\"quit\" to cancel) :"
        res = input(str_to_print)

        if res == "quit":
            self.menu()
        else:
            return res

################################################################################


########################### MENU METHODS #######################################
        
    def open_cat(self):
        i = 1
        for cat in self.orm.categories :
            print("{}: {}".format(i, cat.name))
            i += 1

        res = self.question("Pick the categorie you want")
        cat_to_open = self.orm.categories[res]

        prods = self.orm.get_cat_products(cat_code=cat_to_open.code)

        self.clear_screen()
        print("Categorie " + cat_to_open.name + " :")

        i = 1
        for prod in prods:
            print("{}: {}".format(i, prod.generic_name))
            i += 1

        res = self.question("Pick the alliment you want to substitute")

        prod_to_sub = prods[res]
        print(prod_to_sub.name + " DEBUG: PICKING IS WORKING.")
        #self.orm.substitute(prod_to_sub)


    def add_cat(self):
        print("NOT STARTED YET")
        self.wait()

    def del_cat(self):
        print("NOT STARTED YET")
        self.wait()
    
################################################################################


if __name__ == "__main__":
    program = main()
