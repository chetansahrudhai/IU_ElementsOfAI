# utils.py: Utility file for implementing helpful utility functions used by the ML algorithms.
# Submitted by: Chetan Sahrudhai Kimidi - ckimidi
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff and references slightly from online resources, listed beside each module and in the report as well!

import numpy as np

def euclidean_distance(x1, x2): #NEGLECTING THIS FUNCTION SINCE I CHOSE PART-2 AND DID NOT IMPLEMENT KNN
    """
    Computes and returns the Euclidean distance between two vectors.
    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    raise NotImplementedError('This function must be implemented by the student.')

def manhattan_distance(x1, x2): #NEGLECTING THIS FUNCTION SINCE I CHOSE PART-2 AND DID NOT IMPLEMENT KNN
    """
    Computes and returns the Manhattan distance between two vectors.
    Args:
        x1: A numpy array of shape (n_features,).
        x2: A numpy array of shape (n_features,).
    """
    raise NotImplementedError('This function must be implemented by the student.')

def identity(x, derivative = False): #reference for this activation function is - http://theurbanengine.com/blog/linear-identity-activation
    #Identity is a special case of linear activation function when the 'a' in f(x) = a.x, equals to 1 i.e. a = 1.
    """
    Computes and returns the identity activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.
    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    if derivative: # return f'(x), which would be 1 
        return 1
    return x #else return the same itself

def sigmoid(x, derivative = False): # reference for this activation function is - https://en.wikipedia.org/wiki/Sigmoid_function (Logistic)
    """
    Computes and returns the sigmoid (logistic) activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.
    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    Logistic = 1. / (1. + np.exp(-x))
    if derivative: #return f'(x), which is as follows
        return Logistic * (1. - Logistic)
    return Logistic #else return the sigmoid (logistic) activation of the x itself

def tanh(x, derivative = False): # reference for this activation function is - https://paperswithcode.com/method/tanh-activation
    """
    Computes and returns the hyperbolic tangent activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.
    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    Hyper = 2. / (1. + np.exp(-2 * x)) - 1. #There were a couple of runtime overflow warnings here (around 5-6) when using tanh(), but the output was alright!
    if derivative: #return derivative of the tanh hyperbole expression
        return (1. - (Hyper ** 2))
    return Hyper # else return the respective activation function of x

def relu(x, derivative = False): # reference for this activation function is - https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/
    param = x
    """
    Computes and returns the rectified linear unit activation function of the given input data x. If derivative = True,
    the derivative of the activation function is returned instead.
    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    if derivative: #return derivative of the ReLU function
        return np.where(param >= 0, 1, 0)
    return np.where(param >= 0, param, 0) # else return the REctified Linear Unit function of the param , which is x itself

def softmax(x, derivative = False): # my reference for this activation function is - https://deepai.org/machine-learning-glossary-and-terms/softmax-layer
    x = np.clip(x, -1e100, 1e100)
    """
    Computes and returns the normalized exponential function of the given input data x, also known as Softmax or Softargmax. If derivative = True,
    the derivative of the activation function is returned instead.
    Args:
        x: A numpy array of shape (n_samples, n_hidden).
        derivative: A boolean representing whether or not the derivative of the function should be returned instead.
    """
    if not derivative: #returns the normalized exponential of x, which is limited into a given range using np.clip function
        c = np.max(x, axis = 1, keepdims = True)
        return np.exp(x - c - np.log(np.sum(np.exp(x - c), axis = 1, keepdims = True)))
    else: # return derivative of the softmax function
        return softmax(x) * (1 - softmax(x))

def cross_entropy(y, p): #Referenced from https://towardsdatascience.com/cross-entropy-loss-function-f38c4ec8643e
    CEL = y.shape[0]
    p = np.clip(p, 1e-15, 1 - 1e-15)
    """
    Computes and returns the cross-entropy loss, defined as the negative log-likelihood of a logistic model that returns
    p probabilities for its true class labels y.
    Args:
        y:
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.
        p:
            A numpy array of shape (n_samples, n_outputs) representing the predicted probabilities from the normalize
            output activation function.
    """
    if len(np.unique(y, axis = 1)) > 2: # more than 2 classes, so we use categorised entropy formula
        return (-1./CEL) * np.sum(y * np.log(p))
    else: # 2 classes, so we use binary entropy formula
        return (-1./CEL) * np.sum((y * np.log(p)) + ((1-y) * np.log(1-p)))

def one_hot_encoding(y): 
    # reference for encoding categorical data into one-hot - https://machinelearningmastery.com/one-hot-encoding-for-categorical-data/
    """
    Converts a vector y of categorical target class values into a one-hot numeric array using one-hot encoding: one-hot
    encoding creates new binary-valued columns, each of which indicate the presence of each possible value from the
    original data.
    Args:
        y: A numpy array of shape (n_samples,) representing the target class values for each sample in the input data.

    Returns:
        A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the input
        data. n_outputs is equal to the number of unique categorical class values in the numpy array y.
    """
    # reference for doing so using Numpy - https://www.educative.io/answers/how-to-convert-an-array-of-indices-to-one-hot-encoded-numpy-array
    
    return np.array([(y == cat) * 1. for cat in np.unique(y)]).T