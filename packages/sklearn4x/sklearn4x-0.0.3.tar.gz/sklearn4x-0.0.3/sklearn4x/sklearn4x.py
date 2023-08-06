from typing import *

import sklearn
from sklearn.base import BaseEstimator

from .core.BinaryBuffer import BinaryBuffer
from .core.BinaryPackage import BinaryPackage
from .serializers.serializers_list import LIST_OF_SERIALIZERS


__all__ = [
    'save_scikit_learn_model'
]


def __ensure_input_is_valid(models):
    if not isinstance(models, dict):
        raise Exception('The models parameter should be a dictionary of {name: model_object}.')

    for model_name in models.keys():
        model = models[model_name]

        if not isinstance(model, BaseEstimator):
            raise Exception('The model provided with key "' + model_name + '" is not an scikit-learn BaseEstimator')


def save_scikit_learn_model(models: Dict[str, Any], path: str, additional_data=None) -> None:
    """
    Take a dictionary of scikit-learn objects and serialize them in a single binary package file.

    :param models: Dictionary of the scikit-learn objects. The key for each model is later used to
                   access that object in other languages.
    :param path: Path to save the model in.
    :param additional_data: A dictionary of extra values that should be included in the binary
                            package.
    :return: None
    """

    __ensure_input_is_valid(models)

    content = []
    for model_name in models.keys():
        model = models[model_name]
        found = False
        for type, serializer in LIST_OF_SERIALIZERS:
            if isinstance(model, type):
                content.append((model_name, model, serializer))
                found = True
                break

        if not found:
            raise Exception('The model provided with key "' + model_name + '" is an unsupported types.')

    # Prepare file header
    buffer = BinaryBuffer()
    package = BinaryPackage.default(buffer)
    package.create_file_header([serializer for model_name, model, serializer in content])

    # Append models
    for model_name, model, serializer in content:
        package.append_serialized_model(model_name, model, serializer)

    # Add additional data
    if additional_data is not None:
        package.add_additional_data(additional_data)

    # Save package
    package.save_to_file(path)
