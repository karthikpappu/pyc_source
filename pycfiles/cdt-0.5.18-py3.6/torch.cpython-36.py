# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/utils/torch.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 14459 bytes
"""PyTorch utilities for models.

Author: Diviyan Kalainathan, Olivier Goudet
Date: 09/3/2018

.. MIT License
..
.. Copyright (c) 2018 Diviyan Kalainathan
..
.. Permission is hereby granted, free of charge, to any person obtaining a copy
.. of this software and associated documentation files (the "Software"), to deal
.. in the Software without restriction, including without limitation the rights
.. to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
.. copies of the Software, and to permit persons to whom the Software is
.. furnished to do so, subject to the following conditions:
..
.. The above copyright notice and this permission notice shall be included in all
.. copies or substantial portions of the Software.
..
.. THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
.. IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
.. FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
.. AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
.. LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
.. OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
.. SOFTWARE.
"""
import math, torch as th
from torch.nn import Parameter
from torch.nn.modules.batchnorm import _BatchNorm

def _sample_gumbel(shape, eps=1e-10, out=None):
    """
    Implementation of pytorch.
    (https://github.com/pytorch/pytorch/blob/e4eee7c2cf43f4edba7a14687ad59d3ed61d9833/torch/nn/functional.py)
    Sample from Gumbel(0, 1)
    based on
    https://github.com/ericjang/gumbel-softmax/blob/3c8584924603869e90ca74ac20a6a03d99a91ef9/Categorical%20VAE.ipynb ,
    (MIT license)
    """
    U = out.resize_(shape).uniform_() if out is not None else th.rand(shape)
    return -th.log(eps - th.log(U + eps))


def _gumbel_softmax_sample(logits, tau=1, eps=1e-10):
    """
    Implementation of pytorch.
    (https://github.com/pytorch/pytorch/blob/e4eee7c2cf43f4edba7a14687ad59d3ed61d9833/torch/nn/functional.py)
    Draw a sample from the Gumbel-Softmax distribution
    based on
    https://github.com/ericjang/gumbel-softmax/blob/3c8584924603869e90ca74ac20a6a03d99a91ef9/Categorical%20VAE.ipynb
    (MIT license)
    """
    dims = logits.dim()
    gumbel_noise = _sample_gumbel((logits.size()), eps=eps, out=(logits.data.new()))
    y = logits + gumbel_noise
    return th.softmax(y / tau, dims - 1)


def gumbel_softmax(logits, tau=1, hard=False, eps=1e-10):
    """
    Implementation of pytorch.
    (https://github.com/pytorch/pytorch/blob/e4eee7c2cf43f4edba7a14687ad59d3ed61d9833/torch/nn/functional.py)
    Sample from the Gumbel-Softmax distribution and optionally discretize.
    Args:
      logits: `[batch_size, n_class]` unnormalized log-probs
      tau: non-negative scalar temperature
      hard: if ``True``, take `argmax`, but differentiate w.r.t. soft sample y
    Returns:
      [batch_size, n_class] sample from the Gumbel-Softmax distribution.
      If hard=True, then the returned sample will be one-hot, otherwise it will
      be a probability distribution that sums to 1 across classes
    Constraints:
    - this implementation only works on batch_size x num_features tensor for now
    based on
    https://github.com/ericjang/gumbel-softmax/blob/3c8584924603869e90ca74ac20a6a03d99a91ef9/Categorical%20VAE.ipynb ,
    (MIT license)
    """
    shape = logits.size()
    if not len(shape) == 2:
        raise AssertionError
    else:
        y_soft = _gumbel_softmax_sample(logits, tau=tau, eps=eps)
        if hard:
            _, k = y_soft.data.max(-1)
            y_hard = (logits.data.new)(*shape).zero_().scatter_(-1, k.view(-1, 1), 1.0)
            y = y_hard - y_soft.data + y_soft
        else:
            y = y_soft
    return y


def _sample_logistic(shape, out=None):
    U = out.resize_(shape).uniform_() if out is not None else th.rand(shape)
    return th.log(U) - th.log(1 - U)


def _sigmoid_sample(logits, tau=1):
    """
    Implementation of Bernouilli reparametrization based on Maddison et al. 2017
    """
    dims = logits.dim()
    logistic_noise = _sample_logistic((logits.size()), out=(logits.data.new()))
    y = logits + logistic_noise
    return th.sigmoid(y / tau)


def gumbel_sigmoid(logits, ones_tensor, zeros_tensor, tau=1, hard=False):
    shape = logits.size()
    y_soft = _sigmoid_sample(logits, tau=tau)
    if hard:
        y_hard = th.where(y_soft > 0.5, ones_tensor, zeros_tensor)
        y = y_hard.data - y_soft.data + y_soft
    else:
        y = y_soft
    return y


