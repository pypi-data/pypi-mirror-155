import time
import logging
import matlab
import matlab.engine
import numpy as np
import pandas as pd
import datetime

from typing import Union

# from .threads import ExceptionsThread
from .utils import is_recarray
from . import get_matlab_engine

from .conversion import TypeConversor

MatlabEngine = matlab.engine.matlabengine.MatlabEngine
SupportedType = Union[np.ndarray, pd.DataFrame]

logger = logging.getLogger(__name__)

class DspaceWrapper:
    """
    This class implements a wrapper for the objects that the
    MatlabEngine for python returns, when the user starts
    dSpace with pydspace.
    """

    def __init__(
        self,
        dsource: matlab.object,
        dspace_app: matlab.object,
        matlab_engine: MatlabEngine
    ):
        self.dsource = dsource
        self.dspace_app = dspace_app
        self.matlab_engine = matlab_engine

    def dsource_info(self):
        """
        Prints, to the stdout that the associated engine has been started with,
        the info of the dsource object.
        """
        # TODO: Ideally 'info()' should return a string, so that we can handle
        # printing to the console or the logging in pyton itself but it does
        # not. Instead the matlab code just prints to the console.
        self.matlab_engine.info(self.dsource, nargout=0)

    def add_data(self, *args):
        """
        Adds the arguments as an additional source to the dsource attribute of
        the DspaceWrapper.
        It relies on the addData method of the matlab TableDataSource object.

        Args:
            args: Data to be processed and added
        """
        input_names = []
        input_values = []
        index_to_ignore = []

        num_args = len(args)
        i = 0
        while i < num_args:
            # Check if the arguments follow a (name, value) scheme and
            # proceed correspondingly.
            if isinstance(args[i], str):
                if i == num_args - 1:
                    error_msg = (
                        f"dspace: The last function input {i} is a string {args[i]}.\n"
                        "Strings can only occur in name, value pairs"
                        "(to give names to labels or features).\nInput ignored."

                    )
                    logger.warning(error_msg)
                    break
                    # raise ValueError(error_msg)

                name, value = args[i], args[i+1]

                # If the next argument is also a string, ignore those
                # two elements.
                if isinstance(value, str):
                    error_msg = (
                        f"dspace: Function inputs {i} and {i+1} are both strings"
                        f" {name}, {value}.\n"
                        "Strings can only occur in name, value pairs"
                        "(to give names to labels or features).\nInput ignored."
                    )
                    i = i + 2
                    logger.warning(error_msg)
                    continue

                # Check if next argument is indeed a numpy array.
                # TODO: We must be able to use different datatypes not only
                # numpy arrays
                if not isinstance(value, np.ndarray):
                    error_msg = (
                        f"dspace: Function input {i} is a string {name}.\n"
                        f"The next input must be a numpy.ndarray but is not.\n"
                        "Input ignored."
                    )
                    i = i + 2
                    logger.warning(error_msg)
                    continue

                # Create input from the name, value pair.
                # TODO: Make sure the name can be used in Matlab code.
                input_names.append(name)
                input_values.append(value)

                i = i + 2

            else:
                # TODO: In Matlab it is possible to get name of the variable
                # passed as argument to a function with 'inputname'. In Python
                # there is not a clean way to do this, therefore for the moment
                # if no names are passed, each value will get as name 'input_i'.
                name = f"name_{i}"
                value = args[i]

                input_names.append(name)
                input_values.append(value)

                index_to_ignore.append(i)

                i = i + 1

        assert len(input_names) == len(input_values)

        # Perform the conversion from python objects to 'matlab.object'.
        for i, value in enumerate(input_values):
            input_values[i] = convert_value(value, self.matlab_engine)
            # Free the memory immediately
            del value

        # Recollect the input names and input values into a single list,
        # assuming (kev, value) scheme except for dataframes.
        varargin = []
        for i in range(len(input_names)):
            # TODO: This is just a hack that I need to discuss with Sepp.
            if i in index_to_ignore:
                varargin.append(input_values[i])
            else:
                varargin.append(input_names[i])
                varargin.append(input_values[i])

        self.matlab_engine.addData(self.dsource, *varargin, nargout=0)


