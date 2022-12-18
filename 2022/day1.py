from functools import reduce

def get_sum(input_list):
    return reduce(lambda x, y: x + y, input_list)

all_elves_data = []
current_elf_data = []

with open('input1.txt') as f:
    for line in f.readlines():
        caloricity = line.rstrip()
        if caloricity:
            current_elf_data.append(int(caloricity))
        else:
            all_elves_data.append(get_sum(current_elf_data))
            current_elf_data = []

sorted_caloricities = sorted(all_elves_data, reverse=True)        
top_caloricities_sum = get_sum(sorted_caloricities[:3])
print(top_caloricities_sum)