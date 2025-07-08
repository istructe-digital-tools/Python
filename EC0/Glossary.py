import csv
import importlib.resources
from Settings import DesignEquation, DesignFactor, DesignValue

def Dict() -> dict:
    result = {}
    with importlib.resources.open_text('EC0', 'definitions.csv') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                key = row[0].strip()
                value = row[1].strip()
                result[key] = value
    return result

def Glossary(equation: DesignEquation) -> DesignEquation:
    definitions = Dict()  # Load once

    parameters = equation._getEquationParameters()
    for parameter in parameters:
        if isinstance(parameter, (DesignValue, DesignFactor)):
            if parameter.description == "":
                for prefix, definition in definitions.items():
                    if parameter.abbreviation.startswith(prefix[:-1]):
                        parameter.description = definition
                        break  # Stop after first match

    return equation
