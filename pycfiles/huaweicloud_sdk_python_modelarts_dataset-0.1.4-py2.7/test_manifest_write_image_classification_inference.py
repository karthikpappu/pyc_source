# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_write_image_classification_inference.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts.test import test_manifest_image_classification
from modelarts.manifest import Annotation, Sample, DataSet

def create_manifest():
    size = 0
    sample_list = []
    for i in range(10):
        size = size + 1
        source = 's3://obs-ma/test/classification/datafiles/1_1550650984970_' + str(i) + '.jpg'
        usage = 'TRAIN'
        inference_loc = 's3://obs-ma/test/classification/datafiles/1_1550650984970_' + str(i) + '.txt'
        id = 'XGDVGS' + str(i)
        annotations_list = []
        for j in range(1):
            annotation_type = 'modelarts/image_classification'
            if 0 == i % 2:
                annotation_name = 'Cat'
            else:
                annotation_name = 'Dog'
            annotation_creation_time = '2019-02-20 08:23:06'
            annotation_format = 'manifest'
            annotation_property = {'color': 'black'}
            annotation_confidence = 0.8
            annotated_by = 'human'
            annotations_list.append(Annotation(name=annotation_name, type=annotation_type, confidence=annotation_confidence, creation_time=annotation_creation_time, annotated_by=annotated_by, annotation_format=annotation_format, property=annotation_property))

        sample_list.append(Sample(source=source, usage=usage, annotations=annotations_list, inference_loc=inference_loc, id=id))

    for i in range(9):
        id = 'XGDVGS' + str(i)
        size = size + 1
        source = 's3://obs-ma/test/classification/datafiles/1_1550650984970_' + str(i) + '.jpg'
        usage = 'TRAIN'
        annotations_list = []
        inference_loc = 's3://obs-ma/test/classification/datafiles/1_1550650984970_' + str(i) + '.txt'
        sample_list.append(Sample(source=source, usage=usage, annotations=annotations_list, inference_loc=inference_loc, id=id))

    return DataSet(sample=sample_list, size=size)


def main(argv):
    path = os.path.abspath('../../../') + '/resources/classification-xy-V201902220937263726_3.manifest'
    dataset = create_manifest()
    if len(argv) < 2:
        dataset.save(path)
        para = []
        para.append(path)
        test_manifest_image_classification.main(para)
    else:
        path2 = argv[1]
        ak = argv[2]
        sk = argv[3]
        endpoint = argv[4]
        dataset.save(path2, ak, sk, endpoint)


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'