def dspace(*args, no_gui: bool = False) -> DspaceWrapper:
    """
    This function it's just a python rewrite of the dspace.m function provided
    in the dSpace matlab package. You can find more documentation in that
    respective file.

    Args:
        args: Either numpy arrays, or (name,value) pairs.
        no_gui: Don't open the GUI, for testing purposes.
    Returns:
        Matlab engine object.
    """
    input_names = []
    input_values = []

    num_args = len(args)

    if num_args == 0:
        # Start dspace without arguments
        # Start the Matlab Engine
        engine = get_matlab_engine()

        engine.dspace(nargout=0)

        # Start the ExceptionsThread
        # exceptions_thread = ExceptionsThread(engine)
        # exceptions_thread.start()

        # We must return the engine. Since we created it as a local
        # variable if we don't return it, then it will just get deleted from the
        # stack i.e. the engine gets killed and dspace will not open.

        # TODO: Maybe it's useful to also return the dspaceApp, dSource and the
        # dView
        # dspace_wrapper = DspaceWrapper(dsource, dspace_app, engine)

        # return dspace_wrapper

        return
    i = 0
    while i < num_args:
        # Check if the arguments follow a (name, value) scheme and
        # proceed correspondingly.
        if isinstance(args[i], str):
            if i == num_args - 1:
                error_msg = (
                    f"dspace: The last function input {i} is a string {args[i]}.\n"
                    "Strings can only occur in name, value pairs"
                    "(to give names to labels or features).\nInput ignored."

                )
                logger.warning(error_msg)
                break
                # raise ValueError(error_msg)

            name, value = args[i], args[i+1]

            # If the next argument is also a string, ignore those
            # two elements.
            if isinstance(value, str):
                error_msg = (
                    f"dspace: Function inputs {i} and {i+1} are both strings"
                    f" {name}, {value}.\n"
                    "Strings can only occur in name, value pairs"
                    "(to give names to labels or features).\nInput ignored."
                )
                i = i + 2
                logger.warning(error_msg)
                continue

            # Check if next argument is indeed a numpy array.
            # TODO: We must be able to use different dataypes not only
            # numpy arrays
            if not isinstance(value, np.ndarray):
                error_msg = (
                    f"dspace: Function input {i} is a string {name}.\n"
                    f"The next input must be a numpy.ndarray but is not.\n"
                    "Input ignored."
                )
                i = i + 2
                logger.warning(error_msg)
                continue

            # Create input from the name, value pair.
            # TODO: Make sure the name can be used in Matlab code.
            input_names.append(name)
            input_values.append(value)

            i = i + 2

        else:
            # TODO: In Matlab it is possible to get name of the variable
            # passed as argument to a function with 'inputname'. In Python
            # there is not a clean way to do this, therefore for the moment
            # if no names are passed, each value will get as name 'input_i'.
            name = f"name_{i}"
            value = args[i]

            input_names.append(name)
            input_values.append(value)

            i = i + 1

    assert len(input_names) == len(input_values)

    # Start the Matlab Engine
    engine = get_matlab_engine()

    # Perform the conversion from python objects to 'matlab.object'.
    for i, value in enumerate(input_values):
        input_values[i] = convert_value(value, engine)
        # Free the memory immediately
        del value

    # In the ideal case we would like to operate on the object
    # returned by the parseDspaceArgs matlab function, but the matlab api
    # for python does not allow it, so instead we just call the function and
    # save the output in the workspace, then we use eval. An issue is that,
    # then the variable is a global one and not a local one, so naming bugs
    # could appear.
    # TODO: There might be a cleaner way to do this.

    engine.workspace["source_pydspace"] = engine.dspace.parseDspaceArgs(
        input_values,
        input_names,
        1,
        nargout=1
    )

    instr_1 = "source_pydspace.createdBy = 'Import through dspace() function from python.';"
    instr_2 = "source_pydspace.createdOn = now();"

    engine.eval(instr_1, nargout=0)
    engine.eval(instr_2, nargout=0)

    source = engine.workspace["source_pydspace"]

    if no_gui:
        dsource = engine.dspace(source, nargout=1)
        dspace_app = None
    else:
        dsource, dspace_app = engine.dspace(source, nargout=2)

    # Start the ExceptionsThread
    # exceptions_thread = ExceptionsThread(engine)
    # exceptions_thread.start()

    # We must return the engine. Since we created it as a local
    # variable if we don't return it, then it will just get deleted from the
    # stack i.e. the engine gets killed and dspace will not open.

    # TODO: Maybe it's useful to also return the dspaceApp, dSource and the
    # dView
    dspace_wrapper = DspaceWrapper(dsource, dspace_app, engine)

    return dspace_wrapper


def convert_value(value: SupportedType, engine: MatlabEngine):
    """
    Converts the supported types to the corresponding matlab.object.

    Args:
        value: Value to be converted to a matlab.object
        engine: Instance of the matlab engine that will be used to perform the conversions
    Returns:
        matlab.object
    """
    if isinstance(value, np.ndarray):
        if is_recarray(value):
            return convert_recarray(value, engine)
        else:
            return convert_numpy_array(value)
    if isinstance(value, pd.DataFrame):
        return convert_dataframe(value, engine)


def convert_numpy_array(array: np.ndarray) -> matlab.object:
    """
    Converts the numpy array to matlab array of doubles.

    Args:
        array: Array to be converted.
    Returns:
        matlab.object
    """
    return matlab.double(array.tolist())