class ChannelBatchNorm1d(_BatchNorm):
    __doc__ = "Applies Batch Normalization over a 2D or 3D input (a mini-batch of 1D\n    inputs with optional additional channel dimension) as described in the paper\n    `Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift`_ .\n\n    Variant which is adapted for the SAM model, where the Channel dimension is\n    considered as extra-features. Thus considering the input as a\n    `N x (channels * in_features)` tensor.\n\n    .. math::\n        y = \\frac{x - \\mathrm{E}[x]}{\\sqrt{\\mathrm{Var}[x] + \\epsilon}} * \\gamma + \\beta\n\n    The mean and standard-deviation are calculated per-dimension over\n    the mini-batches and :math:`\\gamma` and :math:`\\beta` are learnable parameter vectors\n    of size `C` (where `C` is the input size).\n\n    By default, during training this layer keeps running estimates of its\n    computed mean and variance, which are then used for normalization during\n    evaluation. The running estimates are kept with a default :attr:`momentum`\n    of 0.1.\n\n    If :attr:`track_running_stats` is set to ``False``, this layer then does not\n    keep running estimates, and batch statistics are instead used during\n    evaluation time as well.\n\n    .. note::\n        This :attr:`momentum` argument is different from one used in optimizer\n        classes and the conventional notion of momentum. Mathematically, the\n        update rule for running statistics here is\n        :math:`\\hat{x}_\\text{new} = (1 - \\text{momentum}) \\times \\hat{x} + \\text{momemtum} \\times x_t`,\n        where :math:`\\hat{x}` is the estimated statistic and :math:`x_t` is the\n        new observed value.\n\n    Because the Batch Normalization is done over the `C` dimension, computing statistics\n    on `(N, L)` slices, it's common terminology to call this Temporal Batch Normalization.\n\n    Args:\n        num_features: :math:`C` from an expected input of size\n            :math:`(N, C, L)` or :math:`L` from input of size :math:`(N, L)`\n        eps: a value added to the denominator for numerical stability.\n            Default: 1e-5\n        momentum: the value used for the running_mean and running_var\n            computation. Can be set to ``None`` for cumulative moving average\n            (i.e. simple average). Default: 0.1\n        affine: a boolean value that when set to ``True``, this module has\n            learnable affine parameters. Default: ``True``\n        track_running_stats: a boolean value that when set to ``True``, this\n            module tracks the running mean and variance, and when set to ``False``,\n            this module does not track such statistics and always uses batch\n            statistics in both training and eval modes. Default: ``True``\n\n    Shape:\n        - Input: :math:`(N, C)` or :math:`(N, C, L)`\n        - Output: :math:`(N, C)` or :math:`(N, C, L)` (same shape as input)\n\n    Examples::\n        >>> # With Learnable Parameters\n        >>> m = nn.BatchNorm1d(100)\n        >>> # Without Learnable Parameters\n        >>> m = nn.BatchNorm1d(100, affine=False)\n        >>> input = torch.randn(20, 100)\n        >>> output = m(input)\n\n    .. _`Batch Normalization: Accelerating Deep Network Training by Reducing Internal Covariate Shift`:\n        https://arxiv.org/abs/1502.03167\n    "

    def __init__(self, num_channels, num_features, *args, **kwargs):
        (super(ChannelBatchNorm1d, self).__init__)(num_channels * num_features, *args, **kwargs)
        self.num_channels = num_channels
        self.num_features = num_features

    def _check_input_dim(self, input):
        if input.dim() != 2:
            if input.dim() != 3:
                raise ValueError('expected 2D or 3D input (got {}D input)'.format(input.dim()))

    def forward(self, input):
        _input = input.contiguous().view(-1, self.num_channels * self.num_features)
        output = super(ChannelBatchNorm1d, self).forward(_input)
        return output.view(-1, self.num_channels, self.num_features)


