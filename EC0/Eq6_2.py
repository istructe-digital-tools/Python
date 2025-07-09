import logging
from Settings import DesignValue, DesignFactor, DesignEquation
from EC0.Glossary import Glossary
"""
Implements Equation (6.2) from BS EN 1990:2023, Clause 6.1.2.3 (3):

Q_{freq} = ψ₁ ⋅ Q_k

Inputs:
	psi_1 (DesignFactor): Combination factor ψ₁ with abbreviation 'psi_{1}'
	Q_k   (DesignValue) : Characteristic variable action Q_k with abbreviation 'Q_{k}'

Output:
	Q_freq (DesignValue): Frequent value of a variable action 'Q_{freq}'
"""

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Eq6_2(DesignEquation):
	standard = "BS EN 1990:2023"
	section = "6 Basic variables"
	subsection = "6.1.2.3 Variable actions"
	clause = "(3)"
	equation = "(6.2)"
	formula = "Q_{freq} = psi_{1} * Q_{k}"

	def __init__(self, psi_1: DesignFactor, Q_k: DesignValue):
		# Input validation
		if not isinstance(psi_1, DesignFactor):
			raise TypeError(
				f"Argument 'psi_1' must be of type DesignFactor, not {type(psi_1).__name__}."
			)
		if not isinstance(Q_k, DesignValue):
			raise TypeError(
				f"Argument 'Q_k' must be of type DesignValue, not {type(psi_1).__name__}."
			)
		if psi_1.abbreviation != "psi_{1}":
			raise ValueError(
				f"Argument 'psi_1' must have abbreviation 'psi_1'; got '{psi_1.abbreviation}'."
			)
		if Q_k.abbreviation != "Q_{k}":
			raise ValueError("Argument 'Q_k' must have abbreviation 'Q_{k}'")

		# Log validated inputs
		logger.debug(
			f"Eq6_2 input: {psi_1:value}, {Q_k:value}")

		# Pre-Calculation Unit Conversion
		units = Q_k.units  #Inherits units from Q_k

		# Core calculation
		number = psi_1.number * Q_k.number

		# Encapsulate
		abbreviation = "Q_{freq}"
		name = Q_k.name
		Q_freq = DesignValue(abbreviation, number, units, name)

		# Post-Calcualtion Unit Conversion
		# No unit conversion required here

		# Log calculated result
		logger.debug(f"Eq6_2 result: {Q_freq:value}")

		# Store attributes
		self.psi_1 = psi_1
		self.Q_k = Q_k
		self.Q_freq = Q_freq

		# Add glossary definitions
		self = Glossary(self)

	# Forward attribute access to the calculated value
	def __getattr__(self, name):
		if hasattr(self.Q_freq, name):
			return getattr(self.Q_freq, name)
		raise AttributeError(
			f"{self.__class__.__name__} has no attribute '{name}'.")

	def __format__(self, format_spec):
		if format_spec == "value":
			return str(self.Q_freq)
		if format_spec == "short":
			return self.parameters()
		return str(self)

	# Printable string output
	def __str__(self):
		output = self.reference(self.formula)
		return output
