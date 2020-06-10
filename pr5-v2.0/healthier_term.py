from core.db import Purbeurre_db

class main():
    """ Main loop program """
    def __init__(self):
        self.DB = Purbeurre_db() #interface with the local database
        self.loop = True
        
        while self.loop == True:
            self.menu() #loop menu


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

    def clear_screen(self):
        """ Clear the terminal """
        print("\n" * 100)

    def wait(self):
        """ Press ENTER to continue """
        input("press \"ENTER\" to continue ...")

    def crawl_tags(self, option):
        """ select a tag """
        self.clear_screen()
        tags = self.DB.get_tags()
        cat = None

        i = 1
        for tag in tags:
            print("{}. {}".format(i, tag))
            i += 1

        res = input("Wich categorie you want to {}? :".format(option))

        x = 1
        for tag in tags:
            if int(res) == x:
                cat = tag
                break
            else:
                x += 1

        if option == "delete":
            confirm = input("Confirm suppression of {}? (yes/no) :".format(cat))
            if confirm != "yes":
                print("Cancelled.")
                self.crawl_tags(option)
            
            else:
                self.DB.del_cat(cat)
                return 0

        return cat


    def del_cat(self):
        """ Call the del_cat method from DB """
        cat = self.crawl_tags("delete")
        self.DB.del_cat(cat)


    def add_cat(self):
        """ Call add_cat from DB """
        cat = input("Enter the categorie you want to add (exemple: \"snacks\") :")
        self.DB.add_cat(cat)

    def show_alliment(self, prod):
        """ Show all informations about a product in parameters """
        self.clear_screen()
        print("Name :" + prod['generic_name'] + "\n")
        print("Categories :" + prod['categories'] + "\n")


        print("Image link :" + prod['image_url'] + "\n")
        print("Nutrient levels :")

        for lvl in prod['nutrient_levels']:
            print("                 " + lvl + " :" + prod['nutrient_levels'][lvl])

        print("\n")
        self.wait()

    def open_cat(self):
        """ Open a categorie to choose what product to substitute """
        self.clear_screen()
        cat = self.crawl_tags("open")
        data_cat = self.DB.get_cat(cat)

        for prod in data_cat:
            print("{}. {}".format(prod['id'], prod['generic_name']))

        res = input("type the ID of the alliment you want to substitute :")
        self.clear_screen()
        selected = data_cat[int(res)]

        if res == None:
            print("Invalid argument. please try again.")
            self.clear_screen()
            self.open_cat()

        else:
            self.show_alliment(selected)
            sub = self.DB.substitute(cat, selected)
            self.wait()


if __name__ == "__main__":
    program = main()