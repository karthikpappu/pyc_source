# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/utils/scanutils.py
# Compiled at: 2020-03-06 02:01:31
# Size of source mod 2**32: 16814 bytes
"""
Utils to mock scans
"""
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '30/09/2019'
import h5py, numpy, os
from xml.etree import cElementTree
import fabio, fabio.edfimage

class _ScanMock:
    __doc__ = 'Base class to mock as scan (radios, darks, refs, reconstructions...)'
    PIXEL_SIZE = 0.457

    def __init__(self, scan_path, n_radio, n_ini_radio=None, n_extra_radio=0, scan_range=360, n_recons=0, n_pag_recons=0, recons_vol=False, dim=200, ref_n=0, dark_n=0, scene='noise'):
        """

        :param scan_path:
        :param n_radio:
        :param n_ini_radio:
        :param n_extra_radio:
        :param scan_range:
        :param n_recons:
        :param n_pag_recons:
        :param recons_vol:
        :param dim:
        :param ref_n:
        :param dark_n:
        :param str scene: scene type.
                          * 'noise': generate radios from numpy.random
                          * `increase value`: first frame value will be0, then second 1...
                          * `arange`: arange through frames
                          * 'perfect-sphere: generate a sphere which just fit in the
                          detector dimensions
        TODO: add some differente scene type.
        """
        self.det_width = dim
        self.det_height = dim
        self.scan_path = scan_path
        self.n_radio = n_radio
        self.scene = scene
        if not os.path.exists(scan_path):
            os.mkdir(scan_path)
        self.write_metadata(n_radio=n_radio, scan_range=scan_range, ref_n=ref_n,
          dark_n=dark_n)
        if n_ini_radio:
            for i_radio in range(n_ini_radio):
                self.add_radio(i_radio)

        for i_extra_radio in range(n_extra_radio):
            self.add_radio(i_extra_radio)

        for i_recons in range(n_recons):
            self.add_reconstruction(i_recons)

        for i_recons in range(n_pag_recons):
            self.add_pag_reconstruction(i_recons)

        if recons_vol is True:
            self.add_recons_vol()

    def add_radio(self, index=None):
        raise NotImplementedError('Base class')

    def add_reconstruction(self, index=None):
        raise NotImplementedError('Base class')

    def add_pag_reconstruction(self, index=None):
        raise NotImplementedError('Base class')

    def add_recons_vol(self):
        raise NotImplementedError('Base class')

    def write_metadata(self, n_radio, scan_range, ref_n, dark_n):
        raise NotImplementedError('Base class')

    def end_acquisition(self):
        raise NotImplementedError('Base class')

    def _get_radio_data(self, index):
        if self.scene == 'noise':
            return numpy.random.random(self.det_height * self.det_width).reshape((self.det_width, self.det_height))
        if self.scene == 'increasing value':
            return numpy.zeros((self.det_width, self.det_height)) + index
        if self.scene == 'arange':
            start = index * (self.det_height * self.det_width)
            stop = (index + 1) * (self.det_height * self.det_width)
            return numpy.arange(start=start, stop=stop).reshape(self.det_width, self.det_height)
        if self.scene == 'perfect-sphere':
            background = numpy.zeros(self.det_height * self.det_width)
            radius = min(background.shape)

            def _compute_radius_to_center(data):
                assert data.ndim is 2
                xcenter = data.shape[2] // 2
                ycenter = data.shape[1] // 2
                y, x = numpy.ogrid[:data.shape[0], :data.shape[1]]
                r = numpy.sqrt((x - xcenter) ** 2 + (y - ycenter) ** 2)
                return r

            radii = _compute_radius_to_center(background)
            scale = 1
            background[radii < radius * scale] = 1.0
            return background
        raise ValueError('selected scene %s is no managed' % self.scene)


