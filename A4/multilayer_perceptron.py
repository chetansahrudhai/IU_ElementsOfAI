# multilayer_perceptron.py: Machine learning implementation of a Multilayer Perceptron classifier from scratch.
# Submitted by: Chetan Sahrudhai Kimidi - ckimidi
# Based on skeleton code by CSCI-B 551 Fall 2022 Course Staff

import numpy as np
from utils import identity, sigmoid, tanh, relu, softmax, cross_entropy, one_hot_encoding
# References : https://www.sciencedirect.com/topics/computer-science/multilayer-perceptron and class lectures and online open-source resources, all listed in report!
class MultilayerPerceptron:
    """
    A class representing the machine learning implementation of a Multilayer Perceptron classifier from scratch.
    Attributes:
        n_hidden
            An integer representing the number of neurons in the one hidden layer of the neural network.
        hidden_activation
            A string representing the activation function of the hidden layer. The possible options are
            {'identity', 'sigmoid', 'tanh', 'relu'}.
        n_iterations
            An integer representing the number of gradient descent iterations performed by the fit(X, y) method.
        learning_rate
            A float representing the learning rate used when updating neural network weights during gradient descent.
        _output_activation
            An attribute representing the activation function of the output layer. This is set to the softmax function
            defined in utils.py.
        _loss_function
            An attribute representing the loss function used to compute the loss for each iteration. This is set to the
            cross_entropy function defined in utils.py.
        _loss_history
            A Python list of floats representing the history of the loss function for every 20 iterations that the
            algorithm runs for. The first index of the list is the loss function computed at iteration 0, the second
            index is the loss function computed at iteration 20, and so on and so forth. Once all the iterations are
            complete, the _loss_history list should have length n_iterations / 20.
        _X
            A numpy array of shape (n_samples, n_features) representing the input data used when fitting the model. This
            is set in the _initialize(X, y) method.
        _y
            A numpy array of shape (n_samples, n_outputs) representing the one-hot encoded target class values for the
            input data used when fitting the model.
        _h_weights
            A numpy array of shape (n_features, n_hidden) representing the weights applied between the input layer
            features and the hidden layer neurons.
        _h_bias
            A numpy array of shape (1, n_hidden) representing the weights applied between the input layer bias term
            and the hidden layer neurons.
        _o_weights
            A numpy array of shape (n_hidden, n_outputs) representing the weights applied between the hidden layer
            neurons and the output layer neurons.
        _o_bias
            A numpy array of shape (1, n_outputs) representing the weights applied between the hidden layer bias term
            neuron and the output layer neurons.
    Methods:
        _initialize(X, y)
            Function called at the beginning of fit(X, y) that performs one-hot encoding for the target class values and
            initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).
        fit(X, y)
            Fits the model to the provided data matrix X and targets y.
        predict(X)
            Predicts class target values for the given test data matrix X using the fitted classifier model. 
    Additional methods created: 
        PropagateNext(self, reps)
            Method used for propagating forward in the multilayer perceptron network
        PropagateBack(self)
            Method used for propagating the feedback on error, backwards in the network
    """

    def __init__(self, n_hidden = 16, hidden_activation = 'sigmoid', n_iterations = 1000, learning_rate = 0.01):
        # Create a dictionary linking the hidden_activation strings to the functions defined in utils.py
        activation_functions = {'identity': identity, 'sigmoid': sigmoid, 'tanh': tanh, 'relu': relu}
        # Check if the provided arguments are valid
        if not isinstance(n_hidden, int) \
                or hidden_activation not in activation_functions \
                or not isinstance(n_iterations, int) \
                or not isinstance(learning_rate, float):
            raise ValueError('The provided class parameter arguments are not recognized.')
        # Define and setup the attributes for the MultilayerPerceptron model object
        self.n_hidden = n_hidden
        self.hidden_activation = activation_functions[hidden_activation]
        self.n_iterations = n_iterations
        self.learning_rate = learning_rate
        self._output_activation = softmax
        self._loss_function = cross_entropy
        self._loss_history = []
        self._X = None
        self._y = None
        self._h_weights = None
        self._h_bias = None
        self._o_weights = None
        self._o_bias = None
        self.HiddenInput = None
        self.OutputInput = None
        self.HiddenOutput = None
        self.OutputOutput = None

    def _initialize(self, X, y):
        """
        Function called at the beginning of fit(X, y) that performs one hot encoding for the target class values and
        initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).
        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.
        Returns:
            None.
        """
        self._X = X
        self._y = one_hot_encoding(y)
        
        # HIDDEN LAYER INITIALIZATION
        if self.hidden_activation.__name__ in ['sigmoid', 'tanh']:
            min, max = -(1.0 / np.sqrt(self._X.shape[1])), (1.0 / np.sqrt(self._X.shape[1]))
            self._h_weights = min + (np.random.rand(self._X.shape[1],self.n_hidden) * (max - min))
        elif self.hidden_activation.__name__ in ['relu']:
            RFactor = np.sqrt(2.0 / self._X.shape[1])
            self._h_weights = np.random.rand(self._X.shape[1],self.n_hidden) * RFactor
        else:
            self._h_weights = np.random.rand(self._X.shape[1],self.n_hidden)
        self._h_bias = np.zeros((1, self.n_hidden))
        
        # OUTPUT LAYER INITIALIZATION
        if self._output_activation.__name__ in ['sigmoid', 'tanh']:
            min, max = -(1.0 / np.sqrt(self.n_hidden)), (1.0 / np.sqrt(self.n_hidden))
            self._o_weights = min + (np.random.rand(self.n_hidden, self._y.shape[1]) * (max - min))
        elif self._output_activation.__name__ in ['relu']:
            RFactor = np.sqrt(2.0 / self.n_hidden)
            self._o_weights = np.random.rand(self.n_hidden, self._y.shape[1]) * RFactor
        else:
            self._o_weights = np.random.rand(self.n_hidden, self._y.shape[1])
        self._o_bias = np.zeros((1, self._y.shape[1]))
        
        np.random.seed(42)

    def PropagateNext(self, reps): #reps is for the number of iterations
        # Layer 1 to 2
        self.HiddenInput = np.dot(self._X, self._h_weights) + self._h_bias
        self.HiddenOutput = self.hidden_activation(self.HiddenInput)
        # Layer 2 to 3
        self.OutputInput = np.dot(self.HiddenOutput, self._o_weights) + self._o_bias
        self.OutputOutput = self._output_activation(self.OutputInput)
        # Error calculation for further usage while back propagation
        E = self._loss_function(self._y, self.OutputOutput)
        if reps % 20 == 0: #This is like an error log in the form of a list, so appending all errors into this _loss_history[]
            self._loss_history.append(E)

    def PropagateBack(self):
        # Back propagation step for the changes in output layer i.e. layer-3, where the factor is calculated for changing the respectives weights and biases.
        OutputFactor = (self.OutputOutput -  self._y) * self._output_activation(self.OutputInput, derivative=True)
        OutputWeightChanges = np.dot(self.HiddenOutput.T, OutputFactor) 
        OutputBiasChanges = np.sum(OutputFactor, axis=0, keepdims=True)
        self._o_weights = self._o_weights - (self.learning_rate * OutputWeightChanges)
        self._o_bias = self._o_bias - (self.learning_rate * OutputBiasChanges)
        # Back propagation step for the changes in hidden layer i.e. layer-2, where the factor is calculated for changing the respectives weights and biases.
        HiddenError = np.dot(OutputFactor, self._o_weights.T)
        HiddenFactor = HiddenError * self.hidden_activation(self.HiddenInput, derivative=True)
        HiddenWeightChanges = np.dot(self._X.T, HiddenFactor) 
        HiddenBiasChanges = np.sum(HiddenFactor, axis=0, keepdims=True)
        self._h_weights = self._h_weights - (self.learning_rate * HiddenWeightChanges)
        self._h_bias = self._h_bias - (self.learning_rate * HiddenBiasChanges)
    
    def fit(self, X, y):
        """
        Fits the model to the provided data matrix X and targets y and stores the cross-entropy loss every 20
        iterations.
        Args:
            X: A numpy array of shape (n_samples, n_features) representing the input data.
            y: A numpy array of shape (n_samples,) representing the true class values for each sample in the input data.
        Returns:
            None.
        """
        self._initialize(X, y)
        for reps in range(self.n_iterations): #using features of the fully connected feed-forward network (MLP network), which are:
            self.PropagateNext(reps) #forward propagation and
            self.PropagateBack() # backward propagation
    
    def predict(self, X):
        """
        Predicts class target values for the given test data matrix X using the fitted classifier model.
        Args:
            X: A numpy array of shape (n_samples, n_features) representing the test data.
        Returns:
            A numpy array of shape (n_samples,) representing the predicted target class values for the given test data.
        """
        PredictionL2 = np.dot(X, self._h_weights) + self._h_bias # Input layer to Hidden layer prediction
        PredictionL2 = self.hidden_activation(PredictionL2) # Applying activation function
        PredictionL3 = np.dot(PredictionL2, self._o_weights) + self._o_bias # Output layer prediction
        PredictionL3 = self._output_activation(PredictionL3) # Applying activation function
        PredictionFinalResult = np.argmax(PredictionL3, axis=1) #Final step where the prediction is done for the iris/digits datasets
        
        return PredictionFinalResult