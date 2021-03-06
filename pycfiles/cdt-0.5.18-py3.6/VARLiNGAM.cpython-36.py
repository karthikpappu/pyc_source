# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cdt/timeseries/graph/VARLiNGAM.py
# Compiled at: 2020-02-05 06:32:12
# Size of source mod 2**32: 4321 bytes
"""VARLiNGAM algorithm.

Author: Georgios Koutroulis

.. MIT License
..
.. Copyright (c) 2019 Georgios Koutroulis
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
import numpy as np, pandas as pd, networkx as nx
from statsmodels.tsa.vector_ar.var_model import VAR
from ...causality.graph import LiNGAM
from ...causality.graph.model import GraphModel
from ...utils.Settings import SETTINGS

class VarLiNGAM(GraphModel):
    __doc__ = ' Estimate a VAR-LiNGAM\n    Random generate matrix ids to set zeros.\n\n    Args:\n        lag (float): order to estimate the vector autoregressive model\n        verbose (bool): Verbosity of the class. Defaults to SETTINGS.verbose\n\n    .. note::\n       Ref: - A. Hyvarinen, S. Shimizu, P.O. Hoyer ((ICML-2008). Causal modelling\n       combining instantaneous and lagged effects: an identifiable model based\n       on non-Gaussianity;\n       - A. Hyvarinen, K. Zhang, S. Shimizu, P.O. Hoyer (JMLR-2010). Estimation of\n       a Structural Vector Autoregression Model Using Non-Gaussianity;\n     '

    def __init__(self, lag=1, verbose=None):
        self.lag = lag
        self.verbose = SETTINGS.get_default(verbose=verbose)

    def orient_undirected_graph(self, data, graph):
        """Run varLiNGAM on an undirected graph."""
        raise ValueError('VarLiNGAM cannot (yet) be ran with a skeleton/directed graph.')

    def orient_directed_graph(self, data, graph):
        """Run varLiNGAM on a directed_graph."""
        raise ValueError('VarLiNGAM cannot (yet) be ran with a skeleton/directed graph.')

    def create_graph_from_data(self, data):
        """ Run the VarLiNGAM algorithm on data.

        Args:
            data (pandas.DataFrame): time series data

        Returns:
            tuple :(networkx.Digraph, networkx.Digraph) Predictions given by
               the varLiNGAM algorithm: Instantaneous and Lagged causal Graphs
        """
        inst, lagged = self._run_varLiNGAM((data.values), verbose=(self.verbose))
        return (nx.relabel_nodes(nx.DiGraph(inst), {idx:i for idx, i in enumerate(data.columns)}),
         nx.relabel_nodes(nx.DiGraph(lagged), {idx:i for idx, i in enumerate(data.columns)}))

    def _run_varLiNGAM(self, xt, verbose=False):
        """ Run the VarLiNGAM algorithm on data.

        Args:
            xt : time series matrix with size n*m (length*num_variables)

        Returns:
            Tuple: (Bo, Bhat) Instantaneous and lagged causal coefficients

        """
        Ident = np.identity(xt.shape[1])
        model = VAR(xt)
        results = model.fit(self.lag)
        Mt_ = results.params[1:, :]
        resid_VAR = results.resid
        model = LiNGAM(verbose=verbose)
        data = pd.DataFrame(resid_VAR)
        Bo_ = model._run_LiNGAM(data)
        Bhat_ = np.dot(Ident - Bo_, Mt_)
        return (Bo_, Bhat_)