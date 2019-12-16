import copy
import unittest

from navigation.orbit_map import OrbitMap, Body, OrbitMapLoader


def create_test_orbit_map():
    orbit_map = OrbitMap()
    system = orbit_map.add_system('COM')
    b = system.add_satellite('B')
    b.add_satellite('G').add_satellite('H')
    d = b.add_satellite('C').add_satellite('D')
    d.add_satellite('I')
    e = d.add_satellite('E')
    e.add_satellite('F')
    e.add_satellite('J').add_satellite('K').add_satellite('L')
    return orbit_map


class OrbitCountTests(unittest.TestCase):
    def test_counts_empty_map(self):
        orbit_map = OrbitMap()

        self.assertEqual(0, orbit_map.count_orbits())

    def test_counts_empty_system(self):
        orbit_map = OrbitMap()
        orbit_map.add_system('COM')

        self.assertEqual(0, orbit_map.count_orbits())

    def test_counts_direct_orbits(self):
        orbit_map = OrbitMap()
        system = orbit_map.add_system('COM')
        system.add_satellite('A')
        system.add_satellite('B')
        system.add_satellite('C')

        self.assertEqual(3, orbit_map.count_orbits())

    def test_counts_indirect_orbits(self):
        orbit_map = OrbitMap()
        orbit_map.add_system('COM').add_satellite('S').add_satellite('P').add_satellite('M')

        self.assertEqual(6, orbit_map.count_orbits())

    def test_counts_more_indirect_orbits(self):
        orbit_map = OrbitMap()
        orbit_map.add_system('COM').add_satellite('1').add_satellite('2')\
            .add_satellite('3').add_satellite('4').add_satellite('5')

        self.assertEqual(15, orbit_map.count_orbits())

    def test_counts_orbits_multiple_systems(self):
        orbit_map = OrbitMap()
        system1 = orbit_map.add_system('COM1')
        system1.add_satellite('A')
        system1.add_satellite('B')
        orbit_map.add_system('COM2').add_satellite('C').add_satellite('D')

        self.assertEqual(5, orbit_map.count_orbits())

    def test_counts_orbit_hierarchy(self):
        orbit_map = create_test_orbit_map()

        self.assertEqual(42, orbit_map.count_orbits())


class OrbitMapLoaderTests(unittest.TestCase):
    def test_loads_empty_map(self):
        loader = OrbitMapLoader()
        orbit_map = loader.load([])

        self.assertEqual(0, len(orbit_map._systems))

    def test_loads_tree_map(self):
        loader = OrbitMapLoader()
        orbit_map = loader.load(['COM)A', 'A)B', 'B)C', 'G)H', 'C)D', 'B)E'])

        self.assertEqual(2, len(orbit_map._systems))
        self.assertEqual(['A'], orbit_map.find_body('COM').get_satellite_names())
        self.assertEqual(['B'], orbit_map.find_body('A').get_satellite_names())
        self.assertEqual(['C', 'E'], orbit_map.find_body('B').get_satellite_names())
        self.assertEqual(['D'], orbit_map.find_body('C').get_satellite_names())
        self.assertEqual(['H'], orbit_map.find_body('G').get_satellite_names())

    def test_ignores_line_end(self):
        loader = OrbitMapLoader()
        orbit_map = loader.load(['A)B\n', 'B)C\n'])

        self.assertEqual(['B'], orbit_map.find_body('A').get_satellite_names())
        self.assertEqual(['C'], orbit_map.find_body('B').get_satellite_names())

    def test_loads_out_of_order(self):
        loader = OrbitMapLoader()
        orbit_map = loader.load(['B)C', 'A)B'])

        a = orbit_map.find_body('A')
        self.assertEqual(None, a.get_orbit_center())
        self.assertEqual(0, a.get_orbit_depth())
        self.assertEqual(['B'], a.get_satellite_names())
        b = a.find_body('B')
        self.assertEqual(a, b.get_orbit_center())
        self.assertEqual(1, b.get_orbit_depth())
        self.assertEqual(['C'], b.get_satellite_names())
        c = b.find_body('C')
        self.assertEqual(b, c.get_orbit_center())
        self.assertEqual(2, c.get_orbit_depth())
        self.assertEqual([], c.get_satellite_names())


class OrbitalTransferTests(unittest.TestCase):
    def test_transfer_one_up(self):
        orbit_map = OrbitMap()
        top = orbit_map.add_system('TOP')
        start = top.add_satellite('DOWN').add_satellite('START')
        target = top.add_satellite('TARGET')

        transfer_count = orbit_map.transfer('START', 'TARGET')

        self.assertEqual(1, transfer_count)
        self.assertEqual(target.get_orbit_center(), start.get_orbit_center())

    def test_transfer_one_down(self):
        orbit_map = OrbitMap()
        top = orbit_map.add_system('TOP')
        down = top.add_satellite('DOWN')
        target = down.add_satellite('TARGET')
        start = top.add_satellite('START')

        transfer_count = orbit_map.transfer('START', 'TARGET')

        self.assertEqual(1, transfer_count)
        self.assertEqual(target.get_orbit_center(), start.get_orbit_center())

    def test_transfer_sideways(self):
        orbit_map = OrbitMap()
        system = orbit_map.add_system('SYSTEM')
        start = system.add_satellite('LEFT').add_satellite('START')
        target = system.add_satellite('RIGHT').add_satellite('TARGET')

        transfer_count = orbit_map.transfer('START', 'TARGET')

        self.assertEqual(2, transfer_count)
        self.assertEqual(target.get_orbit_center(), start.get_orbit_center())

    def test_transfer_up_and_down(self):
        orbit_map = OrbitMap()
        system = orbit_map.add_system('SYSTEM')
        start = system.add_satellite('LEFT1').add_satellite('LEFT2').add_satellite('LEFT3').add_satellite('START')
        target = system.add_satellite('RIGHT1').add_satellite('RIGHT2').add_satellite('RIGHT3').add_satellite('TARGET')

        transfer_count = orbit_map.transfer('START', 'TARGET')

        self.assertEqual(6, transfer_count)

    def test_transfer(self):
        orbit_map = create_test_orbit_map()
        start = orbit_map.find_body('I').add_satellite('SAN')
        target = orbit_map.find_body('K').add_satellite('YOU')

        transfer_count = orbit_map.transfer('YOU', 'SAN')

        self.assertEqual(4, transfer_count)
        self.assertEqual(target.get_orbit_center(), start.get_orbit_center())


if __name__ == '__main__':
    unittest.main()
