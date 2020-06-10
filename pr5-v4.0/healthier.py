from db_tools.pb_orm import ORM


class main():
    """ Main loop program """
    def __init__(self):
        self.orm = ORM()
        self.loop = True
        self.lines_to_clear = 100
        
        
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
        if res == "":
            print("Wrong argument.")
            self.pick_option(options) #restart recursively

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
            {'desc': 'Show substitutions',  'func': self.show_subs},
            {'desc': 'add a categorie',     'func': self.add_cat},
            {'desc': 'delete a categorie',  'func': self.del_cat},
            {'desc': 'quit',                'func': exit}
        ]
        self.pick_option(options)

####################################################################################



########################### DISPAY ENHANCEMENT #####################################

    def clear_screen(self):
        """ Clear the terminal """
        print("\n" * self.lines_to_clear)

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
        self.clear_screen()
        cats = self.orm.get_all_cats()

        nbr = 0
        for cat in cats:
            nbr += 1
            print("{} :{}".format(nbr, cat.name))

        choice = self.question("Pick a categorie to open ")
        choice = int(choice) - 1

        if choice < 0 or choice > nbr-1:
            print("wrong argument ...")
            self.wait()
            self.open_cat()

        self.clear_screen()

        prods = self.orm.get_all_by_cat(cats[choice].name)

        nbr = 0
        for prod in prods:
            nbr += 1
            print("{} :{}".format(nbr, prod.generic_name))

        choice = self.question("Pick a product to substitute ")
        choice = int(choice) - 1

        if choice < 0 or choice > nbr-1:
            print("wrong argument ...")
            self.wait()
            self.open_cat()

        self.clear_screen()

        primary_prod = prods[choice]

        sub = self.orm.substitute(primary_prod)

        print("PRIMARY PRODUCT : \n")
        print("         - Name : " + primary_prod.generic_name)
        print("         - Categorie : " + primary_prod.categorie)
        print("         - Image url : " + primary_prod.image_url)
        print("         - Nutri grade : " + primary_prod.nutrition_grade)
        
        print("\n\n SUBSTITUTION PRODUCT :\n")
        print("         - Name : " + sub.generic_name)
        print("         - Categorie : " + sub.categorie)
        print("         - Image url : " + sub.image_url)
        print("         - Nutri grade : " + sub.nutrition_grade)

        self.wait()

    def show_subs(self):
        subs = self.orm.get_substitutions()

        i = 0
        for sub in subs:
            i += 1
            prime = sub[0]
            final = sub[1]
            print("\n\n")
            print(str(i) + ".")
            print("     Primary : " + prime.generic_name)
            print("     Nutriscore : " + prime.nutrition_grade)
            print("\n    Substitute : " + final.generic_name)
            print("     Nutriscore : " + final.nutrition_grade)

        print()
        choice = self.question("Pick a substitution to see more ")
        choice = int(choice) - 1

        if choice < 0 or choice > i-1:
            print("wrong argument ...")
            self.wait()
            self.show_subs()

        sub_to_show = subs[choice]

        prime_prod = sub_to_show[0]
        sub_prod = sub_to_show[1]

        self.clear_screen()
        print("PRIMARY PRODUCT : \n")
        print("         - Name : " + primary_prod.generic_name)
        print("         - Categorie : " + primary_prod.categorie)
        print("         - Image url : " + primary_prod.image_url)
        print("         - Nutri grade : " + primary_prod.nutrition_grade)
        
        print("\n\n SUBSTITUTION PRODUCT :\n")
        print("         - Name : " + sub.generic_name)
        print("         - Categorie : " + sub.categorie)
        print("         - Image url : " + sub.image_url)
        print("         - Nutri grade : " + sub.nutrition_grade)

        self.wait()

    def add_cat(self):

        cat = self.question("New categorie name ")
        self.orm.add_cat(cat)
        self.wait()

    def del_cat(self):
        cats = self.orm.get_all_cats()

        nbr = 0
        for cat in cats:
            nbr += 1
            print("{} :{}".format(nbr, cat.name))

        choice = self.question("Pick a categorie to open ")
        choice = int(choice) - 1

        if choice < 0 or choice > nbr-1:
            print("wrong argument ...")
            self.wait()
            self.del_cat()

        cat = cats[choice]

        self.orm.del_cat(cat.name)
        print("{} Deleted successfuly.".format(cat.name))
        self.wait()
    
################################################################################


if __name__ == "__main__":
    program = main()
