from .naive_bayes import *
from sklearn.naive_bayes import *

LIST_OF_SERIALIZERS = []


def add_sklearn_type(cls, serializer):
    try:
        classifier_type = eval(compile(cls, f'{cls}_dynamic.py', 'eval'))
        LIST_OF_SERIALIZERS.append((classifier_type, serializer))
    except NameError as ex:
        # Ignore the type, it is not supported by this version of sklearn.
        pass


def load_nb_serializers():
    add_sklearn_type('GaussianNB', GaussianNaiveBayesSerializer())
    add_sklearn_type('BernoulliNB', BernoulliNaiveBayesSerializer())
    add_sklearn_type('MultinomialNB', MultinomialNaiveBayesSerializer())
    add_sklearn_type('ComplementNB', ComplementNaiveBayesSerializer())
    add_sklearn_type('CategoricalNB', CategoricalNaiveBayesSerializer())


def load_list_of_serializers():
    load_nb_serializers()


if len(LIST_OF_SERIALIZERS) == 0:
    load_list_of_serializers()
