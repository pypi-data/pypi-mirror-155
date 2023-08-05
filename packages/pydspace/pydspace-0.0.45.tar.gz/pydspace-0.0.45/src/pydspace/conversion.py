import logging
import datetime
import matlab
import matlab.engine
import numpy as np
import pandas as pd

from collections.abc import Iterable
from typing import Union

logger = logging.getLogger(__name__)

MatlabEngine = matlab.engine.matlabengine.MatlabEngine

class TypeConversor:

    def __init__(self, fields: list, engine: MatlabEngine):
        # Unfortunately the engine is needed to convert some types
        self.engine = engine
        self.fields = fields


        # There is no float16 in the python api engine, so we use matlab.single.
        self.type_map = {
            np.float16: self.from_np_float16,
            np.float32: self.from_np_float32,
            np.float64: self.from_np_float64,
            np.int8: self.from_np_int8,
            np.int16: self.from_np_int16,
            np.int32: self.from_np_int32,
            np.int64: self.from_np_int64,
            np.uint8: self.from_np_uint8,
            np.uint16: self.from_np_uint16,
            np.uint32: self.from_np_uint32,
            np.uint64: self.from_np_uint64,
            np.bool8: self.from_np_bool8,
            str: self.from_string,
            "col_of_arrays": self.from_column_of_arrays,
            datetime.date: self.from_datetime
        }

        SUPPORTED_TYPES = tuple(self.type_map.keys())

        valid_types = []
        numpy_object_types = []
        unknown_types = []

        for name, type_attr in self.fields:
            if type_attr in SUPPORTED_TYPES:
                valid_types.append((name, type_attr))
            else:
                if type_attr == np.object_:
                    numpy_object_types.append((name,type_attr))
                    warn_msg = (
                        f"Type for the column {name} is unknow "
                        f"i.e np.object_."
                    )
                    logger.warning(warn_msg)
                else:
                    unknown_types.append((name, type_attr))
                    logger.warning(f"Type for the column {name} not supported.")


        self.valid_types = valid_types
        self.numpy_object_types = numpy_object_types
        self.unknown_types = unknown_types

        # TODO: In theory the above list must be empty since either the dtype
        # in a numpy recarray is either known or a np.object_, therefore
        # something went really wrong if these assert is met.
        assert len(self.unknown_types) == 0

    def get_valid_types(self) -> list:
        """
        Returns a subset of the list passed to the constructor
        with the name and the types that we actually support.

        Returns:
            Subset of the list with the supported types.
        """
        return self.valid_types

    def get_fields_with_numpy_obj(self) -> list:
        """
        Returns a subset of the list passed to the constructor
        with the elements that have as type np.object_.

        Returns:
            Subset of the list with the columns that have as type np.object_.
        """
        return self.numpy_object_types


    def is_column_of(self, column:np.ndarray, class_to_test: type) -> bool:
        """
        Attempts to guess if the column has actually as 'dtype' the
        class_to_test.

        If 0.95 of the elements of the list have the correct type then we
        declare the column as a column with type class_to_test.

        Args:
            column: The column to check for.
        Returns:
            boolean
        """
        N = len(column)
        counter = 0

        for item in column:
            if isinstance(item, class_to_test):
                counter += 1

        ratio = counter/N

        if ratio >= 0.95:
            return True
        else:
            return False 

    def convert_value(
        self, 
        value: np.ndarray,
        dtype: Union[str, type]
    ) -> matlab.object:
        """
        Converts the argument 'value' to the specified 'dtype' and
        returns it as a matlab.object. For some conversions the matlab
        engine is needed. We assume that the conversion is indeed possible.

        Args:
            value: Object to be converted to a matlab.object
            dtype: Type to be converted in.
        Returns:
            The converted matalab.object.
        """
        conversion_function = self.type_map[dtype]
        return conversion_function(value)

    def from_np_float16(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.single(value.tolist())

    def from_np_float32(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.single(array.tolist())

    def from_np_float64(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.double(array.tolist())

    def from_np_int8(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.int8(array.tolist())

    def from_np_int16(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.int16(array.tolist())

    def from_np_int32(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.int32(array.tolist())

    def from_np_int64(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.int64(array.tolist())

    def from_np_uint8(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.uint8(array.tolist())

    def from_np_uint16(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.uint16(array.tolist())

    def from_np_uint32(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.uint32(array.tolist())

    def from_np_uint64(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.uint64(array.tolist())

    def from_np_bool8(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array to a matlab.object array.

        Args:
            array: Array to be converted.
        Returns:
            matlab.object
        """
        return matlab.logical(array.tolist())

    def from_string(self, array: np.ndarray) -> matlab.object:
        """
        Converts a numpy array of strings to a matlab.object cell of strings.

        Args:
            array: Array or list to be converted.
        Returns:
            Cell (matlab.object) of strings.
        """
        return self.engine.cell(array.tolist())

    def from_column_of_arrays(self, arrays: np.ndarray) -> matlab.object:
        """
        Converts a numpy array of numpy ndarrays to a matlab.object array, with
        the first dimension equal to the number of arrays in the array. The
        other dimensions remain fixed. i.e. If arrays[0].shape # (2,3), then
        the dimension of the returned matlab array is (N, 2, 3)

        Args:
            arrays: Array of arrays to be converted.
        Returns:
            matlab.object.
        """
        # TODO: Find a better way to get the actual dtype
        # since if the first item is None, it doesn't work

        # Arrays must be a list of np.ndarrays
        column = np.vstack(arrays)
        type_attr = column.dtype.type

        # First dimension must match the number of items in the list
        assert column.shape[0] == len(arrays)

        return self.convert_value(column, type_attr)

    def from_datetime(self, dates: np.ndarray) -> matlab.object:
        """
        Converts a numpy array with elements fo the type datatime.date to a
        matlab.object array of matlab type datetime.

        Args:
            array: List of dates to be converted.
        Returns:
            matlab.object.
        """
        dates_cell = []
        for date in dates:
            date_string = date.strftime("%Y-%m-%d %H:%M:%S")
            dates_cell.append(date_string)

        matlab_cell = self.engine.datetime(dates_cell)

        return matlab_cell