class MatrixSampler(th.nn.Module):
    __doc__ = 'Matrix Sampler, following a Bernoulli distribution. with learnable\n    parameters.\n\n    Args:\n        graph_size (int or tuple): shape of the matrix to sample. If is int,\n           samples a square matrix.\n        mask (torch.Tensor): Allows to forbid some elements to be sampled.\n           Defaults to ``1 - th.eye()``.\n        gumbel (bool): Use either gumbel softmax (True) or gumbel sigmoid (False)\n    Attributes:\n        weights: the learnable weights of the module of shape\n            `(graph_size x graph_size)` if the input was `int` else `(*graph_size)`\n    Shape:\n        - output: `graph_size` if tuple given, else `(graph_size, graph_size)`\n    '

    def __init__(self, graph_size, mask=None, gumbel=False):
        super(MatrixSampler, self).__init__()
        if not isinstance(graph_size, (list, tuple)):
            self.graph_size = (
             graph_size, graph_size)
        else:
            self.graph_size = graph_size
        self.weights = th.nn.Parameter((th.FloatTensor)(*self.graph_size))
        self.weights.data.zero_()
        if mask is None:
            mask = 1 - (th.eye)(*self.graph_size)
        if not (type(mask) == bool and not mask):
            self.register_buffer('mask', mask)
        self.gumble = gumbel
        ones_tensor = (th.ones)(*self.graph_size)
        self.register_buffer('ones_tensor', ones_tensor)
        zeros_tensor = (th.zeros)(*self.graph_size)
        self.register_buffer('zeros_tensor', zeros_tensor)

    def forward(self, tau=1, drawhard=True):
        """Return a sampled graph."""
        if self.gumble:
            drawn_proba = (gumbel_softmax((th.stack([self.weights.view(-1), -self.weights.view(-1)], 1)), tau=tau,
              hard=drawhard)[:, 0].view)(*self.graph_size)
        else:
            drawn_proba = gumbel_sigmoid((2 * self.weights), (self.ones_tensor), (self.zeros_tensor), tau=tau, hard=drawhard)
        if hasattr(self, 'mask'):
            return self.mask * drawn_proba
        else:
            return drawn_proba

    def get_proba(self):
        if hasattr(self, 'mask'):
            return th.sigmoid(2 * self.weights) * self.mask
        else:
            return th.sigmoid(2 * self.weights)

    def set_skeleton(self, mask):
        self.register_buffer('mask', mask)


def functional_linear3d(input, weight, bias=None):
    r"""
    Apply a linear transformation to the incoming data: :math:`y = xA^T + b`.
    Shape:
        - Input: :math:`(N, *, in\_features)` where `*` means any number of
          additional dimensions
        - Weight: :math:`(out\_features, in\_features)`
        - Bias: :math:`(out\_features)`
        - Output: :math:`(N, *, out\_features)`
    """
    output = input.transpose(0, 1).matmul(weight)
    if bias is not None:
        output += bias.unsqueeze(1)
    return output.transpose(0, 1)


class Linear3D(th.nn.Module):
    __doc__ = 'Applies a linear transformation to the incoming data: :math:`y = Ax + b`.\n    Broadcasts following a 3rd dimension. If input is 2d, input is repeated over\n    all channels. This layer is a linear layer with 3D parameters.\n\n    Args:\n        sizes: Triplet of int values defining the shape of the 3D tensor:\n            (channels, in_features, out_features)\n        bias: If set to False, the layer will not learn an additive bias.\n            Default: ``True``\n    Attributes:\n        weight (torch.Tensor): the learnable weights of the module of shape\n          `(out_features x in_features)`\n        bias (torch.Tensor): the learnable bias of the module of shape `(out_features)`\n    Shape:\n        - Input: :math:`(N, *, in\\_features)` where :math:`*` means number of\n          channels or no additional dimension.\n        - Output: :math:`(N, channels, out\\_features)`.\n    Examples::\n        >>> m = cdt.utils.torch.Linear3D(3, 20, 30)\n        >>> input = torch.randn(128, 20)\n        >>> output = m(input)\n        >>> print(output.size())\n    '

    def __init__(self, sizes, bias=True):
        super(Linear3D, self).__init__()
        self.in_features = sizes[1]
        self.out_features = sizes[2]
        self.channels = sizes[0]
        self.weight = Parameter(th.Tensor(self.channels, self.in_features, self.out_features))
        if bias:
            self.bias = Parameter(th.Tensor(self.channels, self.out_features))
        else:
            self.register_parameter('bias', None)
        self.reset_parameters()

    def reset_parameters(self):
        stdv = 1.0 / math.sqrt(self.weight.size(1))
        self.weight.data.uniform_(-stdv, stdv)
        if self.bias is not None:
            self.bias.data.uniform_(-stdv, stdv)

    def forward(self, input, noise=None, adj_matrix=None):
        if input.dim() == 2:
            if noise is None:
                input = input.unsqueeze(1).expand([input.shape[0], self.channels, self.in_features])
            else:
                input = th.cat([
                 input.unsqueeze(1).expand([input.shape[0],
                  self.channels,
                  self.in_features - 1]),
                 noise.unsqueeze(2)], 2)
        if adj_matrix is not None:
            input = input * adj_matrix.t().unsqueeze(0)
        return functional_linear3d(input, self.weight, self.bias)

    def extra_repr(self):
        return 'in_features={}, out_features={}, bias={}'.format(self.in_features, self.out_features, self.bias is not None)