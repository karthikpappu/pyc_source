# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/modelarts/test/test_manifest_image_classification_detection_get_sample_list.py
# Compiled at: 2019-06-14 07:01:24
import os, sys
from modelarts import manifest, field_name

def check_data(sample_list):
    assert len(sample_list) == 2
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://obs-ma/test/classification/datafiles')
        assert len(label_list) == 1 or len(label_list) == 0


def check_data_usage_inference(sample_list):
    assert len(sample_list) == 3
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://obs-ma/test/classification/datafiles')
        assert len(label_list) == 0


def check_data_usage(sample_list):
    assert len(sample_list) == 2
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://obs-ma/test/classification/datafiles')
        assert len(label_list) == 1


def check_data_without_label(sample_list):
    assert len(sample_list) == 2
    for raw_data, label_list in sample_list:
        assert str(raw_data).startswith('s3://obs-ma/test/classification/datafiles')
        assert len(label_list) == 0 or len(label_list) == 1


def test_multi_default(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', False, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'success: test_multi_default '


def test_multi_default_usage(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', False, usage='Train', *args)
    assert label_type == field_name.multi_lable
    check_data_usage(sample_list)
    print 'success: test_multi_default_usage '


def test_multi_default_usage_inference(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', False, usage='INFERENCE', *args)
    assert label_type == field_name.single_lable
    check_data_usage_inference(sample_list)
    print 'success: test_multi_default_usage_inference '


def test_multi_default_usage3(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', False, usage='all', *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'success: test_multi_default_usage3 '


def test_multi_default_akskep(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'image_classification', access_key=args[0], secret_key=args[1], end_point=args[2])
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'success: test_multi_default '


def test_multi_exactly_match_type(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/image_classification', True, *args)
    assert label_type == field_name.multi_lable
    check_data(sample_list)
    print 'Success: test_multi_exactly_match_type'


def test_multi_exactly_match_type_detect(path, *args):
    sample_list, label_type = manifest.get_sample_list(path, 'modelarts/object_detection', True, *args)
    assert label_type == field_name.multi_lable
    check_data_without_label(sample_list)
    print 'Success: test_multi_exactly_match_type_detect'


def main(argv):
    if len(argv) < 2:
        path2 = os.path.abspath('../../../') + '/resources/classification-detection-multi-xy-V201902220937263726.manifest'
        test_multi_default(path2)
        test_multi_exactly_match_type(path2)
        test_multi_exactly_match_type_detect(path2)
        test_multi_default_usage(path2)
        test_multi_default_usage_inference(path2)
        test_multi_default_usage3(path2)
        print 'test local Success'
    else:
        path2 = 's3://carbonsouth/manifest/classification-detection-multi-xy-V201902220937263726.manifest'
        ak = argv[1]
        sk = argv[2]
        endpoint = argv[3]
        test_multi_default(path2, ak, sk, endpoint)
        test_multi_exactly_match_type(path2, ak, sk, endpoint)
        test_multi_exactly_match_type_detect(path2, ak, sk, endpoint)
        test_multi_default_akskep(path2, ak, sk, endpoint)
        test_multi_default_usage(path2, ak, sk, endpoint)
        test_multi_default_usage_inference(path2, ak, sk, endpoint)
        test_multi_default_usage3(path2, ak, sk, endpoint)
        print 'test OBS Success'


if __name__ == '__main__':
    main(sys.argv)
    print 'Success'