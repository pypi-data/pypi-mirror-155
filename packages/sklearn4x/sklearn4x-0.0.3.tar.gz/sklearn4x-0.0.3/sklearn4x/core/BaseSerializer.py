from abc import *

from sklearn4x.core.BinaryBuffer import BinaryBuffer


class BaseSerializer:
    @abstractmethod
    def identifier(self):
        pass

    def serialize_model(self, buffer: BinaryBuffer, model_name, model, version):
        fields = self.get_fields_to_be_serialized(model, version)

        buffer.append_string(model_name)
        buffer.append_int(len(fields))
        for name, value in fields:
            buffer.append_string(name)
            buffer.append_data(value)

    @abstractmethod
    def get_fields_to_be_serialized(self, model, version):
        pass

    def add_n_features(self, fields, model):
        if hasattr(model, 'n_features_'):
            self.add_field(fields, 'n_features', model.n_features_)
        elif hasattr(model, 'n_features_in_'):
            self.add_field(fields, 'n_features', model.n_features_in_)

    def add_feature_names(self, fields, model):
        if hasattr(model, 'feature_names_in_'):
            self.add_field(fields, 'feature_names', self.to_array_of_string(model.feature_names_in_))

    def add_field(self, fields, name, value, version=None, min_version=None, max_version=None):
        if version is None and min_version is None and max_version is None:
            fields.append((name, value))
        elif min_version is None and max_version is not None and self.is_version_higher(max_version, version):
            fields.append((name, value))
        elif self.is_version_higher(version, min_version, True) and self.is_version_higher(max_version, version, False):
            fields.append((name, value))

    def to_array_of_string(self, numpy_array):
        result = [None] * numpy_array.shape[0]

        for i, value in enumerate(numpy_array):
            result[i] = str(value)

        return result

    def is_version_higher(self, v1, v2, on_equal=True):
        if v1 is None:
            return True

        if v1 == v2:
            return on_equal

        c1 = v1.split('.')
        c2 = v2.split('.')

        max_length = max(len(c1), len(c2))
        self.__pad_with_zero(c1, max_length)
        self.__pad_with_zero(c2, max_length)

        for i in range(len(c1)):
            i1 = int(c1[i])
            i2 = int(c2[i])

            if i1 > i2:
                return True
            elif i1 < i2:
                return False

        return False

    def __pad_with_zero(self, c, l):
        while len(c) < l:
            c.append('0')
