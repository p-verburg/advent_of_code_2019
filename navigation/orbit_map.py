class Body:
    def __init__(self, name):
        self._name = name
        self._orbit_center = None
        self._orbit_depth = 0
        self._satellites = []

    def get_name(self):
        return self._name

    def get_orbit_center(self):
        return self._orbit_center

    def get_orbit_depth(self):
        return self._orbit_depth

    def get_satellite_names(self):
        return [body.get_name() for body in self._satellites]

    def add_satellite(self, satellite):
        if isinstance(satellite, str):
            satellite = Body(satellite)
        elif not isinstance(satellite, Body):
            raise ValueError()
        if satellite == self:
            raise ValueError()
        satellite._orbit_center = self
        satellite.update_orbit_depths()
        self._satellites.append(satellite)
        return satellite

    def update_orbit_depths(self):
        if self._orbit_center is None:
            self._orbit_depth = 0
        else:
            self._orbit_depth = self._orbit_center.get_orbit_depth() + 1
        for satellite in self._satellites:
            satellite.update_orbit_depths()

    def remove_satellite(self, satellite):
        if satellite in self._satellites:
            self._satellites.remove(satellite)
            satellite._orbit_center = None
            satellite.update_orbit_depths()

    def count_satellites(self):
        return len(self._satellites)

    def find_body(self, name):
        if self.get_name() == name:
            return self
        for satellite in self._satellites:
            body = satellite.find_body(name)
            if body is not None:
                return body
        return None

    def find_orbit_center(self, satellite_name):
        for satellite in self._satellites:
            if satellite.get_name() == satellite_name:
                return self
            center = satellite.find_orbit_center(satellite_name)
            if center is not None:
                return center
        return None

    def count_orbits(self, orbit_depth=0):
        orbit_count = 0
        for body in self._satellites:
            orbit_count += orbit_depth + 1 + body.count_orbits(orbit_depth + 1)
        return orbit_count


class OrbitMap:
    def __init__(self):
        self._systems = []

    def add_system(self, system_name):
        system = Body(system_name)
        self._systems.append(system)
        return system

    def move(self, system, center):
        self._systems.remove(system)
        center.add_satellite(system)

    def transfer(self, start_name, target_name):
        start_body = self.find_body(start_name)
        if start_body is None:
            return None
        start_center = start_body.get_orbit_center()
        if start_center is None:
            return None
        target_center = self.find_orbit_center(target_name)
        if target_center is None:
            return None

        transfer_steps = 0
        start_node = start_center;
        target_node = target_center;
        while start_node.get_orbit_depth() > target_node.get_orbit_depth():
            start_node = start_node.get_orbit_center()
            transfer_steps += 1
        while target_node.get_orbit_depth() > start_node.get_orbit_depth():
            target_node = target_node.get_orbit_center()
            transfer_steps += 1

        while start_node != target_node:
            if start_node.get_orbit_center() is None:
                return None
            start_node = start_node.get_orbit_center()
            target_node = target_node.get_orbit_center()
            transfer_steps += 2

        start_center.remove_satellite(start_body)
        target_center.add_satellite(start_body)
        return transfer_steps

    def count_orbits(self):
        orbit_count = 0
        for system in self._systems:
            orbit_count += system.count_orbits()
        return orbit_count

    def find_system(self, name):
        for system in self._systems:
            if system.get_name() == name:
                return system
        return None

    def find_body(self, name):
        for system in self._systems:
            body = system.find_body(name)
            if body is not None:
                return body
        return None

    def find_orbit_center(self, satellite_name):
        for system in self._systems:
            center = system.find_orbit_center(satellite_name)
            if center is not None:
                return center
        return None

    def contains(self, name):
        return self.find_body(name) is not None


class OrbitMapLoader:
    def __init__(self):
        self._orbit_map = OrbitMap()

    def get_center(self, center_name):
        body = self._orbit_map.find_body(center_name)
        if body is None:
            body = self._orbit_map.add_system(center_name)
        return body

    def load(self, file):
        self._orbit_map = OrbitMap()

        for line in file:
            center_name, satellite_name = line.strip().split(')')

            center = self.get_center(center_name)

            system = self._orbit_map.find_system(satellite_name)
            if system is not None:
                self._orbit_map.move(system, center)
            else:
                if self._orbit_map.contains(satellite_name):
                    raise ValueError()

                center.add_satellite(Body(satellite_name))

        return self._orbit_map
