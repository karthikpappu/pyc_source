# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/dimer/nnet/autoencoder_tests.py
# Compiled at: 2013-07-10 19:56:04
from operator import concat
import numpy as np
rng = np.random.RandomState()
import theano, theano.tensor as T, base_test_classes
from autoencoder import AELayer, AutoEncoder, AEStack

class TestAEl(base_test_classes.CNNLayerTester, base_test_classes.NpyTester):

    def setUp(self):
        super(TestAEl, self).setUp()
        self.thrng = T.shared_randomstreams.RandomStreams(self.rng.randint(100))
        self.bs = rng.randint(5, 10)
        self.nin = 20
        self.nout = 10

    def get_input(self):
        return np.asarray(rng.rand(self.bs, self.nin), dtype=np.float64)

    def get_layer(self, cl=0):
        return AELayer(T.matrix('X'), self.nin, self.nout, self.rng, self.thrng, self.get_input().dtype, cl)

    def test_aelinit(self):
        """hr weights are all init'ed to [-thr, thr]"""
        self._weights_inrange(np.sqrt(6.0 / (self.nin + self.nout)), 0)
        self._weights_inrange(0.0, 1)
        self._weights_inrange(0.0, 2)

    def test_init(self):
        self._test_init_()

    def test_norms(self):
        self._test_norms_()

    def test_corruption(self):
        X = T.matrix('X')
        x = self.get_input()
        layer = self.get_layer()
        f = theano.function(inputs=[X], outputs=layer.corrupt(X, 1))
        self.assertZeroArray(f(x))
        f = theano.function(inputs=[X], outputs=layer.corrupt(X, 0))
        self.assertEqualArray(f(x), x)

    def test_activation(self):
        layer = self.get_layer()
        enc_f = theano.function(inputs=[layer.input], outputs=layer.encoder)
        i = self.get_input()
        self.assertEqualArray(theano.function(inputs=[layer.input], outputs=layer.tilde_input)(i), i)
        wv = np.ones(self.zero_weights()[0].shape, self.zero_weights()[0].dtype)
        wv[:, 0] = 0.0
        layer._weights_[0].set_value(wv)
        o = enc_f(i)
        eo = 1.0 / (1 + np.exp(-np.dot(i, wv)))
        print i.shape, wv.shape
        print o
        print eo
        print eo - o
        self.assertAlmostEqual(np.max(np.abs(eo - o)), 0)

    def test_iact(self):
        _identity_size = 5
        ilayer = AELayer(T.matrix('X'), _identity_size, _identity_size, self.rng, self.thrng, self.get_input().dtype, 0)
        wv = np.zeros((_identity_size, _identity_size), self.zero_weights()[0].dtype)
        for _i in range(_identity_size):
            wv[(_i, _i)] = 1

        ilayer._weights_[0].set_value(wv)
        enc_f = theano.function(inputs=[ilayer.input], outputs=ilayer.encoder)
        dec_f = theano.function(inputs=[ilayer.input], outputs=ilayer.decoder)
        i = np.asarray(rng.rand(self.bs, _identity_size), dtype=self.zero_weights()[0].dtype)
        i -= i
        print i.shape, wv.shape
        print wv
        print i
        print
        print
        o = enc_f(i)
        eo = 1.0 / (1 + np.exp(-i))
        print o
        print eo
        print eo - o
        print
        self.assertAlmostEqual(np.max(np.abs(o - eo)), 0)
        o = dec_f(i)
        eo = 1.0 / (1 + np.exp(-eo))
        print o
        print eo
        print eo - o
        self.assertAlmostEqual(np.max(np.abs(o - eo)), 0)

    def speed_update(self):
        pass


class TestAEModel(base_test_classes.ModelTester, base_test_classes.NpyTester):

    def setUp(self):
        super(TestAEModel, self).setUp()
        self.thrng = T.shared_randomstreams.RandomStreams(self.rng.randint(100))
        self.bs = rng.randint(4, 13)
        self.nin = rng.randint(50, 100)
        self.nout = rng.randint(10, 40)
        self.cl = rng.randint(0, 100) / 100.0

    def get_model(self):
        return AutoEncoder(self.nin, self.nout, self.rng, self.thrng, self.get_input().dtype, 0)

    def get_input(self):
        return np.asarray(rng.rand(self.bs, self.nin), dtype=np.float64)

    def get_output(self):
        return np.asarray(rng.rand(self.nout), dtype=self.get_input().dtype)

    def get_gradient_f(self, l1, l2):
        model = self.get_model()
        idx = T.iscalar('batch_idx')
        X = theano.shared(value=self.get_input(), name='X')
        params = reduce(concat, model.get_params())
        return theano.function(inputs=[idx], outputs=T.grad(model.cost(l1, l2), wrt=params), givens={model[0].input: X[self.bs * idx:self.bs * (idx + 1)]})

    def test_update(self):
        model = self.get_model()
        layer = model[0]
        grad_f = self.get_gradient_f(0, 0)
        rho = rng.randint(0, 10) / 10.0
        mu = rng.randint(0, 10) / 10.0
        weights = layer.get_weights()
        self.assertFalse(all(map(lambda s: np.all(s == 0), layer.get_weights())))
        self.assertTrue(all(map(lambda s: np.all(s == 0), layer.get_speeds())))
        grad_v = grad_f(0)
        model.update_params([0], grad_f, mu, rho)
        for i in range(len(grad_v)):
            print i, rho, mu
            self.assertAlmostEqualArray(layer.get_speeds()[i], -rho * grad_v[i])
            self.assertAlmostEqualArray(layer.get_weights()[i] - layer.get_speeds()[i], weights[i])

        weights = layer.get_weights()
        speeds = layer.get_speeds()
        model.update_params([0], grad_f, mu, rho)
        for i in range(len(grad_v)):
            print i, rho, mu
            print layer.get_weights()[i] - layer.get_speeds()[i] - weights[i]
            print np.max(np.abs(layer.get_weights()[i] - layer.get_speeds()[i] - weights[i]))
            self.assertTrue(np.all(layer.get_speeds()[i] == -rho * grad_v[i] + mu * speeds[i]))
            self.assertAlmostEqual(np.max(np.abs(layer.get_weights()[i] - layer.get_speeds()[i] - weights[i])), 0)


