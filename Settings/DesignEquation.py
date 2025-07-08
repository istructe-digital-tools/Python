from dataclasses import dataclass
from Settings import DesignValue, DesignFactor


class DesignEquation(object):
	standard: str
	section: str
	subsection: str
	clause: str
	equation: str

		
	def __format__(self, format_spec):
        if format_spec == "short":
            return self.parameters()

	def _getEquationParameters(self):
		#Returns a list of explicitly defined objects that are of type DesignFactor or DesignValue.
		exclude = {"standard", "section", "subsection", "clause", "equation"}

		# Get all instance attributes excluding defaults and retrieve their values
		parameters = [
		    getattr(self, key) for key in vars(self).keys()
		    if key not in exclude and isinstance(getattr(self, key), (DesignFactor,
		                                                              DesignValue))
		]
		return parameters

	def reference(self, equation) -> str:
		output = self.standard + ":\n  "
		output += "Section: " + self.section + "\n  "
		output += "Subsection: " + self.subsection + "\n  "
		output += "Clause: " + self.clause + "\n  "
		output += "Equation: " + self.equation + "\n  "
		output += "Where:\n"

		parameters = self._getEquationParameters()
		for parameter in parameters:
			output += "    " + parameter.abbreviation + ", " + parameter.description + "\n"
		output += "  "
		output += self.parameters()
		return output
		
    def parameters(self) -> str:
		output = "Parameters:\n"
		output += "    " + equation + "\n"
		for parameter in parameters:
			if isinstance(parameter, DesignEquation):
				output += "    " + f"{parameter:value}"
			else:
				output += "    " + str(parameter)
			output += "\n"
		return output