# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\dynn\data\mnist.py
# Compiled at: 2018-09-19 13:24:45
# Size of source mod 2**32: 2515 bytes
"""
MNIST
=====

Various functions for accessing the MNIST dataset.
"""
import os, struct, numpy as np
from .data_util import download_if_not_there
mnist_url = 'http://yann.lecun.com/exdb/mnist/'
mnist_files = {'train_img':'train-images.idx3-ubyte', 
 'train_lbl':'train-labels.idx1-ubyte', 
 'test_img':'t10k-images.idx3-ubyte', 
 'test_lbl':'t10k-labels.idx1-ubyte'}

def download_mnist(path='.', force=False):
    """Downloads mnist from "http://yann.lecun.com/exdb/mnist/"

    Args:
        path (str, optional): Local folder (defaults to ".")
        force (bool, optional): Force the redownload even if the files are
            already at ``path``
    """
    for filename in mnist_files.values():
        download_if_not_there(f"{filename}.gz", mnist_url, path, force=force)


def read_mnist(split, path):
    """Iterates over the MNIST dataset

    Example:

    .. code-block:: python

        for image in read_mnist("training", "/path/to/mnist"):
            train(image)

    Args:
        split (str): Either ``"training"`` or ``"test"``
        path (str): Path to the folder containing the ``*-ubyte`` files

    Returns:
        tuple: image, label
    """
    if not (split is 'test' or split is 'train'):
        raise ValueError('split must be "train" or "test"')
    fname_img = os.path.join(path, mnist_files[f"{split}_img"])
    fname_lbl = os.path.join(path, mnist_files[f"{split}_lbl"])
    with open(fname_lbl, 'rb') as (flbl):
        _, _ = struct.unpack('>II', flbl.read(8))
        lbl = np.fromfile(flbl, dtype=(np.int8))
    with open(fname_img, 'rb') as (fimg):
        _, _, rows, cols = struct.unpack('>IIII', fimg.read(16))
        img = np.multiply(np.fromfile(fimg, dtype=(np.uint8)).reshape(len(lbl), rows, cols), 0.00392156862745098)

    def get_img(idx):
        return (
         lbl[idx], img[idx])

    for i in range(len(lbl)):
        yield get_img(i)


def load_mnist(path):
    """Loads the MNIST dataset

    Returns the train and test set, each as a list of images and labels.
    The images are represented as numpy arrays.

    Args:
        path (str): Path to the folder containing the ``*-ubyte`` files

    Returns:
        tuple: train and test sets
    """
    train_set = [sample for sample in read_mnist('train', path)]
    test_set = [sample for sample in read_mnist('test', path)]
    return (
     train_set, test_set)