class MockHDF5(_ScanMock):
    __doc__ = '\n    Mock an acquisition in a hdf5 file\n    '

    def __init__(self, scan_path, n_radio, n_ini_radio=None, n_extra_radio=0, scan_range=360, n_recons=0, n_pag_recons=0, recons_vol=False, dim=200):
        self.scan_master_file = os.path.join(scan_path, os.path.basename(scan_path) + '.h5')
        super(MockHDF5, self).__init__(scan_path=scan_path, n_radio=n_radio, n_ini_radio=n_ini_radio,
          n_extra_radio=n_extra_radio,
          scan_range=scan_range,
          n_recons=n_recons,
          n_pag_recons=n_pag_recons,
          recons_vol=recons_vol,
          dim=dim)

    def add_radio(self, index=None):
        radio = self._get_radio_data(index=index)
        radio = radio.reshape((1, self.det_height, self.det_width))
        with h5py.File(self.scan_master_file, 'r+') as (h5_file):
            if '1_tomo/measurement/pcoedge64:image' in h5_file:
                current_dataset = h5_file['1_tomo/measurement/pcoedge64:image'][()]
                del h5_file['1_tomo/measurement/pcoedge64:image']
                new_dataset = numpy.append(current_dataset, radio)
                shape = list(current_dataset.shape)
                shape[0] += 1
                new_dataset = new_dataset.reshape(shape)
            else:
                new_dataset = radio
        with h5py.File(self.scan_master_file, 'a') as (h5_file):
            h5_file['1_tomo/measurement/pcoedge64:image'] = new_dataset

    def write_metadata(self, n_radio, scan_range, ref_n, dark_n):
        with h5py.File(self.scan_master_file, 'a') as (h5_file):
            h5_file['1_tomo/scan_meta/technique/scan/tomo_n'] = n_radio
            h5_file['1_tomo/scan_meta/technique/scan/scan_range'] = scan_range
            h5_file['1_tomo/scan_meta/technique/scan/ref_n'] = ref_n
            h5_file['1_tomo/scan_meta/technique/scan/dark_n'] = dark_n
            h5_file['1_tomo/scan_meta/technique/detector/size'] = (self.det_width, self.det_height)
            h5_file['1_tomo/scan_meta/technique/detector/pixel_size'] = _ScanMock.PIXEL_SIZE
            h5_file['1_tomo/scan_meta/technique/detector/ref_on'] = str(n_radio)

    def end_acquisition(self):
        pass


