from dataclasses import dataclass
from Settings.UnitConversion import UnitConversion

class DesignValueMeta(type):

	def __instancecheck__(cls, instance):
		return hasattr(instance, "abbreviation") and hasattr(
		    instance, "number") and hasattr(instance, "description") and hasattr(
		        instance, "units")


@dataclass
class DesignValue(metaclass=DesignValueMeta):
	abbreviation: str
	number: float
	units: str
	name: str = ""
	description: str = ""
	tolerance: float = 0
	upperLimit: float = 0
	lowerLimit: float = 0

	def __post_init__(self):
		if not isinstance(self.abbreviation, str):
			raise TypeError(
			    f"'abbreviation' must be a string, not {type(self.abbreviation).__name__}"
			)
		if not isinstance(self.number, (float, int)):
			raise TypeError(
			    f"'number' must be a float or int, not {type(self.number).__name__}")
		if not isinstance(self.units, str):
			raise TypeError(
			    f"'units' must be a string, not {type(self.units).__name__}")

		# Ensure ints are converted to floats
		self.number = float(self.number)

	def __str__(self):
		output = self.abbreviation
		if self.name != "":
			output = output.replace("}", "," + self.name + "}")
		return f"{output} = {str.format('{0:.4}', self.number)} [{self.units}]"

	def __format__(self, format_spec):
		return str(self)

	def Units(self, units: str):
		return UnitConversion(self, units)