import sys
import numpy
import scipy
import platform
from sklearn4x.core.BinaryPackage import BinaryPackage

FILE_VERSION = 1


class BinaryPackageV1(BinaryPackage):
    def create_file_header(self, model_serializers):
        self.buffer.append_int(FILE_VERSION)
        header_data = {
            'sklearn4x_version': self.get_library_version(),
            'scikit_learn_version': self.get_scikit_learn_version(),
            'numpy_version': numpy.__version__,
            'scipy_version': scipy.__version__,
            'python_info': sys.version,
            'platform_info': str(platform.uname()),
            'serializer_types': [s.identifier() for s in model_serializers],
        }

        self.buffer.append_dictionary(header_data)

    def append_serialized_model(self, model_name, model, serializer):
        version = self.get_scikit_learn_version()
        serializer.serialize_model(self.buffer, model_name, model, version)

    def add_additional_data(self, dictionary):
        self.buffer.append_dictionary(dictionary)