def convert_recarray(recarray: np.ndarray, engine: MatlabEngine) -> matlab.object:
    """
    Takes a numpy record array and transforms it to a matlab.object of type
    Table. Non supported columns will be skipped. For some type conversions
    the engine is needed.

    Args:
        recarray: Record array to be converted to a matlab.object Table.
        engine: Instance of the matlab engine that will be used to perform the conversions
    Returns:
        matlab.object
    """
    N = recarray.shape[0]
    fields = list(recarray.dtype.fields.items())
    fields = [(tup[0], tup[1][0].type) for tup in fields]

    conversor = TypeConversor(fields, engine)

    # These are the easy types to convert
    valid_types = conversor.get_valid_types()

    # The types for these fields are unknown
    fields_with_numpy_obj = conversor.get_fields_with_numpy_obj()

    # WARNING: I assume that in a recarray if one field is not a np.ndarray
    # then it must be a np.object_ otherwise we will be ignoring some columns
    # The following assert checks that.
    assert len(conversor.unknown_types) == 0

    # We perform a heuristic to check if we can guess the type of the np.obj
    # as a string or as a column of numpy arrays.
    for field_name, _ in fields_with_numpy_obj:
        column = recarray[field_name]

        if conversor.is_column_of(column, str):
            valid_types.append((field_name, str))
            logger.warning(f"We infer column {field_name} as a column of strings.")
        elif conversor.is_column_of(column, np.ndarray):
            valid_types.append((field_name, "col_of_arrays"))
            logger.warning(f"We infer column {field_name} as a column of arrays.")
        elif conversor.is_column_of(column, datetime.date):
            valid_types.append((field_name, datetime.date))
            logger.warning(f"We infer column {field_name} as a column of dates.")
        else:
            error_msg = (
                f"We cannot infer the type for the column"
                f"{field_name}, skipping that column."
            )
            logger.warning(error_msg)

    # Convert the values
    table_var_name = f"local_table_{round(time.time())}"
    engine.workspace[table_var_name] = engine.table()

    for field_name, type_attr in valid_types:
        column = recarray[field_name]
        matlab_column = conversor.convert_value(column, type_attr)

        var_name = f"local_{field_name}_{round(time.time())}"
        engine.workspace[var_name] = matlab_column

        if type_attr == "col_of_arrays":
            # We don't reshape in these case.
            instr_2 = f"{table_var_name}.{field_name} = {var_name};"
            instr_3 = f"clear {var_name};"

            engine.eval(instr_2, nargout=0)
            engine.eval(instr_3, nargout=0)
        else:
            instr_1 = f"{var_name} = reshape({var_name}, {N}, 1);"
            instr_2 = f"{table_var_name}.{field_name} = {var_name};"
            instr_3 = f"clear {var_name};"

            engine.eval(instr_1, nargout=0)
            engine.eval(instr_2, nargout=0)
            engine.eval(instr_3, nargout=0)

    return engine.workspace[table_var_name]


def convert_dataframe(df: pd.DataFrame, engine: MatlabEngine) -> matlab.object:
    """
    Takes a pandas DataFrame and attempts an as close as possible conversion to
    a matlab.Table, using the matlab engine for python. Unfortunately several
    hacks had to be performed to make this work.

    Args:
        df: DataFrame to convert to a matlab Table.
        engine: The MatlabEngine that provides the workspace where the Table
        will be stored.
    Returns:
        The matlab.object that references to the Table.
    """
    # Pandas DataFrames returns scalars as numpy dtypes.
    # Numpy References:
    # https://numpy.org/doc/stable/reference/arrays.scalars.html#sized-aliases
    # Matlab References
    # https://ch.mathworks.com/help/matlab/matlab_external/get-started-with-matlab-engine-for-python.html

    # NOTE:
    # Unfortunately we cannot reshape matlab cells from python using the engine
    # (or at least I couldn't find a way to do it), and then continue to
    # reference the cell later in the python code. Each time you reference, in
    # python, a value that you have created with the matlab.engine, a type
    # conversion is created, and the previous reshape you have performed before is lost.
    # This issue forbids more short and clean ways to transform a DataFrame,
    # with supported columns, to a Matlab table, as for example.
    #     'table = engine.table(*input_values, "VariableNames", data.columns)'
    # sice the engine complains about the shape of the cells. If all the
    # columns of the DataFrame have only numerical data, then it is indeed
    # possible since you only work with mlarrays, but with columns with
    # text/categorical data, a cell must be created and the aforementioned issue
    # appears. Therefore, we resort again to the use of 'engine.eval'.

    recarray = df.to_records()
    return convert_recarray(recarray, engine)
