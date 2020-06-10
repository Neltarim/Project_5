import requests

from core.consts import *


class OffAPI():
    """ Reach the Open Food Fact API to dump all tags and categories """
    def __init__(self):
        #self.status_api = self.test_connectivity()
        self.max_tags = MAX_TAGS
        self.max_items_bc = MAX_ITEM_BC

    #####################ATTRIBUTES'S GET METHOD ######################

    #def get_status_api(self):
        #return self.status_api

    ###################################################################

    def test_connectivity(self):
        '''Test the connectivity with Open Food Facts's API'''
        res = requests.get(OFF_URL, headers=HEADERS)
        if res.status_code == requests.codes.ok:
            return True
        else:
            print("Open Food Facts's API is not currently available.")
            exit(0)

    def dump_tags(self):
        '''get categories tags from the URL API'''
        response = requests.get(OFF_URL + 'categories&json=1') #Reach the API
        data_json = response.json()
        data_tags = data_json.get('tags')
        wild_tags = [tag.get('name', 'None') for tag in data_tags] #get the name of all tags
        i = 0
        tags = []

        for cat in wild_tags:
            tags.append(cat)

            i += 1
            if i == self.max_tags: #save the maximum amount of tags
                break

        return tags

    def dump_cat(self, cat):
        '''Dump categorie from OFF's API'''
        payload = { #Most efficiency payload to dump a categorie
            'action': 'process',
            'tagtype_0': 'categories',
            'tag_contains_0': 'contains',
            'tag_0': cat,
            'sort_by': 'unique_scans_n',
            'page_size': self.max_items_bc, #number of items to download
            'countries': COUNTRY,
            'json': 1,
            'page': 1
        }

        response = requests.get(SEARCH_URL, params=payload)
        res = response.json()
        prods = res.get('products') #another method to get something from the request's row

        formatted = [] #Final version of the categorie
        i = 1 
        for prod in prods:
            try: #in order to reduce the amount of useless data in the products, we only save
                 # those attributes
                simplified = {
                'generic_name'          : prod['generic_name'],
                'categorie'             : prod['categorie'],
                'image_url'             : prod['image_url'],
                'sub_cats'              : prod['categories'],           #also sub categories (just in case)
                'nutrition_grade'       : prod['nutrition_grades']         #nutrient levels
                }

                if simplified['generic_name'] != '' or simplified['nutrition_grade'] != '': #avoid the products without name
                    formatted.append(simplified) #add to the product to the final list
                    i += 1

            except:
                pass

        print("total product for " + cat + " :" + str(i))
        return formatted #final list of products simplified


if __name__ == "__main__":
    print("ERROR:reach_api.py: This is a class file. Don't use it as main program.")
    exit(0)