class MockEDF(_ScanMock):
    __doc__ = 'Mock a EDF acquisition\n    '
    _RECONS_PATTERN = '_slice_'
    _PAG_RECONS_PATTERN = '_slice_pag_'

    def __init__(self, scan_path, n_radio, n_ini_radio=None, n_extra_radio=0, scan_range=360, n_recons=0, n_pag_recons=0, recons_vol=False, dim=200, scene='noise'):
        self._last_radio_index = -1
        super(MockEDF, self).__init__(scan_path=scan_path, n_radio=n_radio,
          n_ini_radio=n_ini_radio,
          n_extra_radio=n_extra_radio,
          scan_range=scan_range,
          n_recons=n_recons,
          n_pag_recons=n_pag_recons,
          recons_vol=recons_vol,
          dim=dim,
          scene=scene)

    def get_info_file(self):
        return os.path.join(self.scan_path, os.path.basename(self.scan_path) + '.info')

    def end_acquisition(self):
        xml_file = os.path.join(self.scan_path, os.path.basename(self.scan_path) + '.xml')
        if not os.path.exists(xml_file):
            root = cElementTree.Element('root')
            tree = cElementTree.ElementTree(root)
            tree.write(xml_file)

    def write_metadata(self, n_radio, scan_range, ref_n, dark_n):
        info_file = self.get_info_file()
        if not os.path.exists(info_file):
            with open(self.get_info_file(), 'w') as (info_file):
                info_file.write('TOMO_N=    ' + str(n_radio) + '\n')
                info_file.write('ScanRange= ' + str(scan_range) + '\n')
                info_file.write('REF_N=     ' + str(ref_n) + '\n')
                info_file.write('REF_ON=    ' + str(n_radio) + '\n')
                info_file.write('DARK_N=    ' + str(dark_n) + '\n')
                info_file.write('Dim_1=     ' + str(self.det_width) + '\n')
                info_file.write('Dim_2=     ' + str(self.det_height) + '\n')
                info_file.write('Col_beg=    0\n')
                info_file.write('Col_end=   ' + str(self.det_width) + '\n')
                info_file.write('Row_beg=    0\n')
                info_file.write('Row_end=    ' + str(self.det_height) + '\n')
                info_file.write('PixelSize=  ' + str(_ScanMock.PIXEL_SIZE) + '\n')

    def add_radio(self, index=None):
        if index is not None:
            self._last_radio_index = index
            index_ = index
        else:
            self._last_radio_index += 1
            index_ = self._last_radio_index
        file_name = os.path.basename(self.scan_path) + '_{0:04d}'.format(index_) + '.edf'
        f = os.path.join(self.scan_path, file_name)
        if not os.path.exists(f):
            data = self._get_radio_data(index=index_)
            assert data is not None
            assert data.shape == (self.det_width, self.det_height)
            edf_writer = fabio.edfimage.EdfImage(data=data, header={'tata': 'toto'})
            edf_writer.write(f)

    @staticmethod
    def mockReconstruction(folder, nRecons=5, nPagRecons=0, volFile=False):
        """
        create reconstruction files into the given folder

        :param str folder: the path of the folder where to save the reconstruction
        :param nRecons: the number of reconstruction to mock
        :param nPagRecons: the number of paganin reconstruction to mock
        :param volFile: true if we want to add a volFile with reconstruction
        """
        if not (type(nRecons) is int and nRecons >= 0):
            raise AssertionError
        basename = os.path.basename(folder)
        dim = 200
        for i in range(nRecons):
            f = os.path.join(folder, basename + str(MockEDF._RECONS_PATTERN + str(i) + '.edf'))
            data = numpy.zeros((dim, dim))
            data[::i + 2, ::i + 2] = 1.0
            edf_writer = fabio.edfimage.EdfImage(data=data, header={'tata': 'toto'})
            edf_writer.write(f)

        for i in range(nPagRecons):
            f = os.path.join(folder, basename + str(MockEDF._PAG_RECONS_PATTERN + str(i) + '.edf'))
            data = numpy.zeros((dim, dim))
            data[::i + 2, ::i + 2] = 1.0
            edf_writer = fabio.edfimage.EdfImage(data=data, header={'tata': 'toto'})
            edf_writer.write(f)

        if volFile is True:
            volFile = os.path.join(folder, basename + '.vol')
            infoVolFile = os.path.join(folder, basename + '.vol.info')
            dataShape = (nRecons, dim, dim)
            data = numpy.random.random(nRecons * dim * dim).reshape(nRecons, dim, dim)
            data.astype(numpy.float32).tofile(volFile)
            MockEDF._createVolInfoFile(filePath=infoVolFile, shape=dataShape)

    @staticmethod
    def _createVolInfoFile(filePath, shape, voxelSize=1, valMin=0.0, valMax=1.0, s1=0.0, s2=1.0, S1=0.0, S2=1.0):
        assert len(shape) is 3
        f = open(filePath, 'w')
        f.writelines('\n'.join([
         '! PyHST_SLAVE VOLUME INFO FILE',
         'NUM_X =  %s' % shape[2],
         'NUM_Y =  %s' % shape[1],
         'NUM_Z =  %s' % shape[0],
         'voxelSize =  %s' % voxelSize,
         'BYTEORDER = LOWBYTEFIRST',
         'ValMin =  %s' % valMin,
         'ValMax =  %s' % valMax,
         's1 =  %s' % s1,
         's2 =  %s' % s2,
         'S1 =  %s' % S1,
         'S2 =  %s' % S2]))
        f.close()

    @staticmethod
    def fastMockAcquisition(folder, n_radio=20, n_extra_radio=0, scan_range=360):
        """
        Simple function creating an acquisition into the given directory
        This won't complete data, scan.info of scan.xml files but just create the
        structure that data watcher is able to detect in edf mode.
        """
        if type(n_radio) is int:
            if not n_radio > 0:
                raise AssertionError
            basename = os.path.basename(folder)
            dim = 200
            if not os.path.exists(folder):
                os.mkdir(folder)
        else:
            info_file = os.path.join(folder, basename + '.info')
            if not os.path.exists(info_file):
                with open(info_file, 'w') as (info_file):
                    info_file.write('TOMO_N=                 ' + str(n_radio) + '\n')
                    info_file.write('ScanRange=                 ' + str(scan_range) + '\n')
            for i in range(n_radio + n_extra_radio):
                file_name = basename + '_{0:04d}'.format(i) + '.edf'
                f = os.path.join(folder, file_name)
                if not os.path.exists(f):
                    data = numpy.random.random(dim * dim).reshape(dim, dim)
                    edf_writer = fabio.edfimage.EdfImage(data=data, header={'tata': 'toto'})
                    edf_writer.write(f)

            xml_file = os.path.join(folder, basename + '.xml')
            root = os.path.exists(xml_file) or cElementTree.Element('root')
            tree = cElementTree.ElementTree(root)
            tree.write(xml_file)

    @staticmethod
    def mockScan(scanID, nRadio=5, nRecons=1, nPagRecons=0, dim=10, scan_range=360, n_extra_radio=0):
        """
        Create some random radios and reconstruction in the folder

        :param str scanID: the folder where to save the radios and scans
        :param int nRadio: The number of radios to create
        :param int nRecons: the number of reconstruction to mock
        :param int nRecons: the number of paganin reconstruction to mock
        :param int dim: dimension of the files (nb row/columns)
        :param int scan_range: scan range, usually 180 or 360
        :param int n_extra_radio: number of radio run after the full range is made
                                  usually used to observe any sample movement
                                  during acquisition
        """
        assert type(scanID) is str
        assert type(nRadio) is int
        assert type(nRecons) is int
        assert type(dim) is int
        from tomwer.core.scan.scanfactory import ScanFactory
        MockEDF.fastMockAcquisition(folder=scanID, n_radio=nRadio, scan_range=scan_range,
          n_extra_radio=n_extra_radio)
        MockEDF.mockReconstruction(folder=scanID, nRecons=nRecons,
          nPagRecons=nPagRecons)
        return ScanFactory.create_scan_object(scanID)