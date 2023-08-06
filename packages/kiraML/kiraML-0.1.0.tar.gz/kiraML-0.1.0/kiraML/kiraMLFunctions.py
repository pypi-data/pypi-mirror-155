"""
KiraML Library v0.1.0
"""
from sklearn import datasets, linear_model, neural_network
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import numpy as np
import os
import csv
from ._version import __version__

VERSION = "0.1.0"

DATASETS = {'diabetes' : ['age', 'sex', 'bmi', 'tc', 'ldl', 'hdl', 'tch', 'ltg', 'glu']}

MODELS = {'regression' : {'model': linear_model.LinearRegression, 'params': {}},
        'neural-network':  {'model': neural_network.MLPClassifier, 'params': {
            'hidden_layer_sizes':(15,), 
            'activation': 'logistic',
            'alpha': 1e-4,
            'solver': 'adam', 
            'max_iter': 500,
            'tol': 1e-4, 
            'random_state': 1,
            'learning_rate_init': .1, 
            'verbose': True}
            },
        }

def load(dataset, features=None):
    """
    Loads one of the built-in kiraML datasets or a custom dataset
    """
    # try a built-in dataset
    load_fn = f"load_{dataset}"
    if hasattr(datasets, load_fn):
        x, y = getattr(datasets, load_fn)(return_X_y=True)
        if features:
            return x[:, np.newaxis, DATASETS[dataset].index(features[0])], y
        else:
            return x, y
    else:
        # try to load a local dataset
        try:
            with open(dataset) as f:
                x = []
                y = []
                data_reader = csv.reader(f, delimiter=',', quotechar='"')
                header = list(next(data_reader))
                x_index = header.index(features[0])
                y_index = header.index(features[1])
                for row in data_reader:
                    x.append([float(row[x_index])])
                    y.append(float(row[y_index]))
                # shape of x needs to be (1, len(x))
                # shape of y needs to be (len(y), )
                return np.array(x), np.array(y) 

        except: 
            raise InvalidDataset(dataset)

def split_data(data, train_percent=95):
    """
    Splits the data into a training and testing set.
    The default training set is 95% of the total data set
    Returns [training_set, test_set]
    """
    training_count = round(train_percent / 100 * len(data))
    return data[:training_count], data[training_count:]

def train(training_x, training_y, model_type="regression", user_params = None):
    """
    Train a data set based on the model
    """
    # Train the model
    params = MODELS[model_type]['params']
    if user_params:
        for param, val in user_params.items():
            params[param] = val

    training_obj = MODELS[model_type]['model'](**params) 
    training_obj.fit(training_x, training_y)

    return training_obj

def predict(model, testing_x_data):
    """
    Make a prediction based on the model and testing_x_data
    """
    # Make a prediction
    return model.predict(testing_x_data)

def print_stats(model, y_test, y_pred):
    # this is going to be different for each model, unfortunately
    if type(model) is linear_model.LinearRegression:
        # The coefficients
        print(f"Coefficients: {model.coef_}\n")

        # The mean squared error
        print(f"Mean squared error: {mean_squared_error(y_test, y_pred):.2f}")

        # The coefficient of determination: 1 is perfect prediction
        print(f"Coefficient of determination: {r2_score(y_test, y_pred):.2f}", end='')
        print(" (1 would be a perfect prediction)")
    elif type(model) is neural_network.MLPClassifier:
        accuracy = accuracy_score(y_test, y_pred)
        print(f"Accuracy of neural network model: {round(accuracy * 100, 1)}%")

def scatterplot(x_data, y_data, color="black"):
    plt.scatter(x_data, y_data, color=color) 

def drawline(x_data, y_data, color="blue", linewidth=3):
    plt.plot(x_data, y_data, color=color, linewidth=linewidth) 

def show_plot():
    plt.xticks(())
    plt.yticks(())

    plt.show()

def label_plot(title="title", x_label="x-axis", y_label="y-axis"):
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)

# custom exceptions

class InvalidDataset(Exception):
    def __init__(self, name="(empty)"):
        super().__init__(f"Dataset '{name}' not found in library, or unreadable.")

