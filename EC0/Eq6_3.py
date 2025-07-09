import logging
from Settings import DesignValue, DesignFactor, DesignEquation
from EC0.Glossary import Glossary
"""
Implements Equation (6.3) from BS EN 1990:2023, Clause 6.1.2.3 (3):

Q_{qper} = ψ₂ ⋅ Q_k

Inputs:
	psi_2 (DesignFactor): Combination factor ψ₂ with abbreviation 'psi_{2}'
	Q_k   (DesignValue) : Characteristic variable action Q_k with abbreviation 'Q_{k}'

Output:
	Q_qper (DesignValue): Quasi-permanent value of a variable action 'Q_{qper}'
"""

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Eq6_3(DesignEquation):
	standard = "BS EN 1990:2023"
	section = "6 Basic variables"
	subsection = "6.1.2.3 Variable actions"
	clause = "(3)"
	equation = "(6.3)"
	formula = "Q_{qper} = psi_{2} * Q_{k}"

	def __init__(self, psi_2: DesignFactor, Q_k: DesignValue):
		# Input validation
		if not isinstance(psi_2, DesignFactor):
			raise TypeError(
				f"Argument 'psi_2' must be of type DesignFactor, not {type(psi_2).__name__}."
			)
		if not isinstance(Q_k, DesignValue):
			raise TypeError(
				f"Argument 'Q_k' must be of type DesignValue, not {type(psi_2).__name__}."
			)
		if psi_2.abbreviation != "psi_{2}":
			raise ValueError(
				f"Argument 'psi_2' must have abbreviation 'psi_2'; got '{psi_2.abbreviation}'."
			)
		if Q_k.abbreviation != "Q_{k}":
			raise ValueError("Argument 'Q_k' must have abbreviation 'Q_{k}'")

		# Log validated inputs
		logger.debug(
			f"Eq6_3 input: {psi_2:value}, {Q_k:value}")

		# Pre-Calculation Unit Conversion
		units = Q_k.units  #Inherits units from Q_k

		# Core calculation
		number = psi_2.number * Q_k.number

		# Encapsulate
		abbreviation = "Q_{qper}"
		name = Q_k.name
		Q_qper = DesignValue(abbreviation, number, units, name)

		# Post-Calcualtion Unit Conversion
		# No unit conversion required here

		# Log calculated result
		logger.debug(f"Eq6_3 result: {Q_qper:value}")

		# Store attributes
		self.psi_2 = psi_2
		self.Q_k = Q_k
		self.Q_qper = Q_qper

		# Add glossary definitions
		self = Glossary(self)

	# Forward attribute access to the calculated value
	def __getattr__(self, name):
		if hasattr(self.Q_qper, name):
			return getattr(self.Q_qper, name)
		raise AttributeError(
			f"{self.__class__.__name__} has no attribute '{name}'.")

	def __format__(self, format_spec):
		if format_spec == "value":
			return str(self.Q_qper)
		if format_spec == "short":
			return self.parameters()
		return str(self)

	# Printable string output
	def __str__(self):
		output = self.reference(self.formula)
		return output
