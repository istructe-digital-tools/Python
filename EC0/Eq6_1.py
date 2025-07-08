import logging
from Settings import DesignValue, DesignFactor, DesignEquation
from EC0.Glossary import Glossary
"""
Implements Equation (6.1) from BS EN 1990:2023, Clause 6.1.2.3 (3):

Q_{comb} = ψ₀ ⋅ Q_k

Inputs:
	psi_0 (DesignFactor): Combination factor ψ₀ with abbreviation 'psi_{0}'
	Q_k   (DesignValue) : Characteristic variable action Q_k with abbreviation 'Q_{k}'

Output:
	Q_comb (DesignValue): Combined action value with abbreviation 'Q_{comb}'
"""
""" Principle 1: Document Code and Link to Standards
In our example it explicitly reference BS EN 1990:2023 and the clause/equation number. 
This makes the code self-explanatory and traceable to the exact standard equation 
being implemented. The metadata ensures any engineer (new or experienced) can verify 
the formula.
"""

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Eq6_1(DesignEquation):
	""" Principle 1: Document Code and Link to Standards
		Here we continue to capture information but this time in a machine readable format.
	"""
	standard = "BS EN 1990:2023"
	section = "6 Basic variables"
	subsection = "6.1.2.3 Variable actions"
	clause = "(3)"
	equation = "(6.1)"
	formula = "Q_{comb} = psi_{0} * Q_{k}"

	def __init__(self, psi_0: DesignFactor, Q_k: DesignValue):
		# Input validation
		""" Principle 2: Validate Inputs Early
			In this example, the function immediately checks that psi_0 is a DesignFactor 
			and Q_k a DesignValue, and that their abbreviations match the expected symbols. 
			These guards prevent nonsensical use (e.g. passing a length as a force) and 
			flag mistakes at once. 
			Input validation helps ensure that the data being processed is accurate and free 
			from errors, which is crucial in safety-critical calculations.
		"""
		if not isinstance(psi_0, DesignFactor):
			raise TypeError(
				f"Argument 'psi_0' must be of type DesignFactor, not {type(psi_0).__name__}."
			)
		if psi_0.abbreviation != "psi_{0}":
			raise ValueError(
				f"Argument 'psi_0' must have abbreviation 'psi_0'; got '{psi_0.abbreviation}'."
			)
		""" Principle 3: Use Meaningful Errors and Exceptions
			The code above raises explicit 'TypeError' or 'ValueError' with clear messages. 
			This makes debugging straightforward. 
			For a new engineer, a message like “must be of type DesignValue” pinpoints 
			the problem immediately. 
		"""
		if Q_k.abbreviation != "Q_{k}":
			raise ValueError("Argument 'Q_k' must have abbreviation 'Q_{k}'")

		# Log validated inputs
		""" Principle 4: Log Key Steps for Traceability 
			In this example, this function uses logger.debug to record both the validated inputs 
			and the final result.
		"""
		logger.debug(
			f"Eq6_1 input: psi_0=%s, Q_k=%s {psi_0:value}, {Q_k:value}")

		# Pre-Calculation Unit Conversion
		""" Principle 5: Enfore Unit Consistency
			This function does not require unit conversion. However, the here the output 
			units is inherited from the input units. Always keeping units consistent 
			across calculations is critical. Even a tiny oversight in unit consistency 
			can have catastrophic consequences in structural engineering.
		"""

		# Core calculation
		""" Principle 6: Implement the Math Clearly and Exactly
			In our example the script does this by literally coding 
			Q_comb = ψ₀ * Q_k. 
		
		"""
		number = psi_0.number * Q_k.number
		""" Principle 7: Encapsulate Outputs in Domain Classes
			Our example doesn’t just spit out a number. It returns a DesignValue object 
			that bundles the numerical result, its units, and a meaningful name "Q_{comb}" 
			together. 
			The code above shows creating Q_comb = DesignValue(abbreviation, number, units), 
			which means downstream code can rely on standard methods of DesignValue. 
			Using domain-specific classes like DesignValue ensures that all results carry 
			metadata for later checks or computations and provides consistency across 
			calculations.

		"""
		abbreviation = "Q_{comb}"
		units = Q_k.units  #Inherits units from Q_k
		name = Q_k.name
		Q_comb = DesignValue(abbreviation, number, units, name)

		# Post-Calcualtion Unit Conversion
		# No unit conversion required here

		# Log calculated result
		logger.debug(f"Eq6_1 result: Q_comb=%s{Q_comb:value}")

		# Store attributes
		self.psi_0 = psi_0
		self.Q_k = Q_k
		self.Q_comb = Q_comb

		# Add glossary definitions
		self = Glossary(self)

	# Forward attribute access to the calculated value
	""" Principle 8: Make it easier to get the right information
		Most people using this equation will do so like this:
		Load = Eq6_1(psi_0, Q_k) 
		
		The class’s use of __getattr__ to forward any attributes of the object 
		to Q_comb makes it easy to access the result for example if the script 
		was used. Without the __getattr__ the result would have to be accessed as:
		Load.Q_comb.number
		
		The __getattr__ the result can be access simple as:
		Load.number 
		
		The benefit of saving all the objects in the class is it makes tracability easier
		for example the user could check what 'Q_k' has been used to calculate 'Q_comb' by:
		Load.Q_k.number
	"""

	def __getattr__(self, name):
		if hasattr(self.Q_comb, name):
			return getattr(self.Q_comb, name)
		raise AttributeError(
			f"{self.__class__.__name__} has no attribute '{name}'.")

	def __format__(self, format_spec):
		if format_spec == "value":
			return str(self.Q_comb)
		if format_spec == "short":
			return self.parameters()
		return str(self)

	# Printable string output
	""" Principle 9: Provide a clear output interface
		Our example uses a custom __str__ method that inherits from the DesignCalculation class. 
		This so that printing the equation object always shows the equation with its values 
		and reference. This means an engineer can simply perform a print command and the output 
		would be printed consistently:
		
		print(Eq6_1(psi0, Qk))
		----
		
		BS EN 1990:2023:
		  Section 6: Basic variables
		  Subsection 6.1.2.3: Variable actions
		  Clause (3)
		  Equation (6.1):
		  Where:
			psi_{0}, Combination factor applied to a variable action to determine its combination value
			Q_{k}, Characteristic value of a variable action
			Q_{comb}, Combination value of a variable action
		  Solved:
			Q_{comb} = psi_{0} * Q_{k}
			psi_{0} = 0.7 []
			Q_{k} = 532.0 [kN]
			Q_{comb} = 372.4 [kN]

		The method provides consistency, if used on another equation the layout of the output would 
		be in the same format. 
	"""

	def __str__(self):
		output = self.reference(self.formula)
		return output
