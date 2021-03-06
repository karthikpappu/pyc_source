# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cjld/new_jittor/jittor/python/jittor/test/test_resnet.py
# Compiled at: 2020-04-02 03:47:07
# Size of source mod 2**32: 4993 bytes
import jittor as jt
from jittor import nn, Module
from jittor.models import resnet
import numpy as np, sys, os, random, math, unittest
from jittor.test.test_reorder_tuner import simple_parser
from jittor.test.test_log import find_log_with_re
from jittor.dataset.mnist import MNIST
import jittor.transform as trans
import time
skip_this_test = False

class MnistNet(Module):

    def __init__(self):
        self.model = resnet.Resnet18()
        self.layer = nn.Linear(1000, 10)

    def execute(self, x):
        x = self.model(x)
        x = self.layer(x)
        return x


@unittest.skipIf(skip_this_test, 'skip_this_test')
class TestResnet(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        self.batch_size = 100
        self.weight_decay = 0.0001
        self.momentum = 0.9
        self.learning_rate = 0.1
        self.train_loader = MNIST(train=True, transform=(trans.Resize(224))).set_attrs(batch_size=(self.batch_size),
          shuffle=True)

    def setup_seed(self, seed):
        np.random.seed(seed)
        random.seed(seed)
        jt.seed(seed)

    @unittest.skipIf(not jt.has_cuda, 'Cuda not found')
    @jt.flag_scope(use_cuda=1, use_stat_allocator=1)
    def test_resnet(self):
        global prev
        self.setup_seed(1)
        loss_list = []
        acc_list = []
        mnist_net = MnistNet()
        prev = time.time()
        SGD = nn.SGD(mnist_net.parameters(), self.learning_rate, self.momentum, self.weight_decay)
        for batch_idx, (data, target) in enumerate(self.train_loader):
            output = mnist_net(data)
            loss = nn.cross_entropy_loss(output, target)
            with jt.log_capture_scope(log_silent=1,
              log_v=1,
              log_vprefix='op.cc=100,exe=10') as (logs):
                SGD.step(loss)

                def callback(loss, output, target, batch_idx):
                    pred = np.argmax(output, axis=1)
                    acc = np.sum(target == pred) / self.batch_size
                    loss_list.append(loss[0])
                    acc_list.append(acc)
                    print('Train Epoch: {} [{}/{} ({:.0f}%)]\tLoss: {:.6f}\tAcc: {:.6f} \tTime:{:.3f}'.format(0, batch_idx, 600, 1.0 * batch_idx / 6.0, loss[0], acc, time.time() - prev))

                jt.fetch([loss, output, target], callback, batch_idx)
            log_conv = find_log_with_re(logs, 'Jit op key (not )?found: ((mkl)|(cudnn))_conv.*')
            log_matmul = find_log_with_re(logs, 'Jit op key (not )?found: ((mkl)|(cublas))_matmul.*')
            if batch_idx:
                raise len(log_conv) == 59 and len(log_matmul) == 6 or AssertionError((len(log_conv), len(log_matmul)))
            mem_used = jt.flags.stat_allocator_total_alloc_byte - jt.flags.stat_allocator_total_free_byte
            assert mem_used < 5000000000.0, mem_used
            assert jt.core.number_of_lived_vars() < 3500

        jt.sync_all(True)
        assert np.mean(loss_list[-50:]) < 0.3


if __name__ == '__main__':
    unittest.main()