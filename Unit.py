import math

# test


class Measurement(object):
    def __init__(self, _value: float, _rates: dict) -> None:
        self.rates = _rates
        self.value = _value

    def __eq__(self, other) -> bool:
        assert type(self) == type(other), "Attempted comparison across types."
        return self.value == other.value

    def __gt__(self, other) -> bool:
        assert type(self) == type(other), "Attempted comparison across types."
        return self.value > other.value

    def __lt__(self, other) -> bool:
        assert type(self) == type(other), "Attempted comparison across types."
        return self.value < other.value

    def __ge__(self, other) -> bool:
        assert type(self) == type(other), "Attempted comparison across types."
        return self.value >= other.value

    def __le__(self, other) -> bool:
        assert type(self) == type(other), "Attempted comparison across types."
        return self.value <= other.value

    def get_as(self, unit: str) -> float:
        return self.value / self.rates[unit.lower()]


class Angle(Measurement):
    # All angles are converted to radians on construction
    def __init__(self, _value: float, _unit: str) -> None:
        self.rates = {
            'radians': 1,
            'degrees': math.pi / 180,
            'gradians': math.pi / 200,
            'rotations':  2* math.pi
        }
        super().__init__(_value * self.rates[_unit.lower()], self.rates)

    def __add__(self, other):
        assert type(self) == type(other), "Attempted addition across types."
        return Angle(self.get_as("radians") + other.get_as("radians"), "radians")

    def __sub__(self, other):
        assert type(self) == type(other), "Attempted subtraction across types."
        return Angle(self.get_as("radians") - other.get_as("radians"), "radians")


class Distance(Measurement):
    # All distances are converted to meters on construction
    def __init__(self, _value: float, _unit: str) -> None:
        self.rates = {
            'meters': 1,
            'feet': 1/3.280839895,
            'miles': 5280/3.280839895,
            'nautical miles': 1852,
            'inches': 1/3.280839895/12,
            'cubits': 0.4572
        }
        super().__init__(_value * self.rates[_unit.lower()], self.rates)

    def __add__(self, other):
        assert type(self) == type(other), "Attempted addition across types."
        return Distance(self.get_as("meters") + other.get_as("meters"), "meters")

    def __sub__(self, other):
        assert type(self) == type(other), "Attempted subtraction across types."
        return Distance(self.get_as("meters") - other.get_as("meters"), "meters")


class Duration(Measurement):
    # All durations are converted to seconds on construction
    def __init__(self, _value: float, _unit: str) -> None:
        self.rates = {
            'milliseconds': 1/1000,
            'seconds': 1,
            'minutes': 60,
            'fortnight': 1209600
        }
        super().__init__(_value * self.rates[_unit.lower()], self.rates)

    def __add__(self, other):
        assert type(self) == type(other), "Attempted addition across types."
        return Duration(self.get_as("seconds") + other.get_as("seconds"), "seconds")

    def __sub__(self, other):
        assert type(self) == type(other), "Attempted subtraction across types."
        return Duration(self.get_as("seconds") - other.get_as("seconds"), "seconds")

class Angular_Velocity(Measurement):
    def __init__(self, _value: float, _unit: str):
        self.rates = {
            'radians/second': 1,
            'degrees/second': math.pi/180,
            'gradians/second': math.pi/200,
            'rotations/second': 2*math.pi,
            'radians/minute': 1/60,
            'degrees/minute': math.pi/(180*60),
            'gradians/minute': math.pi/(200*60),
            'rotations/minute': 2*math.pi/60
        }
        super().__init__(_value * self.rates[_unit.lower()], self.rates)

    def __add__(self, other):
        assert type(self) == type(other), "Attempted addition across types."
        return Angular_Velocity(self.get_as("radians/second") + other.get_as("radians/second"), "radians/second")

    def __sub__(self, other):
        assert type(self) == type(other), "Attempted subtraction across types."
        return Angular_Velocity(self.get_as("radians/second") - other.get_as("radians/second"), "radians/second")


class Velocity(Measurement):
    def __init__(self, _value: float, _unit: str):
        self.rates = {
            'meters/second': 1,
            'feet/second': 1/3.280839895,
            'miles/second': 5280/3.280839895,
            'nautical miles/second': 1852,
            'inches/second': 1/3.280839895/12,
            'cubits/second': 0.4572,
            'meters/minute': 1 / 60,
            'feet/minute': 1 / 60 / 3.280839895,
            'miles/minute': 5280 / 60 / 3.280839895,
            'nautical miles/minute': 1852 / 60,
            'inches/minute': 1 / 60 / 3.280839895 / 12,
            'cubits/minute': 0.4572 / 60,
            'meters/fortnight': 1 / 1209600,
            'feet/fortnight': 1 / 1209600 / 3.280839895,
            'miles/fortnight': 5280 * 1209600 / 3.280839895,
            'nautical miles/fortnight': 1852 / 1209600,
            'inches/fortnight': 1 / 1209600 / 3.280839895 / 12,
            'cubits/fortnight': 0.4572 / 1209600
        }

        super().__init__(_value * self.rates[_unit.lower()], self.rates)

    def __add__(self, other):
        assert type(self) == type(other), "Attempted addition across types."
        return Velocity(self.get_as("meters/second") + other.get_as("meters/second"), "meters/second")

    def __sub__(self, other):
        assert type(self) == type(other), "Attempted subtraction across types."
        return Velocity(self.get_as("meters/second") - other.get_as("meters/second"), "meters/second")


class Mass(Measurement):
    def __init__(self, _value: float, _unit: str) -> None:
        self.rates = {
            'kilograms': 1,
            'pounds': 0.45359237,
            'grams': 0.001
        }
        super().__init__(_value * self.rates[_unit.lower()], self.rates)

    def __add__(self, other):
        assert type(self) == type(other), "Attempted comparison across types."
        return Mass(self.value + other.value, "kilograms")

    def __sub__(self, other):
        assert type(self) == type(other), "Attempted comparison across types."
        return Mass(self.value - other.value, "kilograms")


class GlobalPosition(object):
    def __init__(self, _longitude: Angle, _latitude: Angle) -> None:
        self.longitude = _longitude
        self.latitude = _latitude

    def __eq__(self, other):
        assert type(self) == type(other), "Attempted comparison across types."
        return self.longitude == other.longitude and self.latitude == other.latitude


class RelativePosition(object):
    def __init__(self, _system, _x: Distance, _y: Distance):
        self.system = _system
        self.x = _x
        self.y = _y

    def __eq__(self, other):
        return self.system == other.system and self.x == other.x and self.y == other.y

    # Uses the pythagorean theorem to calculate distance in meters.
    def distance_to(self, other) -> Distance:
        assert self.system == other.system
        return Distance(math.sqrt((self.x.get_as('meters') - other.x.get_as('meters')) * (self.x.get_as('meters') - other.x.get_as('meters')) +
                                  (self.y.get_as('meters') - other.y.get_as('meters')) * (self.y.get_as('meters') - other.y.get_as('meters'))), 'meters')


class CartesianSystem(object):
    def __init__(self, _center: GlobalPosition):
        self.center = _center

    def __eq__(self, other):
        return self.center == other.center

    def point(self, x: Distance, y: Distance) -> RelativePosition:
        return RelativePosition(self, x, y)
