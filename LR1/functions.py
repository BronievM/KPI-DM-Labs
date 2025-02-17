def calculate_var(group_fullnum, personal_num):
    return (group_fullnum+personal_num%60)%30+1

def not_(a, universal):
    return universal.difference(a)

def union_python(a, b):
    return a | b

def intersection_python(a, b):
    return a & b

def difference_python(a, b):
    return a - b

def difference(a, b):
    result = set()
    for element in a:
        if element not in b:
            result.add(element)
    return result

def symmetric_difference(a, b):
    return a ^ b

def calc_step1():
    return 0

def calculate_z(x, y):
    return difference(x, y)