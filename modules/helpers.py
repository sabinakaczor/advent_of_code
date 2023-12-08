def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def greatest_common_divisor(x, y):
    z = x % y if (x > y) else y % x
    if z == 0:
        return y if (x > y) else x
    return greatest_common_divisor(z, y) if x > y else greatest_common_divisor(z, x)

def lowest_common_multiple(x, y):
    return x * y // greatest_common_divisor(x, y)