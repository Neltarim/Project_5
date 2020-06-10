prods = [{"id": "12", "grade" : "A"}, {"id": "13", "grade": "C"}]



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

print(grade_to_int(prods[1]["grade"]))