class TestAEStackModel(base_test_classes.ModelTester, base_test_classes.NpyTester):

    def setUp(self):
        super(TestAEStackModel, self).setUp()
        self.thrng = T.shared_randomstreams.RandomStreams(self.rng.randint(100))
        self.bs = rng.randint(2, 3)
        self.nin = 100
        self.nhid = (rng.randint(50, 80),
         rng.randint(10, 40),
         rng.randint(2, 4))
        self.nin, self.nhid = 10, (5, 2)
        self.cl = rng.randint(0, 100) / 100.0

    def get_model(self):
        return AEStack(self.nin, self.nhid, self.rng, self.thrng, self.get_input().dtype, 0)

    def get_input(self):
        return np.asarray(rng.rand(self.bs, self.nin), dtype=np.float64)

    def get_output(self):
        return np.asarray(rng.rand(self.nhid[(-1)]), dtype=self.get_input().dtype)

    def test_cost(self):
        l1 = rng.randint(0, 10) / 10
        l2 = rng.randint(0, 10) / 10
        M = self.get_model()
        for layer in M:
            cost = layer.cost
            cf = theano.function(inputs=[M[0].input], outputs=cost(l1, l2))
            cf_00 = theano.function(inputs=[M[0].input], outputs=cost(0, 0))
            w_summ = l1 * layer.weight_norm('l1')
            w_summ_sq = l2 * layer.weight_norm('l2')
            x = self.get_input()
            self.assertEqual(cf(x) - cf_00(x), w_summ + w_summ_sq)

        M = self.zero_model()
        for layer in M:
            cost = layer.cost
            cf = theano.function(inputs=[M[0].input], outputs=cost(l1, l2))
            cf_00 = theano.function(inputs=[M[0].input], outputs=cost(0, 0))
            x = self.get_input()
            self.assertEqual(cf(x), cf_00(x))

    def get_gradient_f(self, l1, l2, lidx):
        model = self.get_model()
        print model.get_params()[lidx]
        grad = T.grad(model[lidx].cost(l1, l2), wrt=model.get_params()[lidx])
        idx = T.iscalar('batch_idx')
        X = theano.shared(value=self.get_input(), name='X')
        givens = {model[0].input: X[self.bs * idx:self.bs * (idx + 1)]}
        return theano.function(inputs=[idx], outputs=grad, givens=givens)

    def _test_layer_update(self, model, lidx):
        layer = model[lidx]
        grad_f = self.get_gradient_f(0, 0, lidx)
        rho = rng.randint(0, 10) / 10.0
        mu = rng.randint(0, 10) / 10.0
        weights = layer.get_weights()
        self.assertFalse(all(map(lambda s: np.all(s == 0), layer.get_weights())))
        self.assertTrue(all(map(lambda s: np.all(s == 0), layer.get_speeds())))
        grad_v = grad_f(0)
        model.update_params([0], grad_f, mu, rho, lidx)
        for i in range(len(grad_v)):
            print i, rho, mu
            self.assertAlmostEqualArray(layer.get_speeds()[i], -rho * grad_v[i])
            self.assertAlmostEqualArray(layer.get_weights()[i] - layer.get_speeds()[i], weights[i])

        weights = layer.get_weights()
        speeds = layer.get_speeds()
        model.update_params([0], grad_f, mu, rho, lidx)
        for i in range(len(grad_v)):
            print i, rho, mu
            print layer.get_weights()[i] - layer.get_speeds()[i] - weights[i]
            print np.max(np.abs(layer.get_weights()[i] - layer.get_speeds()[i] - weights[i]))
            self.assertTrue(np.all(layer.get_speeds()[i] == -rho * grad_v[i] + mu * speeds[i]))
            self.assertAlmostEqual(np.max(np.abs(layer.get_weights()[i] - layer.get_speeds()[i] - weights[i])), 0)

    def test_model_update(self):
        model = self.get_model()
        for i in range(len(model)):
            self._test_layer_update(model, i)

    def test_activation(self):
        model = self.get_model()
        x = self.get_input()
        out_f = []
        grad_f = []
        outvals = []
        for i in range(len(model)):
            out_f.append(theano.function(inputs=[model[0].input], outputs=model[i].activation()))
            grad_f.append(self.get_gradient_f(0, 0, i))
            outvals.append(out_f[(-1)](x))

        self.assertEqual(map(lambda _: _.shape[0], outvals), [
         self.bs] * len(model))
        self.assertEqual(map(lambda _: _.shape[1], outvals), list(self.nhid))
        o0 = out_f[0](x)
        o1 = out_f[1](x)
        w = model[1].get_weights()[0]
        print w
        model.update_params([0], grad_f[1], 0, 0.1, 1)
        print grad_f[1](0)
        print w
        self.assertDifferentArray(w[0], model[1].get_weights()[0])
        self.assertDifferentArray(w[1], model[1].get_weights()[1])
        self.assertEqualArray(o0, out_f[0](x))
        self.assertDifferentArray(o1, out_f[1](x))

    def test_io(self):
        self._test_io()