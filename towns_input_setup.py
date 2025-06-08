import csv

towns_list = []

for i in range(16):
    town_name = input(f'Enter name of town no.{i + 1}: ')
    price = input(f'Enter price of {town_name}: Rs ')
    rent = input(f'Enter rent of {town_name}: Rs ')
    towns_list.append([town_name, price, rent])

print(towns_list)

monopolyTownsFile = 'C:/Users/mevin/Documents/monopoly/towns.csv'

with open(monopolyTownsFile, 'w', newline='') as monopolyTowns_csv:
    csvwriter = csv.writer(monopolyTowns_csv)
    csvwriter.writerows(towns_list)
