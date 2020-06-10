import mysql.connector


def sub_cats_to_list(cats_str):

    lst = []
    cat = ""

    for char in cats_str:
        
        if char != ",":
            cat += char

        if char == ",":
            lst.append(cat)
            cat = ""

        else:
            pass

    lst.append(cat)
    return lst



def execute_query(query, fetch=False, commit=False, payload=None, no_except=False, no_db=False, msg=None):

    db_name = None

    if no_db == False:
        db_name = 'purbeurre_db'

    conn = mysql.connector.connect(
            host="localhost",
            user="neltarim",
            password="usertest",
            database=db_name
        )
    cursor = conn.cursor()

    try:
        if payload == None:
            cursor.execute(query)

        else:
            cursor.execute(query, payload)

    except:

        if no_except:
            pass

        else:
            print("ERROR: while executing this query :\n" + query)
            yn = input("\nType \"quit\" to leave or press ENTER to continue ...")

            if yn == "quit":
                quit(0)

            else:
                pass

    if fetch:
        rows = cursor.fetchall()
        conn.close()
        return rows
        
    if commit:
        conn.commit()
        
    conn.close()