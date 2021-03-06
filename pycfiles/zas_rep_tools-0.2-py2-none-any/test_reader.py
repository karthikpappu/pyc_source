# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/egoruni/Desktop/BA/Code/zas-rep-tools/zas_rep_tools/tests/test_reader.py
# Compiled at: 2018-10-25 09:09:03
import unittest, os, logging, codecs, sure, copy
from nose.plugins.attrib import attr
from testfixtures import tempdir, TempDirectory
from distutils.dir_util import copy_tree
from zas_rep_tools.src.classes.reader import Reader
from zas_rep_tools.src.utils.debugger import p, wipd, wipdn, wipdl, wipdo
from zas_rep_tools.src.utils.helpers import LenGen, path_to_zas_rep_tools, get_number_of_streams_adjust_cpu
from zas_rep_tools.src.utils.basetester import BaseTester

class TestZASreaderReader(BaseTester, unittest.TestCase):
    _multiprocess_can_split_ = True

    def setUp(self):
        super(type(self), self).setUp()

    def tearDown(self):
        super(type(self), self).tearDown()

    @attr(status='stable')
    def test_reader_initialisation_000(self):
        self.blogger_corpus()
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode)
        reader.should.be.a(Reader)

    @attr(status='stable')
    def test_lazyreader_from_txt_in_zip_500(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode, read_from_zip=True, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 6
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'working_area' in data
            assert 'age' in data
            assert 'id' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_txt_500(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 6
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'working_area' in data
            assert 'age' in data
            assert 'id' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_txt_for_given_colnames_501(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy(colnames=['text', 'star_constellation', 'gender']):
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 3
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_csv_with_ascii_502(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.csv_blogger_small_fake_set), 'csv', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == len(self.configer.docs_row_values(token=True, unicode_str=True)['blogger'][0])
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'working_area' in data
            assert 'age' in data
            assert 'id' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_csv_with_utf8_503(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.csv_blogger_hightrepetativ_set), 'csv', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == len(self.configer.docs_row_values(token=True, unicode_str=True)['blogger'][0])
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'working_area' in data
            assert 'age' in data
            assert 'id' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_csv_for_given_colnames_504(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.csv_blogger_small_fake_set), 'csv', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy(colnames=['text', 'star_constellation', 'gender']):
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 3
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_xml_with_ascii_505(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.xml_blogger_small_fake_set), 'xml', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 6
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'working_area' in data
            assert 'age' in data
            assert 'id' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_xml_with_utf8_506(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.xml_blogger_hightrepetativ_set), 'xml', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 6
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'working_area' in data
            assert 'age' in data
            assert 'id' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_xml_for_given_colnames_507(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.xml_blogger_small_fake_set), 'xml', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy(colnames=['text', 'star_constellation', 'gender']):
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 3
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_json_with_ascii_508(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.json_blogger_small_fake_set), 'json', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 6
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'working_area' in data
            assert 'age' in data
            assert 'id' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_json_with_utf8_509(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.json_blogger_hightrepetativ_set), 'json', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 6
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'working_area' in data
            assert 'age' in data
            assert 'id' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_json_for_given_colnames_510(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.json_blogger_small_fake_set), 'json', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy(colnames=['text', 'star_constellation', 'gender']):
            if data == end_file_marker:
                continue
            assert isinstance(data, dict)
            assert len(data) == 3
            assert 'text' in data
            assert 'star_constellation' in data
            assert 'gender' in data

    @attr(status='stable')
    def test_lazyreader_from_twitter_json_with_utf8_511(self):
        self.twitter_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_twitter_corp, self.json_twitter_set), 'json', formatter_name='TwitterStreamAPI', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy():
            if data == end_file_marker:
                continue
            assert data and isinstance(data, dict)
            assert 'text' in data
            assert 'u_lang' in data
            assert 'id' in data
            assert 'u_id' in data

    @attr(status='stable')
    def test_lazyreader_from_twitter_json_for_given_colnames_512(self):
        self.twitter_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_twitter_corp, self.json_twitter_set), 'json', formatter_name='TwitterStreamAPI', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy(colnames=['text']):
            if data == end_file_marker:
                continue
            assert data and isinstance(data, dict)
            assert len(data) == 1
            assert 'text' in data

    def test_lazyreader_from_sifter_twitter_csv_with_utf8_513(self):
        self.twitter_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_twitter_corp, 'CSV/zas-rep-tool/sifter'), 'csv', formatter_name='sifter', mode=self.mode, end_file_marker=end_file_marker)
        for data in reader.getlazy(csvdelimiter=';'):
            if data == end_file_marker:
                continue
            assert data and isinstance(data, dict)
            assert 'text' in data
            assert 'u_lang' in data
            assert 'id' in data
            assert 'u_id' in data

    @attr(status='stable')
    def test_getlazy_many_streams_from_csv_also_getted_from_zips_516(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp), 'csv', mode=self.mode, read_from_zip=True, end_file_marker=end_file_marker, send_end_file_marker=True)
        number_of_found_files = reader._get_number_of_left_over_files()
        assert number_of_found_files < 3 and False
        if reader.files_number_in_zips != len(reader.files_to_read_orig):
            assert False
            number_getted_files = len([ row for gen in reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5) for row in gen if row == end_file_marker ])
            assert number_of_found_files != number_getted_files and False
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5)).should.be.equal(get_number_of_streams_adjust_cpu(5, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=3)).should.be.equal(get_number_of_streams_adjust_cpu(3, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=2)).should.be.equal(get_number_of_streams_adjust_cpu(2, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=1)).should.be.equal(get_number_of_streams_adjust_cpu(1, number_of_found_files, 4))
        i = 0
        for gen in reader.getlazy(stream_number=1000, adjust_to_cpu=True, min_files_pro_stream=1):
            for row_dict in gen:
                if row_dict == end_file_marker:
                    i += 1
                    continue
                assert isinstance(row_dict, dict)
                assert 'text' in row_dict
                assert 'star_constellation' in row_dict
                assert 'working_area' in row_dict
                assert 'age' in row_dict
                assert 'id' in row_dict
                assert 'gender' in row_dict

        assert number_of_found_files == i

    @attr(status='stable')
    def test_getlazy_many_streams_from_xml_also_getted_from_zips_517(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp), 'xml', mode=self.mode, read_from_zip=True, end_file_marker=end_file_marker, send_end_file_marker=True)
        number_of_found_files = reader._get_number_of_left_over_files()
        assert number_of_found_files < 3 and False
        if reader.files_number_in_zips != len(reader.files_to_read_orig):
            assert False
            number_getted_files = len([ row for gen in reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5) for row in gen if row == end_file_marker ])
            assert number_of_found_files != number_getted_files and False
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5)).should.be.equal(get_number_of_streams_adjust_cpu(5, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=3)).should.be.equal(get_number_of_streams_adjust_cpu(3, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=2)).should.be.equal(get_number_of_streams_adjust_cpu(2, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=1)).should.be.equal(get_number_of_streams_adjust_cpu(1, number_of_found_files, 4))
        i = 0
        for gen in reader.getlazy(stream_number=1000, adjust_to_cpu=True, min_files_pro_stream=1):
            for row_dict in gen:
                if row_dict == end_file_marker:
                    i += 1
                    continue
                assert isinstance(row_dict, dict)
                assert len(row_dict) == 6
                assert 'text' in row_dict
                assert 'star_constellation' in row_dict
                assert 'working_area' in row_dict
                assert 'age' in row_dict
                assert 'id' in row_dict
                assert 'gender' in row_dict

        assert number_of_found_files == i

    @attr(status='stable')
    def test_getlazy_many_streams_from_txt_also_getted_from_zips_518(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp), 'txt', mode=self.mode, read_from_zip=True, end_file_marker=end_file_marker, send_end_file_marker=True, regex_template='blogger')
        number_of_found_files = reader._get_number_of_left_over_files()
        assert number_of_found_files < 3 and False
        if reader.files_number_in_zips != len(reader.files_to_read_orig):
            assert False
            number_getted_files = len([ row for gen in reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5) for row in gen if row == end_file_marker ])
            assert number_of_found_files != number_getted_files and False
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5)).should.be.equal(get_number_of_streams_adjust_cpu(5, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=3)).should.be.equal(get_number_of_streams_adjust_cpu(3, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=2)).should.be.equal(get_number_of_streams_adjust_cpu(2, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=1)).should.be.equal(get_number_of_streams_adjust_cpu(1, number_of_found_files, 4))
        i = 0
        for gen in reader.getlazy(stream_number=1000, adjust_to_cpu=True, min_files_pro_stream=1):
            for row_dict in gen:
                if row_dict == end_file_marker:
                    i += 1
                    continue
                assert isinstance(row_dict, dict)
                assert len(row_dict) == 6
                assert 'text' in row_dict
                assert 'star_constellation' in row_dict
                assert 'working_area' in row_dict
                assert 'age' in row_dict
                assert 'id' in row_dict
                assert 'gender' in row_dict

        assert number_of_found_files == i

    @attr(status='stable')
    def test_getlazy_many_streams_from_json_also_getted_from_zips_519(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp), 'json', mode=self.mode, read_from_zip=True, end_file_marker=end_file_marker, send_end_file_marker=True)
        number_of_found_files = reader._get_number_of_left_over_files()
        assert number_of_found_files < 3 and False
        if reader.files_number_in_zips != len(reader.files_to_read_orig):
            assert False
            number_getted_files = len([ row for gen in reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5) for row in gen if row == end_file_marker ])
            assert number_of_found_files != number_getted_files and False
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5)).should.be.equal(get_number_of_streams_adjust_cpu(5, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=3)).should.be.equal(get_number_of_streams_adjust_cpu(3, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=2)).should.be.equal(get_number_of_streams_adjust_cpu(2, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=1)).should.be.equal(get_number_of_streams_adjust_cpu(1, number_of_found_files, 4))
        i = 0
        for gen in reader.getlazy(stream_number=1000, adjust_to_cpu=True, min_files_pro_stream=1):
            for row_dict in gen:
                if row_dict == end_file_marker:
                    i += 1
                    continue
                assert isinstance(row_dict, dict)
                assert len(row_dict) == 6
                assert 'text' in row_dict
                assert 'star_constellation' in row_dict
                assert 'working_area' in row_dict
                assert 'age' in row_dict
                assert 'id' in row_dict
                assert 'gender' in row_dict

        assert number_of_found_files == i

    @attr(status='stable')
    def test_getlazy_many_streams_from_txt_without_given_number_of_streams_adjusted_for_current_cpu_520(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode, end_file_marker=end_file_marker, send_end_file_marker=True)
        number_of_found_files = reader._get_number_of_left_over_files()
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=3)).should.be.equal(get_number_of_streams_adjust_cpu(3, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=5)).should.be.equal(get_number_of_streams_adjust_cpu(3, number_of_found_files, 5))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=3)).should.be.equal(get_number_of_streams_adjust_cpu(3, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=2)).should.be.equal(get_number_of_streams_adjust_cpu(2, number_of_found_files, 4))
        len(reader.getlazy(stream_number=4, adjust_to_cpu=True, min_files_pro_stream=1)).should.be.equal(get_number_of_streams_adjust_cpu(1, number_of_found_files, 4))
        i = 0
        for gen in reader.getlazy(stream_number=1000, adjust_to_cpu=True, min_files_pro_stream=1):
            for row_dict in gen:
                if row_dict == end_file_marker:
                    i += 1
                    continue
                assert isinstance(row_dict, dict)
                assert len(row_dict) == 6
                assert 'text' in row_dict
                assert 'star_constellation' in row_dict
                assert 'working_area' in row_dict
                assert 'age' in row_dict
                assert 'id' in row_dict
                assert 'gender' in row_dict

        assert number_of_found_files == i

    @attr(status='stable')
    def test_getlazy_many_streams_from_txt_with_given_number_of_streams_without_adjust_for_current_cpu_521(self):
        self.blogger_corpus()
        end_file_marker = -1
        reader = Reader(os.path.join(self.tempdir_blogger_corp, self.txt_blogger_small_fake_set), 'txt', regex_template='blogger', mode=self.mode, end_file_marker=end_file_marker, send_end_file_marker=True)
        number_of_found_files = reader._get_number_of_left_over_files()
        len(reader.getlazy(stream_number=3, adjust_to_cpu=False)).should.be.equal(3)
        len([ rowdict for gen in reader.getlazy(stream_number=3, adjust_to_cpu=False) for rowdict in gen if end_file_marker == rowdict ]).should.be.equal(number_of_found_files)
        len(reader.getlazy(stream_number=2, adjust_to_cpu=False)).should.be.equal(2)
        len([ rowdict for gen in reader.getlazy(stream_number=2, adjust_to_cpu=False) for rowdict in gen if end_file_marker == rowdict ]).should.be.equal(number_of_found_files)
        i = 0
        for gen, fname in zip(reader.getlazy(stream_number=3, adjust_to_cpu=False, min_files_pro_stream=1), reversed(reader.files_to_read_orig)):
            for row_dict in gen:
                if row_dict == end_file_marker:
                    i += 1
                    continue
                t = codecs.open(fname, 'r', encoding='utf-8').read()
                assert row_dict['text'] == t
                assert isinstance(row_dict, dict)
                assert len(row_dict) == 6
                assert 'text' in row_dict
                assert 'star_constellation' in row_dict
                assert 'working_area' in row_dict
                assert 'age' in row_dict
                assert 'id' in row_dict
                assert 'gender' in row_dict

        assert number_of_found_files == i