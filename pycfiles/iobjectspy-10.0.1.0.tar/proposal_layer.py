# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\BuildAgent\work\test/iobjectspy/ml\vision\_models\faster_rcnn\layer_utils\proposal_layer.py
# Compiled at: 2019-12-31 04:09:01
# Size of source mod 2**32: 3103 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import numpy as np, tensorflow as tf
from model.bbox_transform import bbox_transform_inv, clip_boxes, bbox_transform_inv_tf, clip_boxes_tf
from model.config import cfg
from model.nms_wrapper import nms

def proposal_layer(rpn_cls_prob, rpn_bbox_pred, im_info, cfg_key, _feat_stride, anchors, num_anchors):
    """A simplified version compared to fast/er RCNN
       For details please see the technical report
    """
    if type(cfg_key) == bytes:
        cfg_key = cfg_key.decode('utf-8')
    pre_nms_topN = cfg[cfg_key].RPN_PRE_NMS_TOP_N
    post_nms_topN = cfg[cfg_key].RPN_POST_NMS_TOP_N
    nms_thresh = cfg[cfg_key].RPN_NMS_THRESH
    scores = rpn_cls_prob[:, :, :, num_anchors:]
    rpn_bbox_pred = rpn_bbox_pred.reshape((-1, 4))
    scores = scores.reshape((-1, 1))
    proposals = bbox_transform_inv(anchors, rpn_bbox_pred)
    proposals = clip_boxes(proposals, im_info[:2])
    order = scores.ravel().argsort()[::-1]
    if pre_nms_topN > 0:
        order = order[:pre_nms_topN]
    proposals = proposals[order, :]
    scores = scores[order]
    keep = nms(np.hstack((proposals, scores)), nms_thresh)
    if post_nms_topN > 0:
        keep = keep[:post_nms_topN]
    proposals = proposals[keep, :]
    scores = scores[keep]
    batch_inds = np.zeros((proposals.shape[0], 1), dtype=(np.float32))
    blob = np.hstack((batch_inds, proposals.astype((np.float32), copy=False)))
    return (
     blob, scores)


def proposal_layer_tf(rpn_cls_prob, rpn_bbox_pred, im_info, cfg_key, _feat_stride, anchors, num_anchors):
    if type(cfg_key) == bytes:
        cfg_key = cfg_key.decode('utf-8')
    pre_nms_topN = cfg[cfg_key].RPN_PRE_NMS_TOP_N
    post_nms_topN = cfg[cfg_key].RPN_POST_NMS_TOP_N
    nms_thresh = cfg[cfg_key].RPN_NMS_THRESH
    scores = rpn_cls_prob[:, :, :, num_anchors:]
    scores = tf.reshape(scores, shape=(-1, ))
    rpn_bbox_pred = tf.reshape(rpn_bbox_pred, shape=(-1, 4))
    proposals = bbox_transform_inv_tf(anchors, rpn_bbox_pred)
    proposals = clip_boxes_tf(proposals, im_info[:2])
    indices = tf.image.non_max_suppression(proposals, scores, max_output_size=post_nms_topN, iou_threshold=nms_thresh)
    boxes = tf.gather(proposals, indices)
    boxes = tf.to_float(boxes)
    scores = tf.gather(scores, indices)
    scores = tf.reshape(scores, shape=(-1, 1))
    batch_inds = tf.zeros((tf.shape(indices)[0], 1), dtype=(tf.float32))
    blob = tf.concat([batch_inds, boxes], 1)
    return (
     blob, scores)