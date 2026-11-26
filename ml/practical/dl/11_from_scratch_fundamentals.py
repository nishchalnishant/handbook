"""
DL FROM SCRATCH — no autograd, no nn.Module. Pure NumPy.
Interview use: "implement X by hand" prompts (whiteboard/live-coding mode).
Covers: manual MLP forward+backward, SGD/Adam, cross-entropy/focal loss,
batchnorm, an LSTM cell, and conv2d via im2col.
"""

import numpy as np


# ---------------------------------------------------------------------------
# 1. Manual 2-layer MLP: forward + backward (no autograd)
# ---------------------------------------------------------------------------
def relu(x):
    return np.maximum(0, x)


def relu_grad(x):
    return (x > 0).astype(x.dtype)


def softmax(x):
    z = x - x.max(axis=1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(axis=1, keepdims=True)


class MLP:
    """x -> Linear -> ReLU -> Linear -> softmax, trained with manual backprop."""

    def __init__(self, in_dim, hidden_dim, out_dim, seed=0):
        rng = np.random.default_rng(seed)
        self.W1 = rng.standard_normal((in_dim, hidden_dim)) * np.sqrt(2 / in_dim)
        self.b1 = np.zeros(hidden_dim)
        self.W2 = rng.standard_normal((hidden_dim, out_dim)) * np.sqrt(2 / hidden_dim)
        self.b2 = np.zeros(out_dim)

    def forward(self, x):
        self.x = x
        self.z1 = x @ self.W1 + self.b1
        self.a1 = relu(self.z1)
        self.z2 = self.a1 @ self.W2 + self.b2
        self.probs = softmax(self.z2)
        return self.probs

    def backward(self, y_onehot):
        """Returns grads dict. dL/dz2 for softmax+cross-entropy simplifies to (probs - y)."""
        n = self.x.shape[0]
        dz2 = (self.probs - y_onehot) / n          # (n, out_dim)
        dW2 = self.a1.T @ dz2
        db2 = dz2.sum(axis=0)

        da1 = dz2 @ self.W2.T
        dz1 = da1 * relu_grad(self.z1)
        dW1 = self.x.T @ dz1
        db1 = dz1.sum(axis=0)

        return {"W1": dW1, "b1": db1, "W2": dW2, "b2": db2}

    def params(self):
        return {"W1": self.W1, "b1": self.b1, "W2": self.W2, "b2": self.b2}


def cross_entropy_loss(probs, y_onehot):
    n = probs.shape[0]
    return -np.sum(y_onehot * np.log(probs + 1e-9)) / n


# ---------------------------------------------------------------------------
# 2. Optimizers from scratch: SGD (+momentum) and Adam
# ---------------------------------------------------------------------------
class SGD:
    def __init__(self, lr=0.01, momentum=0.0):
        self.lr = lr
        self.momentum = momentum
        self.velocity = {}

    def step(self, params, grads):
        for k in params:
            v = self.velocity.get(k, np.zeros_like(params[k]))
            v = self.momentum * v - self.lr * grads[k]
            self.velocity[k] = v
            params[k] += v


class Adam:
    def __init__(self, lr=0.001, beta1=0.9, beta2=0.999, eps=1e-8):
        self.lr, self.b1, self.b2, self.eps = lr, beta1, beta2, eps
        self.m, self.v, self.t = {}, {}, 0

    def step(self, params, grads):
        self.t += 1
        for k in params:
            m = self.m.get(k, np.zeros_like(params[k]))
            v = self.v.get(k, np.zeros_like(params[k]))
            m = self.b1 * m + (1 - self.b1) * grads[k]
            v = self.b2 * v + (1 - self.b2) * (grads[k] ** 2)
            self.m[k], self.v[k] = m, v
            m_hat = m / (1 - self.b1 ** self.t)
            v_hat = v / (1 - self.b2 ** self.t)
            params[k] -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)


# ---------------------------------------------------------------------------
# 3. Training loop tying it together
# ---------------------------------------------------------------------------
def train_mlp_demo():
    rng = np.random.default_rng(0)
    X = rng.standard_normal((256, 20))
    y = rng.integers(0, 3, size=256)
    y_onehot = np.eye(3)[y]

    model = MLP(in_dim=20, hidden_dim=32, out_dim=3)
    opt = Adam(lr=0.01)

    for epoch in range(200):
        probs = model.forward(X)
        loss = cross_entropy_loss(probs, y_onehot)
        grads = model.backward(y_onehot)
        opt.step(model.params(), grads)
        if epoch % 50 == 0:
            print(f"epoch {epoch} loss {loss:.4f}")
    return model


# ---------------------------------------------------------------------------
# 4. Focal loss (handles class imbalance) — common "write this function" ask
# ---------------------------------------------------------------------------
def focal_loss(probs, y_onehot, gamma=2.0, alpha=0.25):
    """FL = -alpha * (1-p)^gamma * log(p), for the true class only."""
    p_true = np.sum(probs * y_onehot, axis=1)
    loss = -alpha * (1 - p_true) ** gamma * np.log(p_true + 1e-9)
    return loss.mean()


