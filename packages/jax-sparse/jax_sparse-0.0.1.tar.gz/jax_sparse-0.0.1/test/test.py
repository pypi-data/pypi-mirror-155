# coding=utf-8
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"

from jax_sparse.sparse_matrix import SparseMatrix
import jax

import jax.numpy as jnp

key = jax.random.PRNGKey(123)

x = jax.random.normal(key, [10, 5])
edge_index = [
    [0, 0, 1, 1, 2, 3, 4, 5, 6],
    [0, 1, 2, 5, 2, 4, 5, 1, 2]
]

adj = SparseMatrix(edge_index, shape=[10, 10])
print(adj @ x)