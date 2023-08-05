import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)

def is_string_column(series: pd.Series) -> bool:
    """
    Attempts to guess if the pandas series has actually as 'dtype' string.

    If 0.95 of the elements of the series have a string type then we declare the column as a
    string column.

    Args:
        series: The pd.Series column to check for.
    Returns:
        boolean
    """

    # This condition has to be meet.
    assert series.dtype == object or series.dtype == pd.StringDtype()

    # Check if the 95% of the data points are strings.
    N = len(series)
    counter = 0
    for item in series:
        if isinstance(item, str):
            counter += 1

    ratio = counter/N

    if ratio >= 0.95:
        return True
    else:
        return False

def is_recarray(array: np.ndarray) -> bool:
    """
    Simple functino that checks if the array is a record array.
    We are going to take as definition of record array and array that
    has the attribute 'dtype.fields' as non-empty i.e not None.

    Args:
        array: Numpy array to be checked.
    """
    if array.dtype.fields is not None:
        return True
    else:
        return False

def is_query_expression(obj):
    """
    An object will be a query if it contains a fetch method.

    Reference:
    https://stackoverflow.com/questions/5268404/what-is-the-fastest-way-to-check-if-a-class-has-a-function-defined

    Args:
        obj: Objet to be tested
    """
    fetch_method = getattr(obj, "fetch", None)

    if callable(fetch_method):
        return True
    else:
        return False
