# This code is under MIT License and free to use as it is, the code have been written by Liam Nordvall 
# together with Lord Hummer. The module includes most of the functions needed for everything from basic
# Neural Networks to more deep networks with many layers and nodes.


import numpy as np


# This class consists of all the necessary activation functions needed, we have put them into different
# methods to make it easy to use together with other modules. We made the methods ready to use but also 
# added additional parameters for our professional users.

class ActivationFunctions:

    def __init__(self):
        pass

    # Only returns the values for layers without activation
    def none(self, values):
        return values

    # Non-linear Activation Functions

    def elu(self, values, a=0.1, gradient=1):
        values = np.array(values, dtype=float)
        data = np.where(values > 0, values*gradient, a*(np.exp(values)-1))
        return data

    def hardsigmoid(self, values):
        values = np.array(values)
        data = np.maximum(0, np.minimum(1, (values  + 2) / 4))
        return data

    def hardtahn(self, values, min_value=-1, max_value=1):
        values = np.array(values)
        data = np.where(values > max_value, 1, np.where(values < min_value, -1, values))
        return data

    def hardswish(self, values):
        values = np.array(values)
        data = np.where(values <= -3, 0, np.where(values >= 3, values, (values * (values+3))/6))
        return data

    def logsigmoid(self, values):
        values = np.array(values)
        data = np.log(1/(1+np.exp(-values)))
        return data

    def sigmoid(self, values):
        values = np.array(values)
        data = 1 / (1 + np.exp(-values))
        return data

    def relu(self, values, gradient=1):
        values = np.array(values, dtype=float)
        data = np.where(values > 0, values*gradient, 0)
        return data
    
    def tanh(self, values):
        values = np.array(values)
        data = 2/(1 + np.exp(-2*values)) - 1
        return data

    def binarystep(self, values):
        values = np.array(values, dtype=float)
        data = np.heaviside(values, 1)
        return data

    def linear(self, values, gradient=2):
        return np.array(values, dtype=float)*gradient


    def leakyrelu(self, values, gradient=1, leak=0.01):
        values = np.array(values, dtype=float)
        data = np.where(values > 0, values*gradient, values*leak)    
        return data                      

    def swish(self, values):
        values = np.array(values, dtype=float)
        data = values/(1-np.exp(-values))
        return data

    # Linear Activation Functions 

    def softmax(self, values):
        values = np.array(values)
        data = np.exp(values) / np.exp(values).sum()
        return data


# We initialize the class with a keyword for easier use, namely, instead of writing activation = ActivationFunctions() 
# you just import activation class from Tipo.Functional to get access to all the activation functions

activation = ActivationFunctions()


# This class includes all the important Loss and Cost functions, we have made the use of these functions
# much easier by naming the methods to relevant names and using few parameters but at the same time giving 
# more parameters for fine-tuning to our professional users.


class LossFunctions:

  def __init__(self):
       pass

  def MAELoss(self):
    def MAELossCall(true_value, prediction):
        true_value, prediction = np.array(true_value), np.array(prediction)
        return np.mean(np.abs(true_value - prediction))
    return MAELossCall

  def MSELoss(self):
    def MSELossCall(true_value, prediction):
        true_value, prediction = np.array(true_value), np.array(prediction)
        return np.square(true_value - prediction).mean()
    return MSELossCall

  def MBELoss(self):
    def MBELossCall(true_value, prediction):
        true_value, prediction = np.array(true_value), np.array(prediction)
        return (true_value - prediction).mean()
    return MBELossCall
    

loss = LossFunctions()

