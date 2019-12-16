from navigation.orbit_map import OrbitMapLoader

loader = OrbitMapLoader()

orbit_map = loader.load(open('orbitmap.txt', 'r'))

print("Loaded map with {} orbits".format(orbit_map.count_orbits()))

transfer_count = orbit_map.transfer('YOU', 'SAN')

print("Transferred {} orbits from YOU to SAN".format(transfer_count))
