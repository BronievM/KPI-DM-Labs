#для розрахунку варіанту
def calculate_var(group_fullnum, personal_num):
    return (group_fullnum+personal_num%60)%30+1

#деякі стандартні функції python, названі відповідними назвами
def union_python(a, b):
    return a | b

def intersection_python(a, b):
    return a & b

def difference_python(a, b):
    return a - b

#Для початкової функції
def calc_step1(a, b):
    return difference_python(a, b)

def calc_step2(a, b):
    return intersection_python(b, a)

def calc_step3(step1, step2):
    return union_python(step1, step2)

def calc_step4(c, b):
    return union_python(c, b)

def calc_step5(step3, step4):
    return difference_python(step3, step4)

def calculate_default_expression(a, b, c):
    step1 = calc_step1(a, b)
    yield step1
    step2 = calc_step2(a, b)
    yield step2
    step3 = calc_step3(step1, step2)
    yield step3
    step4 = calc_step4(c, b)
    yield step4
    yield calc_step5(step3, step4)

def calc_simplified_step1(c, b):
    return union_python(c, b)

def calc_simplified_step2(a, toDif):
    return difference_python(a, toDif)

def calculate_simplified_expression(a, b, c):
    step1 = calc_simplified_step1(c, b)
    yield step1
    yield calc_simplified_step2(a, step1)

# для вікна 4
def difference(a, b):
    result = set()
    for element in a:
        if element not in b:
            result.add(element)
    return result

def calculate_z(x, y):
    return difference(x, y)

#для вікна 5
def calculate_pythonized_z(x, y):
    return difference_python(x, y)