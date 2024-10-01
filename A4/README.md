# Assignment 4 - Machine Learning
## Part 1: K-Nearest Neighbors Classification
### Question
![image](https://github.com/user-attachments/assets/abd861fb-8987-411e-811a-599c43475e74)
![image](https://github.com/user-attachments/assets/b1e78bfc-fc8e-4697-a28e-3fb5bd03476b)
![image](https://github.com/user-attachments/assets/78cf8ce5-53b6-4042-951f-1c7ac742e255)

### Solution
As we were given the choice to select between one of the two implementations/approaches we could use, I chose to avoid this part and implement Part-2.

## Part 2: Multilayer Perceptron Classification
### Question
![image](https://github.com/user-attachments/assets/3da13dc1-277a-4d09-9fda-184bc5327e19)
![image](https://github.com/user-attachments/assets/693a125a-cb5a-4048-bdf2-eef605e365ed)
![image](https://github.com/user-attachments/assets/3442a9c1-a49e-4bef-b5e2-d9ee74c82a65)
![image](https://github.com/user-attachments/assets/e239d99a-8988-4bc0-9c33-510a5604ee18)
![image](https://github.com/user-attachments/assets/296108bb-6cad-4a6e-b540-6eaaebb2f739)

### Solution
Basically, a perceptron is a single neuron model, which is the functional unit of today's neural networks and chains. 

These (perceptrons/neurons) have inputs (weighted individually) along with a function for activation of the input, to produce appropriate outputs.  The goal of repeating the said process is to minimize/lessen the error, by altering/squeaking the input weights finely. There is a bias factor included too, which is valued at 1. We have Sigmoid, TanH etc. which are some of the popular functions used for activation. Later, multiple layers of such perceptrons are connected together to give a multilayer perceptron. These neural networks must have three types of layers definitely, which are - INPUT, HIDDEN and OUTPUT. The input layer is a sample of the datasets involved, whereas the hidden layers are for calculations and modifications to reduce error, which are usually not exposed to the dataset directly and then there is the output layer finally, which does what it's name suggests i.e. classifying/labeling into types of outputs.

A diagram of a feedforward fully-connected network is shown below, where the input layer has five nodes corresponding to five input features, the hidden layer has four neurons, and the output layer has three neurons corresponding to three possible target class values. The bias terms are also added on as nodes named with subscript b.

![1](https://github.com/user-attachments/assets/04eebc4c-1071-47bc-808d-b67b39804345)


Once the data is prepared properly, training occurs using batch gradient descent. Forward propagation is performed every iteration, whereas backward propagation occurs when the output error is calculated and sent through the network one layer at a time. The training phase ends when the maximum iterations have been reached. The testing phase can be started now. We predict with data from the new testing datasets. Finally, if there are many perceptrons in the output layer, the output with the highest 'softmax' value is declared as the prediction.

### (1) Formulation of problem: 
Clearly, the problem statement we have at hand is to train a multilayer perceptron model first and then test it over the given datasets, which are IRIS and DIGITS, which have three and ten output categories respectively. So, formulating the problem would involve steps such as deciding how to resolve it (we are using MLP), deciding the activation functions etc. Ultimately, the goal is to implement a feed-forward fully connected neural-net classifier, which involves only 1 hidden layer, as visualized in the above figure. 

### (2) Program working strategy:
We have the following methods to help with the MLP:

_initialize(X, y):

Function called at the beginning of fit(X, y) that performs one-hot encoding for the target class values and
initializes the neural network weights (_h_weights, _h_bias, _o_weights, and _o_bias).

_PropagateNext(self, reps):_

Method used for propagating forward in the multilayer perceptron network

_PropagateBack(self):_

Method used for propagating the feedback on error, backwards in the network_

Then, we initialize weights accordingly to the activation method we have used and we perform one-hot encoding. The purpose of this encoding here is to make best use of our training dataset, allowing ourselves the flexibility to rescale the data and also for getting better predictions instead of just plain labels as outputs.

The activation functions we use/ which are given in the skeleton code are: Linear/ Identity, Hyperbole (TanH), Logistic (Sigmoid), REctified Linear Unit and Softmax.

The core part of the MLP model occurs here:

1. FORWARD PROPAGATION - In the input layer, we add the bias to the weight-multiplied input, This is operated upon in the output layer, as the argument of the activation functions. The functions we use are softmax for the outer layer and others like sigmoid, tanh, relu etc. for the hidden layer.
2. LOSS/ERROR CALCULATION: This is the preceding step before error feedback, you could say. We use cross entropy loss as the main method of calculating the loss, as it is efficient for such categorisation problems.
3. BACKWARD PROPAGATION - Using a learning rate parameter set at 0.01, the error is propagated back into the network and each quantities are modified as part of the tweaking to obtain the best performance.

![2](https://github.com/user-attachments/assets/c316d5e3-0bcd-4ed1-8dc0-f6e8a6365a97)



### (3) Further discussions: 
	
  1. Challenges:
  For me, understanding the working of ReLU and Softmax activation functions took an extra bit of time. Also, the loss calculating part and updating weights and bias factors after each back pass was a technical challenge to pass for me i.e. putting it into the form of code was a bit diffcult, but I used some online references later on. (references listed below!)
  
  2. Assumptions:
  A couple of the primary assumptions we have here is that the combination of the set learning rate parameter and the activation functions we are using are assumed to improve/progress after each weight/bias update and also the other assumption is that the IRIS and DIGITS datasets are appropriately, fully and properly tested upon, without any technical hiccups.
  
  3. Improvements:
The improvement which I came across was to tweak the learning rate to 0.01 and not too high or low since the lower part was performing very sub-par and theoretically on the other side, if the learning rate is too high, we know that we would not be reaching a final solution or an optimal point.

### References for Part-2:
Assignment document (for partial problem statement and the diagram of fully feed forward connected network)

Prof Crandalls lecture materials and skeleton code of CSCI B551 course staff

Linear (Identity) activation function
http://theurbanengine.com/blog/linear-identity-activation

Sigmoid activation function
https://en.wikipedia.org/wiki/Sigmoid_function

Tanh activation function
https://paperswithcode.com/method/tanh-activation

RELU activation function
https://machinelearningmastery.com/rectified-linear-activation-function-for-deep-learning-neural-networks/

Softmax function
https://deepai.org/machine-learning-glossary-and-terms/softmax-layer

Cross entropy loss function
https://towardsdatascience.com/cross-entropy-loss-function-f38c4ec8643e

One-hot encoding function
https://machinelearningmastery.com/one-hot-encoding-for-categorical-data/
https://www.educative.io/answers/how-to-convert-an-array-of-indices-to-one-hot-encoded-numpy-array

Multilayer Perceptron overview
https://www.sciencedirect.com/topics/computer-science/multilayer-perceptron

Medium blog for the very accurate explanation of MLP, and alsof for the GIF above (did not take any code sample from the blog, only the GIF)
https://medium.com/computing-science/using-multilayer-perceptron-in-classification-problems-iris-flower-6fc9fbf36040
