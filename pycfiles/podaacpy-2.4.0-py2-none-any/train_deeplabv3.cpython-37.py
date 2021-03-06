# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\poda\segmentation\train_deeplabv3.py
# Compiled at: 2019-09-26 09:27:13
# Size of source mod 2**32: 948 bytes
import deeplab as dl
segmentation = dl.DeepLab(num_classes=1, model_path='/home/model/resnet_v2_101/resnet_v2_101.ckpt',
  is_training=True)
train_generator = segmentation.batch_generator(batch_size=4, dataset_path='/home/dataset/part_segmentation/')
val_generator = segmentation.batch_generator(batch_size=4, dataset_path='/home/dataset/part_segmentation/')
segmentation.optimize(subdivisions=10, iterations=10000, best_loss=1000000, train_batch=train_generator, val_batch=val_generator, save_path='/home/model/melon_segmentation/')