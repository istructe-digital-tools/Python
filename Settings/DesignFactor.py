from dataclasses import dataclass


class DesignFactorMeta(type):

	def __instancecheck__(cls, instance):
		return hasattr(
		    instance, "abbreviation") and hasattr(instance, "number") and hasattr(
		        instance, "description") and not hasattr(instance, "units")


@dataclass
class DesignFactor(metaclass=DesignFactorMeta):
	abbreviation: str
	number: float
	name: str = ""
	description: str = ""

	def __post_init__(self):
		if not isinstance(self.abbreviation, str):
			raise TypeError(
			    f"'abbreviation' must be a string, not {type(self.abbreviation).__name__}"
			)
		if not isinstance(self.number, (float, int)):
			raise TypeError(
			    f"'number' must be a float or int, not {type(self.number).__name__}")

		# Ensure ints are converted to floats
		self.number = float(self.number)

	def __str__(self):
		output = self.abbreviation
		if self.name != "":
			output = output.replace("}", "," + self.name + "}")
		return f"{output} = {str.format('{0:.3}', self.number)} []"

	def __format__(self, format_spec):
		return str(self)
