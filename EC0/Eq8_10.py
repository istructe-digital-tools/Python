import logging
from os import name
from Settings import DesignValue, DesignFactor, DesignEquation
from EC0.Glossary import Glossary
"""
Implements Equation (8.10) from BS EN 1990:2023, Clause 8.3.3.3 (1):

Q_{d} = γ_Q ⋅ Q_{rep}

Inputs:
		gamma_Q (DesignFactor): Partial factor for variable action γ_Q with abbreviation 'gamma_{Q}'
		Q_comb  (DesignValue) : Representative variable action Q_{rep} with abbreviation starting with one of:
														'Q_{rep}', 'Q_{k}', 'Q_{comb}', 'Q_{freq}', or 'Q_{qper}'

Output:
		Q_d (DesignValue): Design value of the variable action with abbreviation 'Q_{d}'
"""

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Eq8_10(DesignEquation):
	#Principle 1: Document Code and Link to Standards
	standard = "BS EN 1990:2023"
	section = "8 Verification by the partial factor method"
	subsection = "8.3.3.3 Variable actions"
	clause = "(1)"
	equation = "(8.10)"
	formula = "Q_{d} = gamma_{Q} * Q_{rep}"

	def __init__(self, gamma_Q: DesignFactor, Q_comb: DesignValue):
		#Principle 2: Validate Inputs Early
		if not isinstance(gamma_Q, DesignFactor):
			raise TypeError(
			    f"Argument 'gamma_Q' must be of type DesignFactor, not {type(gamma_Q).__name__}."
			)
		#Principle 3: Use Meaningful Errors and Exceptions
		if gamma_Q.abbreviation != "gamma_{Q}":
			raise ValueError(
			    f"Argument 'gamma_Q' must have abbreviation 'gamma_{{Q}}'; got '{gamma_Q.abbreviation}'."
			)
		if not isinstance(Q_comb, DesignValue):
			raise TypeError(
			    f"Argument 'Q_comb' must be of type DesignValue, not {type(Q_comb).__name__}."
			)

		valid_prefixes = ("Q_{rep}", "Q_{k}", "Q_{comb}", "Q_{freq}", "Q_{qper}")
		if not Q_comb.abbreviation.startswith(valid_prefixes):
			raise ValueError(
			    f"Argument 'Q_comb' must start with one of {valid_prefixes}; got '{Q_comb.abbreviation}'."
			)

		#Principle 4: Log Key Steps for Traceability
		logger.debug(
		    f"Eq8_10 input: gamma_Q=%s, Q_comb=%s {gamma_Q:value}, {Q_comb:value}")

		#Principle 5: Enforce Unit Consistency
		#No unit conversion required

		#Principle 6: Implement the Math Clearly and Exactly
		number = gamma_Q.number * Q_comb.number

		#Principle 7: Encapsulate Outputs in Domain Classes
		abbreviation = "Q_{d}"
		units = Q_comb.units
		name = Q_comb.name
		Q_d = DesignValue(abbreviation, number, units, name)
		self.gamma_Q = gamma_Q
		self.Q_comb = Q_comb
		self.Q_d = Q_d

		self = Glossary(self)

		#Principle 4: Log Key Steps for Traceability
		logger.debug(f"Eq8_10 result: Q_d=%s{Q_d:value}")

	#Principle 8: Make it easier to get the right information
	def __getattr__(self, name):
		if hasattr(self.Q_d, name):
			return getattr(self.Q_d, name)
		raise AttributeError(
		    f"{self.__class__.__name__} has no attribute '{name}'.")

	def __format__(self, format_spec):
		if format_spec == "value":
			return str(self.Q_d)
		return str(self)

	#Principle 9: Provide a clear output interface
	def __str__(self):
		output = "Q_{d} = gamma_{Q} * Q_{rep} \n  "
		output += "As per clause 6.1.2.3(1): \n    "
		output += "Q_{d} = gamma_{Q} * " + self.Q_comb.abbreviation

		output = self.reference(output)
		return output
