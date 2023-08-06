[![ PyPI ](https://img.shields.io/pypi/v/sklearn4x)](https://pypi.org/project/sklearn4x/)


Working with Python and the Machine Learning and Data Science ecosystem is fun, but
when it comes to deployment, you may not want to have to use Python. The goal of this
repository (and its siblings) is to address this need; you can experiment and train models in the rich
Python ecosystem, but deploy your models in other languages and platforms.
**scikit-learn4x** is a free an open source library that allows you to deploy
scikit-learn model in other programming languages.

### Important Links

Release on pypi.org: https://pypi.org/project/sklearn4x/

scikit-learn 4 JVM Repository: https://github.com/scikitlearn4x/scikit-learn-4-jvm
The scikit-learn-4-jvm library uses the models serialized by this repository to allow inference in JVM
based languages.

scikit-learn 4 .NET Repository: https://github.com/scikitlearn4x/scikit-learn-4-net
The scikit-learn-4-net library uses the models serialized by this repository to allow inference in .NET
based languages.

## Installation

sklearn4x requires only the following 2 dependencies:

* scikit-learn
* numpy

Note for the version of scikit-learn, there is no limitation. The library detects the vesion of 
scikit-learn and looks for the classifier fields based on the installed version.

To install from pypi.org, run this command:
```
pip install sklearn4x
```

## Usage Example

Here is an example on how to use the library. 

#### The Python Code

```
from sklearn import datasets
from sklearn.naive_bayes import GaussianNB
from sklearn4x.sklearn4x import save_scikit_learn_model
import pandas as pd

ds = datasets.load_iris()
X = ds.data
y = ds.target

train_data = pd.DataFrame(data=X, index=None, columns=['SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm'], dtype=X.dtype, copy=False)

classifier = GaussianNB()
classifier.fit(train_data, y)

predictions = classifier.predict(X)
prediction_probabilities = classifier.predict_proba(X)
prediction_log_probabilities = classifier.predict_log_proba(X)

test_data = {
    "training_data": X,
    "predictions": predictions,
    "prediction_probabilities": prediction_probabilities,
    "prediction_log_probabilities": prediction_log_probabilities,
}

print(f'First data point prediction: {predictions[0]}')
print(f'First data point probabilities: {prediction_probabilities[0, 0]:.3f}, {prediction_probabilities[0, 1]:.3f}')
print(f'First data point log probabilities: {prediction_log_probabilities[0, 0]:.3f}, {prediction_log_probabilities[0, 1]:.3f}')


save_scikit_learn_model({'classifier_to_deploy_in_java': classifier}, '/some/path/on/disk.skx', test_data)

# You should see the following outputs:
#
# First data point prediction: 0
# First data point probabilities: 1.000, 0.000
# First data point log probabilities: 0.000, -41.141
```

#### The Java Code

```
String path = "/same/path/on/disk.skx";
IScikitLearnPackage binaryPackage = ScikitLearnPackageFactory.loadFromFile(path);

// Check actual computed values
GaussianNaiveBayes classifier = (GaussianNaiveBayes)binaryPackage.getModel("classifier_to_deploy_in_java");

NumpyArray<Double> x = (NumpyArray<Double>)binaryPackage.getExtraValues().get("training_data");

NumpyArray<Long> predictions = classifier.predict(x);
NumpyArray<Double> probabilities = classifier.predictProbabilities(x);
NumpyArray<Double> logProbabilities = classifier.predictLogProbabilities(x);

System.out.println("First data point prediction: " + predictions.get(0));
System.out.println(String.format("First data point probabilities: %.3f, %.3f", probabilities.get(0, 0), probabilities.get(0, 1)));
System.out.println(String.format("First data point log probabilities: %.3f, %.3f", logProbabilities.get(0, 0), logProbabilities.get(0, 1)));

/*
    You should see the same outputs as Python's:

    First data point prediction: 0
    First data point probabilities: 1.000, 0.000
    First data point log probabilities: 0.000, -41.141
*/
```


#### The C# Code

```
String path = "/same/path/on/disk.skx";
IScikitLearnPackage binaryPackage = ScikitLearnPackageFactory.LoadFromFile(path);

// Check actual computed values
GaussianNaiveBayes classifier = (GaussianNaiveBayes)binaryPackage.GetModel("classifier_to_deploy_in_java");

NumpyArray<double> x = (NumpyArray<double>)binaryPackage.ExtraValues["training_data"];

NumpyArray<long> predictions = classifier.Predict(x);
NumpyArray<double> probabilities = classifier.PredictProbabilities(x);
NumpyArray<double> logProbabilities = classifier.PredictLogProbabilities(x);

Console.Writeline($"First data point prediction: {predictions.Get(0)}:N3");
Console.Writeline($"First data point probabilities: {probabilities.Get(0, 0):N3}, {probabilities.Get(0, 1):N3}");
Console.Writeline($"First data point log probabilities: {logProbabilities.Get(0, 0):N3}, {logProbabilities.Get(0, 1):N3}");

/*
    You should see the same outputs as Python's:

    First data point prediction: 0
    First data point probabilities: 1.000, 0.000
    First data point log probabilities: 0.000, -41.141
*/
```

## Supported Models

See the [release notes](https://github.com/scikitlearn4x/scikit-learn-4x-python-lib/blob/master/ReleaseNotes.md) for most updated support.

## Help and Support

Feel free to contact me with my email address:
ma (initials for Mohammad Ali), then underscore and then my last name (Yektaie). Finally,
add at outlook.com.


