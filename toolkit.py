from typing import Annotated, Literal, Dict, Any
from toolkitutils.math_toolkit import calculator, unified_calculator, get_available_operations, MathToolkit

def math_toolkit_wrapper(operation: str, params: Dict[str, Any]) -> Any:

    print(operation)
    """
    A strict wrapper function to access MathToolkit methods.
    
    :param operation: The specific operation to perform (must be in the format 'category.operation')
    :param params: A dictionary containing the parameters for the operation
    :return: The result of the mathematical operation
    """
    if operation not in get_available_operations():
        raise ValueError(f"Unknown operation: {operation}. Available operations are: {', '.join(get_available_operations)}")
    
    category, specific_operation = operation.split('.')
    category_method = getattr(MathToolkit, category)
    
    # Convert params dictionary to a list of arguments
    args = list(params.values())
    
    return category_method(specific_operation, *args)
    
CATEGORY_ABBR = {
    "geometry": "g",
    "algebra": "a",
    "number_theory": "nt",
    "trigonometry": "t",
    "statistics": "s",
    "probability": "p"
}

ABBR_CATEGORY = {v: k for k, v in CATEGORY_ABBR.items()}

def get_abbreviated_operations():
    operations = get_available_operations()
    return [f"{CATEGORY_ABBR[op.split('.')[0]]}.{op.split('.')[1]}" for op in operations]

def create_concise_description(operations):
    description = "Math operations (category.operation):\n"
    description += ", ".join(operations)
    description += "\nProvide parameters as a dictionary."
    return description

abbreviated_operations = get_abbreviated_operations()
concise_description = create_concise_description(abbreviated_operations)

def abbreviated_math_toolkit_wrapper(operation: str, params: dict):
    category_abbr, func = operation.split('.')
    category = ABBR_CATEGORY[category_abbr]
    return math_toolkit_wrapper(f"{category}.{func}", params)



