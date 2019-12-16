from engine.fuel_calculator import calculate_module_fuel

lines_read = 0
total_fuel = 0
f = open("ModuleMasses.txt", 'r')
for line in f:
    mass = int(line)
    fuel = calculate_module_fuel(mass)
    total_fuel += fuel
    lines_read += 1

print("Read % 2d lines" % lines_read)
print(total_fuel)