# Convolutional Neural Networks (CNN)

In deep learning, a convolutional neural network (CNN, or ConvNet) is a class of deep neural networks, most commonly applied to analyzing visual imagery.

## Layers of a CNN

### 1. Convolutional Layer
This layer is the core building block of a CNN. The parameters of the layer consist of a set of learnable filters (or kernels).

### 2. Pooling Layer
Pooling layers are used to reduce the dimensions of the feature maps. Thus, it reduces the number of parameters to learn and the amount of computation performed in the network.
- **Max Pooling**
- **Average Pooling**

### 3. Fully Connected Layer
Neurons in a fully connected layer have full connections to all activations in the previous layer, as seen in regular Neural Networks.

## Comparison

| Feature | CNN | RNN |
| :--- | :--- | :--- |
| **Input** | images, grid-like data | time-series, sequence data |
| **Connections** | sparse connection | recursive connection |
| **Parameter Sharing** | yes | yes |
