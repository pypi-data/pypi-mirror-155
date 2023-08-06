# Tipo

This is an library including important functions used in ML and Deep Learning,
The library consist of every tool necessary for your research in AI,
everything from activation function and loss functions to complex
back propagation and easy to use forward propagation methods.


## Installation
To download the library you use the following command, because of frequent updates we recommend to use the     ```--upgrade``` syntax
```
  pip install --upgrade tipo
```

## Usage
The Tipo Library is a very easy to use and efficent research tool for AI researchers, it includes a fully customizable forward propagations system using our new module named Node, combining that with our Functional module that consists of all necessarry functions and methods to create a fully working AI. 

The ```Tipo.Functional``` supports many activation and cost functions to use them simply use the script
```python
# Imports the Functional modules
from Tipo.Functional import activation, loss

# Outputs the activation of a certain neuron
scores = activation.relu(neuron)

# Compares the score with the actual answer
loss = loss.meanSquareError(scores, answer)
```

Using these basic methods togheter with the Node module, we get all the necessarry tools for an neural network.

The ```Tipo.Node``` support many different layer type such as convolutional layers and linear layers. To use the Node Module we first import the library using 

```python
  #imports the Node Module
  import tipo.Node
```
Now we are ready to use the module, the first step is to build our network and the recommended way of doing this is to use classes
```python
class NeuralNet():
    def __init__(self, data):
        self.data = data
        self.fc1 = N.LinearPass(4, 6)
        self.fc2 = N.LinearPass(6, 4)

    def forward(self):
        self.fc1.passData(activation.relu(self.data))
        self.fc2.passData(activation.relu(self.fc1.output))

        return self.fc2.output
```
This is how easy it is to set up an network, now we can use this network to make predictions etc.


## Recuirements
- Python 3.0+


## To round of
This library was developed in collaboration with my research team, we will continue the development of this library and have many cool features that we want to implement if you have any ideas or want to be part of our project then contact us at my email liam_nordvall@hotmail.com. Have an awesome day!


## Example
First we import the necesssary libraries
```Python 
from tipo.Functional import activation, loss
import tipo.Node as N
```
Then we use some example data and set up the network structure
```Python
# Example data
data = [[1.0, 2.0, 3.0, 2.5], [2.0, 5.0, -1.0, 2.0], [-1.2, 2.4, 1.5, -2.0]]


# Neural Network
class NeuralNet():
    def __init__(self):
        # initializing the network layers
        self.fc1 = N.LinearPass(4, 16)
        self.fc2 = N.LinearPass(16, 16)
        self.fc3 = N.LinearPass(16, 4)
```
We then initialize the forward propagation
```Python
    def forward(self, batch):
        # Setting up our forward propagation
        self.fc1.passData(activation.relu(batch))
        self.fc2.passData(activation.relu(self.fc1.output))
        self.fc3.passData(self.fc2.output)

        return self.fc3.output

``` 
Now we setup the network and forwards some data trougth it 
```python
# Initlizing Neural Network and forward propagation
NN = NeuralNet()
output = NN.forward(data)
```
We then use some functions from the ```tipo.Functional``` library to calculate the loss
```python

# Finding the loss of our predictions using the MSE function
criterion = loss.MSELoss()
score = criterion(data, output)

```
Thats how easy it is to set up an neural network using the Tipo library!









  
