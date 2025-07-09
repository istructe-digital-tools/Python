import logging
from Settings import DesignValue, DesignFactor, DesignEquation
from EC0.Glossary import Glossary
"""
Implements Equation (8.2) from BS EN 1990:2023, Clause 8.3.1 (1):

E_d <= C_d_ULS

Inputs:
	E_d (DesignValue): Design value of the effect of actions with abbreviation 'E_{d}'
	C_d_ULS   (DesignValue) : Design value of the corresponding resistance with abbreviation 'C_{d,ULS}'

Output:
	Utilisation (DesignFactor): Decimal value representing E_d / C_d_ULS
"""

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Eq8_2(DesignEquation):
	standard = "BS EN 1990:2023"
	section = "8 Verification by the partial factor method"
	subsection = "8.3.1 Verification of ultimate limit states (ULS) - General"
	clause = "(1)"
	equation = "(8.2)"
	formula = "E_{d} <= C_{d,ULS}"

	def __init__(self, E_d: DesignValue, C_d_ULS: DesignValue):
		# Input validation
		if not isinstance(E_d, DesignValue):
			raise TypeError(
				f"Argument 'E_d' must be of type DesignValue, not {type(E_d).__name__}."
			)
		if not isinstance(C_d_ULS, DesignValue):
			raise TypeError(
				f"Argument 'C_{d,ULS}' must be of type DesignValue, not {type(E_d).__name__}."
			)
		if E_d.abbreviation != "E_{d}":
			raise ValueError(
				f"Argument 'E_d' must have abbreviation 'E_d'; got '{E_d.abbreviation}'."
			)
		if C_d_ULS.abbreviation != "C_{d,ULS}":
			raise ValueError("Argument 'C_{d,ULS}' must have abbreviation 'C_{d,ULS}'")

		# Log validated inputs
		logger.debug(
			f"Eq8_1 input: {E_d:value}, {C_d_ULS:value}")

		# Pre-Calculation Unit Conversion
		C_d_ULS_out = C_d_ULS.Units(E_d.units) 
		
		# Core calculation
		number = E_d.number / C_d_ULS_out.number

		# Encapsulate
		abbreviation = "Utilisation"
		if number > 1.0:
			abbreviation += " [FAIL]"
		name = E_d.name
		utilisation = DesignFactor(abbreviation, number, name)
		

		# Post-Calcualtion Unit Conversion
		# No unit conversion required here

		# Log calculated result
		logger.debug(f"Eq6_3 result: {utilisation:value}")

		# Store attributes
		self.E_d = E_d
		self.C_d_ULS = C_d_ULS_out
		self.utilisation = utilisation

		# Add glossary definitions
		self = Glossary(self)

	# Forward attribute access to the calculated value
	def __getattr__(self, name):
		if hasattr(self.utilisation, name):
			return getattr(self.utilisation, name)
		raise AttributeError(
			f"{self.__class__.__name__} has no attribute '{name}'.")

	def __format__(self, format_spec):
		if format_spec == "value":
			return str(self.utilisation)
		if format_spec == "short":
			return self.parameters()
		return str(self)

	# Printable string output
	def __str__(self):
		output = self.reference(self.formula)
		return output
