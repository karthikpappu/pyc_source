# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_eye.py
# Compiled at: 2018-05-24 09:15:44
import numpy as np

def get_opening_degree(eye_matrix):
    eye_matrix = eye_matrix.astype(float)
    up_data = eye_matrix[5] + eye_matrix[4] - eye_matrix[2] - eye_matrix[1]
    down_data = eye_matrix[3] - eye_matrix[0] + 0.1
    return up_data[1] / down_data[0]


def has_closed_eye(face_landmarks):
    open_degree = np.array([0.0, 0.0])
    eye_matrix = np.array(face_landmarks['left_eye'])
    open_degree[0] = get_opening_degree(eye_matrix)
    eye_matrix = np.array(face_landmarks['right_eye'])
    open_degree[1] = get_opening_degree(eye_matrix)
    score = open_degree.mean()
    return (
     score > 0.43, score)