# ---------------------------------------------------------------------------
# 5. BatchNorm forward + backward from scratch
# ---------------------------------------------------------------------------
class BatchNorm1d:
    def __init__(self, dim, eps=1e-5, momentum=0.9):
        self.gamma = np.ones(dim)
        self.beta = np.zeros(dim)
        self.eps = eps
        self.momentum = momentum
        self.running_mean = np.zeros(dim)
        self.running_var = np.ones(dim)

    def forward(self, x, training=True):
        if training:
            mu = x.mean(axis=0)
            var = x.var(axis=0)
            self.running_mean = self.momentum * self.running_mean + (1 - self.momentum) * mu
            self.running_var = self.momentum * self.running_var + (1 - self.momentum) * var
        else:
            mu, var = self.running_mean, self.running_var

        self.x_centered = x - mu
        self.std_inv = 1.0 / np.sqrt(var + self.eps)
        self.x_norm = self.x_centered * self.std_inv
        return self.gamma * self.x_norm + self.beta

    def backward(self, dout):
        n = dout.shape[0]
        dgamma = np.sum(dout * self.x_norm, axis=0)
        dbeta = np.sum(dout, axis=0)

        dx_norm = dout * self.gamma
        dvar_term = dx_norm * self.x_centered
        dx = (1.0 / n) * self.std_inv * (
            n * dx_norm - dx_norm.sum(axis=0) - self.x_centered * self.std_inv ** 2 * dvar_term.sum(axis=0)
        )
        return dx, dgamma, dbeta


# ---------------------------------------------------------------------------
# 6. LSTM cell from scratch (single timestep)
# ---------------------------------------------------------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class LSTMCell:
    """One timestep of an LSTM. Gates: forget, input, cell-candidate, output."""

    def __init__(self, input_dim, hidden_dim, seed=0):
        rng = np.random.default_rng(seed)
        concat_dim = input_dim + hidden_dim
        scale = np.sqrt(1 / concat_dim)
        # stack all 4 gates' weights together for one matmul
        self.W = rng.standard_normal((concat_dim, 4 * hidden_dim)) * scale
        self.b = np.zeros(4 * hidden_dim)
        self.hidden_dim = hidden_dim

    def forward(self, x, h_prev, c_prev):
        concat = np.concatenate([x, h_prev], axis=1)
        gates = concat @ self.W + self.b
        h = self.hidden_dim
        f_gate = sigmoid(gates[:, 0 * h:1 * h])   # forget
        i_gate = sigmoid(gates[:, 1 * h:2 * h])   # input
        g_gate = np.tanh(gates[:, 2 * h:3 * h])   # candidate
        o_gate = sigmoid(gates[:, 3 * h:4 * h])   # output

        c_next = f_gate * c_prev + i_gate * g_gate
        h_next = o_gate * np.tanh(c_next)
        return h_next, c_next


# ---------------------------------------------------------------------------
# 7. Conv2d forward via im2col (the standard "implement convolution" ask)
# ---------------------------------------------------------------------------
def im2col(x, kh, kw, stride=1, pad=0):
    """x: (N, C, H, W) -> cols: (N, out_h*out_w, C*kh*kw)"""
    n, c, h, w = x.shape
    x_padded = np.pad(x, ((0, 0), (0, 0), (pad, pad), (pad, pad)))
    out_h = (h + 2 * pad - kh) // stride + 1
    out_w = (w + 2 * pad - kw) // stride + 1

    cols = np.zeros((n, out_h, out_w, c, kh, kw))
    for i in range(out_h):
        for j in range(out_w):
            hs, ws = i * stride, j * stride
            cols[:, i, j] = x_padded[:, :, hs:hs + kh, ws:ws + kw]
    return cols.reshape(n, out_h * out_w, -1), out_h, out_w


def conv2d_forward(x, weight, bias, stride=1, pad=0):
    """x: (N, C_in, H, W), weight: (C_out, C_in, kh, kw) -> (N, C_out, out_h, out_w)"""
    n, c_in, h, w = x.shape
    c_out, _, kh, kw = weight.shape

    cols, out_h, out_w = im2col(x, kh, kw, stride, pad)     # (N, out_h*out_w, C_in*kh*kw)
    w_flat = weight.reshape(c_out, -1)                       # (C_out, C_in*kh*kw)

    out = cols @ w_flat.T + bias                              # (N, out_h*out_w, C_out)
    return out.transpose(0, 2, 1).reshape(n, c_out, out_h, out_w)


if __name__ == "__main__":
    train_mlp_demo()

    x = np.random.randn(2, 3, 8, 8)
    w = np.random.randn(4, 3, 3, 3) * 0.1
    b = np.zeros(4)
    out = conv2d_forward(x, w, b, stride=1, pad=1)
    print("conv2d output shape:", out.shape)   # (2, 4, 8, 8)

    cell = LSTMCell(input_dim=10, hidden_dim=16)
    h0 = np.zeros((2, 16))
    c0 = np.zeros((2, 16))
    h1, c1 = cell.forward(np.random.randn(2, 10), h0, c0)
    print("LSTM h shape:", h1.shape)
