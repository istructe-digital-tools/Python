import logging
import csv
import importlib.resources
import copy
from Settings import DesignValue

# Configure basic logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def UnitConversion(input: DesignValue, units: str) -> DesignValue: 
	factor = Factor(input.units) / Factor(units)
	output = copy.deepcopy(input)
	output.number = input.number * factor
	output.units = units
	logger.debug(
			f"{input.abbreviation} Conversion from {input.units} to {output.units} "
			f"factored by {factor}."
			)
			
	return output

def Dict(unit_type: str) -> dict:
    result = {}
    with importlib.resources.open_text('Settings', unit_type + 'Units.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip()
                value = float(row[1].strip())
                result[key] = value
    return result

def Factor(unit: str) -> float:
    for unit_type in ["force", "length"]:
        units_dict = Dict(unit_type)
        if unit in units_dict:
            return units_dict[unit]
    raise ValueError(f"Unit '{unit}' not found.")