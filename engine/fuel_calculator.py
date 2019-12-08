def calculate_module_fuel(module_mass):
    fuel_mass = module_mass // 3 - 2
    if fuel_mass <= 0:
        return 0
    return fuel_mass + calculate_module_fuel(fuel_mass)
