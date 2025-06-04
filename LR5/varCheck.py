G = 42
N= 18

def get_variant_number():
    return (int(str(G) + str(N))%26)+1

def print_variant_number():
    print("Номер залікової книжки:",int(str(G)+str(N)))
    print("Мій варіант:",get_variant_number())

def get_NZK():
    return (int(str(G) + str(N)))

if __name__ == "__main__":
    print_variant_number()