"""
Supports the context classification functionality of fidecls.

Context in this case means metadata about a database such as
schema/table/column name

Analysis of PII through the metadata surrounding a table or
data sample(s)

"""

from typing import Callable, Dict, Iterable, List, Union

from fidescls.cls import classifiers

# pylint: disable=invalid-name

CONTEXT_CLASSIFY_METHODS: Dict[str, Callable] = {
    "similarity": classifiers.similarity_classifier
}


def classify(
    input_data: Union[str, Iterable],
    method_name: str = "similarity",
    method_params: Dict = {},
) -> List:
    """
    Perform context classification using the provided method and associated parameters
    Args:
        input_data: Data to be classified
        method_name: name of the context classification method to use (default: similarity)
        method_params: parameters to pass along to the classification method

    Returns:
        The classification response
    """
    if method_name not in CONTEXT_CLASSIFY_METHODS.keys():
        raise ValueError(f"{method_name} is not a valid context classification method")
    return CONTEXT_CLASSIFY_METHODS[method_name](input_data, **method_params)
