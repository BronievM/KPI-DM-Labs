G = 42
N= 18

def get_variant_number():
    return (int(str(G) + str(N))%10)+1

def print_variant_number():
    print("Номер залікової книжки:",G)
    print("Мій варіант:",get_variant_number())

print_variant_number()