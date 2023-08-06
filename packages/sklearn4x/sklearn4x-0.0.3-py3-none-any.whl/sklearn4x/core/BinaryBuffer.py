import struct
from typing import List, Dict, Any

import numpy as np

ELEMENT_TYPE_BYTE = 0x01
ELEMENT_TYPE_SHORT = 0x02
ELEMENT_TYPE_INT = 0x04
ELEMENT_TYPE_LONG = 0x08
ELEMENT_TYPE_UNSIGNED_BYTE = 0x11
ELEMENT_TYPE_UNSIGNED_SHORT = 0x12
ELEMENT_TYPE_UNSIGNED_INT = 0x14
ELEMENT_TYPE_UNSIGNED_LONG = 0x18
ELEMENT_TYPE_FLOAT = 0x20
ELEMENT_TYPE_DOUBLE = 0x21
ELEMENT_TYPE_STRING = 0x30
ELEMENT_TYPE_LIST = 0x40
ELEMENT_TYPE_DICTIONARY = 0x41
ELEMENT_TYPE_NUMPY_ARRAY = 0x42
ELEMENT_TYPE_STRING_ARRAY = 0x43
ELEMENT_TYPE_NONE = 0x10


class BinaryBuffer:
    def __init__(self):
        self.__data = []
        self.__primitive_type_mapper = {
            str: (ELEMENT_TYPE_STRING, self.append_string),
            int: (ELEMENT_TYPE_LONG, self.append_long),
            float: (ELEMENT_TYPE_DOUBLE, self.append_double),
            list: (ELEMENT_TYPE_LIST, self.append_list),
            dict: (ELEMENT_TYPE_DICTIONARY, self.append_dictionary),
            np.ndarray: (ELEMENT_TYPE_NUMPY_ARRAY, self.append_numpy_array),
        }
        self.__numpy_type_mapper = {
            'int8': ('b', ELEMENT_TYPE_BYTE),
            'uint8': ('b', ELEMENT_TYPE_UNSIGNED_BYTE),
            'int16': ('h', ELEMENT_TYPE_SHORT),
            'uint16': ('h', ELEMENT_TYPE_UNSIGNED_SHORT),
            'int32': ('i', ELEMENT_TYPE_INT),
            'uint32': ('i', ELEMENT_TYPE_UNSIGNED_INT),
            'int64': ('l', ELEMENT_TYPE_LONG),
            'uint64': ('l', ELEMENT_TYPE_UNSIGNED_LONG),
            'float32': ('f', ELEMENT_TYPE_FLOAT),
            'float64': ('d', ELEMENT_TYPE_DOUBLE),
        }

    def append_float(self, value: float) -> None:
        if np.isnan(value):
            self.append_byte(0)
        else:
            self.append_byte(1)
            self.__data.append(struct.pack('f', value))

    def append_double(self, value: float) -> None:
        if np.isnan(value):
            self.append_byte(0)
        else:
            self.append_byte(1)
            self.__data.append(struct.pack('d', value))

    def append_byte(self, value: int) -> None:
        self.__data.append(struct.pack('b', value))

    def append_short(self, value: int) -> None:
        self.__data.append(struct.pack('h', value))

    def append_int(self, value: int) -> None:
        self.__data.append(struct.pack('i', value))

    def append_long(self, value: int) -> None:
        self.__data.append(struct.pack('l', value))

    def __append_number(self, value, fmt) -> None:
        if fmt in ['d', 'f']:
            # This is a float value and may be NaN
            if np.isnan(value):
                self.append_byte(0)
            else:
                self.append_byte(1)
                self.__data.append(struct.pack(fmt, value))
        else:
            self.__data.append(struct.pack(fmt, value))

    def append_numpy_array(self, value: np.ndarray) -> None:
        if value is None:
            self.append_byte(0)
        else:
            self.append_byte(1)
            shape = value.shape
            self.append_int(len(shape))

            if value.dtype.name not in self.__numpy_type_mapper:
                raise Exception('The type ' + value.dtype.name + ' is not supported!')

            fmt, element_type = self.__numpy_type_mapper[value.dtype.name]
            self.append_byte(element_type)

            for dimension in shape:
                self.append_int(dimension)

            data = value.tolist()

            self.__append_numpy_array_as_list_to_buffer(data, fmt)

    def __append_numpy_array_as_list_to_buffer(self, data: List, fmt: str) -> None:
        first_element = data[0]

        if isinstance(first_element, list):
            # List of list, must recurse
            for inner_list in data:
                self.__append_numpy_array_as_list_to_buffer(inner_list, fmt)
        else:
            for value in data:
                self.__append_number(value, fmt)

    def append_string(self, value: str) -> None:
        if value is None:
            self.append_byte(0)
        else:
            self.append_byte(1)
            value = bytes(value, 'utf-8')
            self.append_int(len(value))
            self.__data.append(value)

    def append_array_of_string(self, array):
        if array is None:
            self.append_byte(0)
        else:
            self.append_byte(1)
            self.append_int(len(array))
            for item in array:
                self.append_string(item)

    def append_list(self, value: List) -> None:
        if value is None:
            self.append_byte(0)
        else:
            self.append_byte(1)
            self.append_int(len(value))

            for element in value:
                if element is None:
                    self.append_byte(ELEMENT_TYPE_NONE)
                elif self.__is_primitive_value(element):
                    self.__append_primitive_value(element)
                else:
                    raise Exception('An error occurred when serializing a list. Only primitive values are supported.')

    def append_dictionary(self, value: Dict[str, Any]) -> None:
        if value is None:
            self.append_byte(0)
        else:
            self.append_byte(1)
            self.append_int(len(value))

            for key in value.keys():
                self.append_string(key)
                element = value[key]

                if element is None:
                    self.append_byte(ELEMENT_TYPE_NONE)
                elif self.__is_string_array(element):
                    self.append_byte(ELEMENT_TYPE_STRING_ARRAY)
                    self.append_array_of_string(element)
                elif self.__is_primitive_value(element):
                    self.__append_primitive_value(element)
                else:
                    raise Exception(
                        'An error occurred when serializing a dictionary. Only string key and primitive values are supported.')

    def __is_primitive_value(self, value):
        return type(value) in self.__primitive_type_mapper.keys()

    def __append_primitive_value(self, value):
        element_type, appender = self.__primitive_type_mapper[type(value)]
        self.append_byte(element_type)
        appender(value)

    def to_buffer(self):
        return b''.join(self.__data)

    def append_data(self, value):
        if isinstance(value, np.ndarray):
            self.append_numpy_array(value)
        elif self.__is_string_array(value):
            self.append_array_of_string(value)
        elif isinstance(value, list):
            self.append_list(value)
        elif isinstance(value, float):
            self.append_double(value)
        elif isinstance(value, int):
            self.append_long(value)
        else:
            raise Exception('This type is not supported.')

    def __is_string_array(self, value):
        if isinstance(value, list) and len(value) > 0:
            all_string = True

            for item in value:
                all_string = isinstance(item, str)
                if not all_string:
                    break

            return all_string

        return False
