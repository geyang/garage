"""PyTorch Q-functions."""
from garage.torch.q_functions.continuous_mlp_q_function import (
    ContinuousMLPQFunction)
from garage.torch.q_functions.discrete_mlp_q_function import (
    DiscreteMLPQFunction)

__all__ = ['ContinuousMLPQFunction', 'DiscreteMLPQFunction']
