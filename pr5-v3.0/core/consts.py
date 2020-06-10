################### API ##########################################
OFF_URL = "http://fr.openfoodfacts.org/"    #Base Url for Open Food Fact API
SEARCH_URL = OFF_URL + "cgi/search.pl?"     #Url for research API
HEADERS = {"UserAgent": "PyBeurre - ubuntu-18.04 - Version 1.1"}    #headers for our app

MAX_TAGS = 3        #max categories to dump
MAX_ITEM_BC = 40    #max products by categories to dump

################## DB ############################################

USER_NAME   =   "neltarim"
HOST_ADRESS =   "localhost"
PWD         =   "usertest"
DB_NAME     =   "purbeurredb_orm"
COUNTRY     =   "France"

lvl_values = ['low', 'moderate', 'high']


if __name__ == "__main__":
    print("ERROR:const.py: This is a constants file. Don't use it as main program.")
    exit(0)