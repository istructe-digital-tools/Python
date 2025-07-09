import logging
from Settings import DesignValue, DesignFactor, DesignEquation
from EC0.Glossary import Glossary
"""
Implements Equation (8.1) from BS EN 1990:2023, Clause 8.3.1 (1):

E_d <= R_d

Inputs:
	E_d (DesignValue): Design value of the effect of actions with abbreviation 'E_{d}'
	R_d   (DesignValue) : Design value of the corresponding resistance with abbreviation 'R_{d}'

Output:
	Utilisation (DesignFactor): Decimal value representing E_d / R_d
"""

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Eq8_1(DesignEquation):
	standard = "BS EN 1990:2023"
	section = "8 Verification by the partial factor method"
	subsection = "8.3.1 Verification of ultimate limit states (ULS) - General"
	clause = "(1)"
	equation = "(8.1)"
	formula = "E_{d} <= R_{d}"

	def __init__(self, E_d: DesignValue, R_d: DesignValue):
		# Input validation
		if not isinstance(E_d, DesignValue):
			raise TypeError(
				f"Argument 'E_d' must be of type DesignValue, not {type(E_d).__name__}."
			)
		if not isinstance(R_d, DesignValue):
			raise TypeError(
				f"Argument 'R_{d}' must be of type DesignValue, not {type(E_d).__name__}."
			)
		if E_d.abbreviation != "E_{d}":
			raise ValueError(
				f"Argument 'E_d' must have abbreviation 'E_d'; got '{E_d.abbreviation}'."
			)
		if R_d.abbreviation != "R_{d}":
			raise ValueError("Argument 'R_{d}' must have abbreviation 'R_{d}'")

		# Log validated inputs
		logger.debug(
			f"Eq8_1 input: {E_d:value}, {R_d:value}")

		# Pre-Calculation Unit Conversion
		R_d_out = R_d.Units(E_d.units) 
		
		# Core calculation
		number = E_d.number / R_d_out.number

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
		self.R_d = R_d_out
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
