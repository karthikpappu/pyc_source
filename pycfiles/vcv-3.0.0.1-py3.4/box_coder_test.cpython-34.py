# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/core/box_coder_test.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 2082 bytes
"""Tests for object_detection.core.box_coder."""
import tensorflow as tf
from object_detection.core import box_coder
from object_detection.core import box_list

class MockBoxCoder(box_coder.BoxCoder):
    __doc__ = 'Test BoxCoder that encodes/decodes using the multiply-by-two function.'

    def code_size(self):
        return 4

    def _encode(self, boxes, anchors):
        return 2.0 * boxes.get()

    def _decode(self, rel_codes, anchors):
        return box_list.BoxList(rel_codes / 2.0)


class BoxCoderTest(tf.test.TestCase):

    def test_batch_decode(self):
        mock_anchor_corners = tf.constant([
         [
          0, 0.1, 0.2, 0.3], [0.2, 0.4, 0.4, 0.6]], tf.float32)
        mock_anchors = box_list.BoxList(mock_anchor_corners)
        mock_box_coder = MockBoxCoder()
        expected_boxes = [
         [
          [
           0.0, 0.1, 0.5, 0.6], [0.5, 0.6, 0.7, 0.8]],
         [
          [
           0.1, 0.2, 0.3, 0.4], [0.7, 0.8, 0.9, 1.0]]]
        encoded_boxes_list = [mock_box_coder.encode(box_list.BoxList(tf.constant(boxes)), mock_anchors) for boxes in expected_boxes]
        encoded_boxes = tf.stack(encoded_boxes_list)
        decoded_boxes = box_coder.batch_decode(encoded_boxes, mock_box_coder, mock_anchors)
        with self.test_session() as (sess):
            decoded_boxes_result = sess.run(decoded_boxes)
            self.assertAllClose(expected_boxes, decoded_boxes_result)


if __name__ == '__main__':
    tf.test.main()