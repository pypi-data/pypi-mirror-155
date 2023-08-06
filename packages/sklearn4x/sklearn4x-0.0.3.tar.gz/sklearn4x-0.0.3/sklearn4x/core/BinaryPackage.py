from abc import abstractmethod

import sklearn

from sklearn4x import __version__
from sklearn4x.core.BinaryBuffer import BinaryBuffer


class BinaryPackage:
    def __init__(self, buffer: BinaryBuffer):
        self.buffer = buffer

    @abstractmethod
    def create_file_header(self, model_serializers):
        pass

    @abstractmethod
    def append_serialized_model(self, model_name, model, serializer):
        pass

    @abstractmethod
    def add_additional_data(self, dictionary):
        pass

    def get_library_version(self):
        return __version__

    def get_scikit_learn_version(self):
        return sklearn.__version__

    def save_to_file(self, path):
        with open(path, 'wb') as handle:
            handle.write(self.buffer.to_buffer())

    @classmethod
    def default(cls, buffer: BinaryBuffer):
        from sklearn4x.core.file_versions.BinaryPackageV1 import BinaryPackageV1
        return BinaryPackageV1(buffer)
