import random

female_names = ["Анастасія", "Аліса", "Ганна", "Галина", "Ірина", "Наталя", "Марія", "Ольга", "Тетяна", "Катерина", "Людмила", "Вікторія", "Софія", "Дарина", "Юлія"]
male_names = ["Андрій", "Богдан", "Євген", "Дмитро", "Степан", "Микола", "Олег", "Василь", "Роман", "Павло", "Іван", "Сергій", "Олександр", "Володимир", "Артем"]

set_a = set()
set_b = set()
cartesian_product = set()
s = set()
r = set()

#розрахунок варіанту
def calculate_var(group_fullnum, personal_num):
    return (group_fullnum + personal_num % 60) % 30 + 1

#декартовий добуток
def calculate_cartesian_product():
    if not set_a and not set_b:
        return
    cartesian_product.clear()
    for a in set_a:
        for b in set_b:
            cartesian_product.add((a, b))

#генерація відношення S => aSb a є мати b
def create_random_s():
    s.clear()
    calculate_cartesian_product()

    available_children = list(set_b)
    random.shuffle(available_children)
    mother_children = {mother: set() for mother in set_a if mother in female_names}
    for mother in mother_children:
        max_children = random.randint(0, 2)

        possible_children = [child for child in available_children
                             if (mother, child) in cartesian_product and child not in {c for i, c in s}]
        random.shuffle(possible_children)

        while possible_children and len(mother_children[mother]) < max_children:
            child = possible_children.pop()
            s.add((mother, child))
            mother_children[mother].add(child)
            available_children.remove(child)

#генерація відношення R => aRb a є онукою b
def create_random_r():
    r.clear()

    mother_of = {child: mother for mother, child in s}

    for grandchild, mother in mother_of.items():
        if mother in mother_of:
            grandparent = mother_of[mother]

            if grandchild in female_names and (grandchild, grandparent) in cartesian_product and (grandchild, grandparent) not in s:
                r.add((grandchild, grandparent))

    if len(r) < 2:
        potential_grandchildren = [name for name in set_a if name in female_names]
        potential_grandparents = list(set_b)

        random.shuffle(potential_grandchildren)
        random.shuffle(potential_grandparents)

        avg_pairs_per_grandchild = max(1, len(potential_grandparents) // len(potential_grandchildren))

        for grandchild in potential_grandchildren:
            num_pairs = max(2, random.randint(1, avg_pairs_per_grandchild))

            for i in range(num_pairs):
                if potential_grandparents:
                    grandparent = random.choice(potential_grandparents)
                    if (grandchild, grandparent) in cartesian_product and (grandchild, grandparent) not in s:
                        r.add((grandchild, grandparent))
                        potential_grandparents.remove(grandparent)

                if len(r) >= 2:
                    print(f"A: {set_a}")
                    print(f"B: {set_b}")
                    print(f"A*B: {cartesian_product}")
                    print(f"S: {s}")
                    print(f"R: {r}")
                    return

#для вікна 4
def get_union():
    return s | r

def get_intersection():
    return s & r

def get_difference():
    return r - s

def get_complement():
    return cartesian_product - r

def get_inverse():
    return {(b, a) for a, b in s}
