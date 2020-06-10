def list_to_str(lst):
    """ Convert a list to a string """
    listToStr = ','.join([str(elem) for elem in lst]) #add every item in the string seperate with a coma
    return listToStr

def dict_to_str(dict):
    """ Convert a dictionary to a string """
    str1 = ""       #string to return
    column = ""     #name of the value
    value = " "

    for col in dict:
        column = ""
        value = " " #add a space before the value, to seperate name and value only
        column = col
        value += dict[col]
        str1 += column + value + "," #append the string with the name and the value like "name1 value1,"

    return str1 #dict formatted to a string

def str_to_list(str1):
    """ Convert a string to a list """
    lst = []    #list to return
    elem = ""   #temporary value
    
    for char in str1: #character by character
        if char != ",":
            elem += char #append the "word"

        else:
            lst.append(elem) #add the word to the list
            elem = "" #refresh the word

    return lst #string formatted to a list

def nutrient_to_dict(str1):
    """ Convert a nutrient_levels back to a dictionary """
    dest = { #We need to first establish a template of the dict
        "salt"          : None,
        "sugars"        : None,
        "saturated-fat" : None,
        "fat"           : None
    }
    word = "" #temporary word string
    column = "" #temporary column name

    for char in str1: #character by character
        if char != " " and char != ",":
            word += char #append the temp word with every letters before a space or a coma

        elif char == " ": #the space mean the end of the name so we save it
            column = word
            word = ""

        elif char == ",": #the coma mean the end of the value so we add all of it to the dict
            dest[column] = word
            word = ""
            column = ""

    return dest #string formatted to a dict

def cat_nbr(str1):
    """ Define the number of the categorie in the rel table """
    nbr = ""
    for char in str1:
        if char == 'c' or char == 'a' or char == 't':
            pass
        else:
            nbr += char

    return int(nbr)

def prod_score(prod):
    """ determine a score to a product with the nutrient levels """
    lvls = { #arbitrary score (I'm not dietist haha)
        "low" : 1,
        "moderate" : 2,
        "high" : 3
    }

    types = { #arbitrary again (still not)
        "salt" : 2,
        "sugars" : 2,
        "saturated-fat" : 4,
        "fat" : 3
    }

    score = 0

    for lvl in prod:
        if prod[lvl] != None: #Many products doesn't have all types of nutrients levels
            column = lvl
            value = prod[lvl]

            score += types[column] * lvls[value] #don't ask why a multiplication.

    return score

def is_similar(prod, sub):
    """ Verify if the two products in parameters are similar """
    match = 0 #if you ever used tinder in your life, you know what it mean

    for sub_cat in prod['categories']: #crawl all categories of the product
        for sub_cat2 in sub['categories']: #Compare with all the categories of the substitute
            if sub_cat == sub_cat2:
                print(sub_cat + " " + sub_cat2)
                match += 1

    if match >= 3:
        return True

    else:
        return False

def grade_to_int(grade):
    scale = {
        "a" : 1,
        "b" : 2,
        "c" : 3,
        "d" : 4,
        "e" : 5
    }

    result = scale[grade]
    return result

def int_to_grade(int_grade):

    scale = {
        "1" : "a",
        "2" : "b",
        "3" : "c",
        "4" : "d",
        "5" : "e"
    }

    result = scale[int_grade]
    return result