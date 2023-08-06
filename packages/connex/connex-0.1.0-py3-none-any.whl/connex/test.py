from typing import Callable, Sequence

from numpy import isin
from network import NeuralNetwork
import jax.nn as jnn
import jax.numpy as jnp
import time

d = {0: 1, 2: 3}
ones = jnp.arange(10)
print(type(jnp.array(0.)))
assert isinstance(ones, Sequence)
assert False


# Specify number of neurons
num_neurons = 12

# Build the adjacency dict
adjacency_dict = {
    0: [1, 2, 3],
    1: [4],
    2: [4, 5],
    4: [6],
    5: [7],
    6: [8, 9],
    7: [10],
    8: [11],
    9: [11],
    10: [11]
}

# Specify the input and output neurons
input_neurons = [0]
output_neurons = [3, 11]

# Create the network
network = NeuralNetwork(
    num_neurons,
    adjacency_dict, 
    input_neurons, 
    output_neurons,
    jnn.relu,
)

class MLP(NeuralNetwork):
    """
    A standard Multi-Layer Perceptron with constant layer width.
    """

    def __init__(
        self,
        input_size: int,
        output_size: int,
        width: int,
        depth: int,
        activation: Callable=jnn.silu,
        output_activation: Callable=lambda x: x,
        dropout_p: float=0.0,
        seed: int=0,
        **kwargs,
    ):
        """**Arguments**:

        - `input_size`: The number of neurons in the input layer.
        - `output_size`: The number of neurons in the output layer.
        - `width`: The number of neurons in each hidden layer.
        - `depth`: The number of hidden layers.
        - `activation`: The activation function applied element-wise to the 
            hidden (i.e. non-input, non-output) neurons. It can itself be a 
            trainable equinox Module.
        - `output_activation`: The activation function applied element-wise to 
            the  output neurons. It can itself be a trainable equinox Module.
        - `seed`: The random seed used to initialize parameters.
        """
        num_neurons = width * depth + input_size + output_size
        input_neurons = jnp.arange(input_size)
        output_neurons_start = num_neurons - output_size
        output_neurons = jnp.arange(output_size) + output_neurons_start
        adjacency_dict = {n: [] for n in range(num_neurons)}
        layer_sizes = [input_size] + ([width] * depth) + [output_size]
        neuron = 0
        for l in range(len(layer_sizes) - 1):
            in_size, out_size = layer_sizes[l], layer_sizes[l + 1]
            row_idx = range(neuron, neuron + in_size)
            col_idx = range(neuron + in_size, neuron + in_size + out_size)
            for r in row_idx:
                adjacency_dict[r] = list(col_idx)
            neuron += in_size

        super().__init__(
            num_neurons,
            adjacency_dict,
            input_neurons,
            output_neurons,
            activation,
            output_activation,
            dropout_p,
            seed,
            **kwargs
        )


network = MLP(1, 1, 32, 2, dropout_p=.0001)


import equinox as eqx
import jax
import jax.numpy as jnp
import optax

# Initialize the optimizer
optim = optax.adam(1e-3)
opt_state = optim.init(eqx.filter(network, eqx.is_array))

# Define the loss function
def loss_fn(model, x, y):
    preds = jax.vmap(model)(x)
    return jnp.mean((preds - y) ** 2)

# Define a single training step
@eqx.filter_jit
def step(model, optim, opt_state, X_batch, y_batch):
    loss, grads = eqx.filter_value_and_grad(loss_fn)(model, X_batch, y_batch)
    updates, opt_state = optim.update(grads, opt_state, model)
    model = eqx.apply_updates(model, updates)
    return model, opt_state, loss

# Toy data
X = jnp.expand_dims(jnp.linspace(0, 2 * jnp.pi, 250), 1)
y = jnp.sin(X)

# Training loop
n_epochs = 1000
for _ in range(n_epochs):
    t0 = time.time()
    network, opt_state, loss = step(network, optim, opt_state, X, y)
    t1 = time.time()
    dt = t1 - t0
    print(f'Loss: {loss}     Time: {dt}s')
