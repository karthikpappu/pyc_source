# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/nxtomomill/converter.py
# Compiled at: 2020-03-12 09:26:22
# Size of source mod 2**32: 30056 bytes
"""
module to convert from (bliss) .h5 to (nexus tomo compliant) .nx
"""
__authors__ = [
 'C. Nemoz', 'H. Payno', 'A.Sole']
__license__ = 'MIT'
__date__ = '28/02/2020'
import silx.utils.enum as _Enum
from nxtomomill.utils import Progress
import os, typing, h5py, numpy, logging
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)
VALID_CAMERA_NAME = ('pcolinux', )
_ROT_ANGLE_KEYS = ('hrsrot', 'srot')
_X_TRANS_KEYS = ('sx', )
_Y_TRANS_KEYS = ('sy', )
_Z_TRANS_KEYS = ('sz', )
_ACQ_EXPO_TIME_KEYS = ('acq_expo_time', )
CURRENT_OUTPUT_VERSION = 0.1

class ImageKey(_Enum):
    ALIGNMENT = -1
    PROJECTION = 0
    FLAT_FIELD = 1
    DARK_FIELD = 2
    INVALID = 3


class AcquisitionStep(_Enum):
    INITIALIZATION = ('tomo:basic', 'tomo:zseries', 'tomo:fullturn')
    DARK = ('dark images', )
    REFERENCE = ('reference images', )
    PROJECTION = ('projections', )
    ALIGNEMENT = ('static images', )


def _ask_for_file_removal(file_path):
    res = input('Overwrite %s ? (Y/n)' % file_path)
    return res == 'Y'


def h5_to_nx(input_file_path: str, output_file: str, single_file: bool, file_extension: typing.Union[(str, None)], ask_before_overwrite=True, request_input=False, entries: typing.Union[(typing.Iterable, None)]=None):
    """

    :param str input_file_path: file to be converted from .h5 to tomo .nx
    :param str output_file: output NXtomo compliant file
    :param bool single_file: split each sequence in a dedicated file or merge
                             them all together
    :param Union[str, None] file_extension: file extension.
    :param bool request_input: if True can ask the user some missing
                               information
    :param Union[Iterable, None]: set of entries to convert. If None will
                                  convert all the entries
    """
    print('******set up***********')
    if not os.path.isfile(input_file_path):
        raise ValueError('Given input file does not exists: %s' % input_file_path)
    elif not h5py.is_hdf5(input_file_path):
        raise ValueError('Given input file is not an hdf5 file')
    else:
        if input_file_path == output_file:
            raise ValueError('input and output file are the same')
        if os.path.exists(output_file):
            if ask_before_overwrite is False:
                _logger.warning(output_file + ' will be removed')
                _logger.info('remove ' + output_file)
                os.remove(output_file)
            else:
                if not _ask_for_file_removal(output_file):
                    _logger.info('unable to overwrite %s, exit' % output_file)
                    exit(0)
                else:
                    os.remove(output_file)
    with h5py.File(input_file_path, 'r') as (h5d):
        groups = list(h5d.keys())
        groups.sort()
        progress = Progress('parse sequences')
        progress.set_max_advancement(len(h5d.keys()))
        acquisitions = []
        current_acquisition = None
        register_current_acq = False
        for group_name in groups:
            _logger.debug('parse %s' % group_name)
            entry = h5d[group_name]
            entry_type = _get_entry_type(entry=entry)
            if entry_type is AcquisitionStep.INITIALIZATION:
                current_acquisition = _Acquisition(entry)
                register_current_acq = entries is None or entry.name in entries
                if register_current_acq:
                    acquisitions.append(current_acquisition)
            elif current_acquisition is None:
                _logger.error('Group %s ignored because no preceding initialization (%s) found in the sequence.' % (
                 group_name,
                 AcquisitionStep.INITIALIZATION.value))
                continue
            else:
                if register_current_acq:
                    current_acquisition.register_step(entry)
            progress.increase_advancement()

        possible_extensions = ('.hdf5', '.h5', '.nx', '.nexus')
        output_file_basename = os.path.basename(output_file)
        file_extension_ = None
        for possible_extension in possible_extensions:
            if output_file_basename.endswith(possible_extension):
                output_file_basename.rstrip(possible_extension)
                file_extension_ = possible_extension

        progress = Progress('write sequences')
        progress.set_max_advancement(len(acquisitions))
        for i_acquisition, acquisition in enumerate(acquisitions):
            if not acquisition.is_valid():
                _logger.error('unable to write nexus file for %s' % acquisition.initialization_entry.name)
            else:
                if single_file:
                    en_output_file = output_file
                    entry = 'entry' + str(i_acquisition).zfill(4)
                else:
                    ext = file_extension_ or file_extension
                    file_name = output_file_basename + '_' + str(i_acquisition).zfill(4) + ext
                    en_output_file = os.path.join(os.path.dirname(output_file), file_name)
                    entry = 'entry'
                    if os.path.exists(en_output_file):
                        if ask_before_overwrite is False:
                            _logger.warning(en_output_file + ' will be removed')
                            _logger.info('remove ' + en_output_file)
                            os.remove(en_output_file)
                        else:
                            if _ask_for_file_removal(en_output_file) is False:
                                _logger.info('unable to overwrite %s, exit' % en_output_file)
                                exit(0)
                            else:
                                os.remove(en_output_file)
                    acquisition.write_as_nxtomo(output_file=en_output_file, data_path=entry,
                      input_file_path=input_file_path,
                      request_input=request_input)
                    if single_file is False:
                        _logger.info('create link in %s' % output_file)
                        with h5py.File(output_file, 'a') as (master_file):
                            mf_entry = 'entry' + str(i_acquisition).zfill(4)
                            link_file = os.path.relpath(en_output_file, os.path.dirname(output_file))
                            master_file[mf_entry] = h5py.ExternalLink(link_file, entry)
                    progress.increase_advancement()


def _get_entry_type(entry: h5py.Group) -> typing.Union[(None, AcquisitionStep)]:
    try:
        title = entry['title'][()]
    except Exception as e:
        try:
            _logger.error('fail to find title for %s, skip this group' % entry.name)
        finally:
            e = None
            del e

    for step in AcquisitionStep:
        if title.startswith(step.value):
            return step


def get_bliss_tomo_entries(input_file_path):
    """Util function. Used by tomwer for example"""
    with h5py.File(input_file_path, 'r') as (h5d):
        acquisitions = []
        for group_name in h5d.keys():
            _logger.debug('parse %s' % group_name)
            entry = h5d[group_name]
            entry_type = _get_entry_type(entry=entry)
            if entry_type is AcquisitionStep.INITIALIZATION:
                acquisitions.append(entry.name)

        return acquisitions


class _Acquisition:
    __doc__ = '\n    Util class to group hdf5 group together and to write the data\n    Nexus / NXtomo compliant\n    '
    _SCAN_NUMBER_PATH = 'measurement/scan_numbers'
    _ENERGY_PATH = 'technique/scan/energy'
    _DISTANCE_PATH = 'technique/scan/sample_detector_distance'
    _X_PIXEL_SIZE_PATH = 'technique/detector/pixel_size'
    _Y_PIXEL_SIZE_PATH = 'technique/detector/pixel_size'
    _X_MAGNIFIED_PIXEL_SIZE = 'technique/optic/sample_pixel_size '
    _Y_MAGNIFIED_PIXEL_SIZE = 'technique/optic/sample_pixel_size '
    _NAME_PATH = 'technique/scan/name'

    def __init__(self, entry: h5py.Group):
        assert _get_entry_type(entry=entry) is AcquisitionStep.INITIALIZATION, 'constructor should be initializaed with an `Initialization entry`'
        self._initialization_entry = entry
        self._indexes = entry[_Acquisition._SCAN_NUMBER_PATH]
        self._indexes_str = tuple([str(index) for index in entry[_Acquisition._SCAN_NUMBER_PATH]])
        self._registered_entries = []
        self._data = None
        self._image_key = None
        self._image_key_control = None
        self._rotation_angle = None
        self._x_translation = None
        self._y_translation = None
        self._z_translation = None
        self._n_frames = None
        self._dim_1 = None
        self._dim_2 = None
        self._data_type = None
        self._virtual_sources = None
        self._acq_expo_time = None

    @property
    def initialization_entry(self):
        return self._initialization_entry

    @property
    def image_key(self):
        return self._image_key

    @property
    def image_key_control(self):
        return self._image_key_control

    @property
    def rotation_angle(self):
        return self._rotation_angle

    @property
    def x_translation(self):
        return self._x_translation

    @property
    def y_translation(self):
        return self._y_translation

    @property
    def z_translation(self):
        return self._z_translation

    @property
    def n_frames(self):
        return self._n_frames

    @property
    def dim_1(self):
        return self._dim_1

    @property
    def dim_2(self):
        return self._dim_2

    @property
    def data_type(self):
        return self._data_type

    @property
    def expo_time(self):
        return self._acq_expo_time

    def register_step(self, entry: h5py.Group) -> None:
        """

        :param entry:
        """
        if not _get_entry_type(entry=entry) is not AcquisitionStep.INITIALIZATION:
            raise AssertionError
        else:
            if entry.name.startswith(self._indexes_str):
                raise ValueError('The %s entry is not part of this sequence' % entry.name)
            if _get_entry_type(entry=entry) is None:
                _logger.warning('%s not recognized, skip it' % entry.name)
            else:
                self._registered_entries.append(entry)

    def is_valid(self) -> bool:
        """Make sure all scan number are present"""
        registered_entries_str = tuple([entry.name for entry in self._registered_entries])

        def has_been_registered(index):
            for entry_str in registered_entries_str:
                if index in entry_str:
                    return True

            return False

        missing = []
        for index_str in self._indexes_str:
            if not has_been_registered(index_str):
                missing.append(index_str)

        if len(missing) > 0:
            _logger.error('%s indexes are missing' % missing)
            return False
        return True

    def write_as_nxtomo(self, output_file: str, data_path: str, input_file_path: str, request_input: bool) -> None:
        """write the current sequence in an NXtomo like"""
        _logger.info('write data of %s to %s' % (self.initialization_entry.name,
         output_file + '::/' + data_path))
        self._preprocess_frames(input_file_path)
        with h5py.File(output_file, 'a') as (h5_file):
            entry = h5_file.require_group(data_path)
            entry.attrs['NX_class'] = 'NXentry'
            entry.attrs['definition'] = 'NXtomo'
            entry.attrs['version'] = CURRENT_OUTPUT_VERSION
            self._write_beam(entry, request_input=request_input)
            self._write_instrument(entry)
            self._write_sample(entry)

    def _preprocess_frames(self, input_file_path):
        """parse all frames of the different steps and retrieve data,
        image_key..."""
        n_frames = 0
        dim_1 = None
        dim_2 = None
        data_type = None
        _x_translation = []
        _y_translation = []
        _z_translation = []
        _image_key = []
        _image_key_control = []
        _rotation_angle = []
        _virtual_sources = []
        _virtual_sources_len = []
        _acq_expo_time = []
        for entry in self._registered_entries:
            type_ = _get_entry_type(entry)
            if type_ is AcquisitionStep.INITIALIZATION:
                raise RuntimeError('no initialization should be registered.There should be only one per acquisition.')
            elif type_ is AcquisitionStep.PROJECTION:
                image_key_control = ImageKey.PROJECTION
                image_key = ImageKey.PROJECTION
            else:
                if type_ is AcquisitionStep.ALIGNEMENT:
                    image_key_control = ImageKey.ALIGNMENT
                    image_key = ImageKey.PROJECTION
                else:
                    if type_ is AcquisitionStep.DARK:
                        image_key_control = ImageKey.DARK_FIELD
                        image_key = ImageKey.DARK_FIELD
                    else:
                        if type_ is AcquisitionStep.REFERENCE:
                            image_key_control = ImageKey.FLAT_FIELD
                            image_key = ImageKey.FLAT_FIELD
                        else:
                            raise ValueError('entry not recognized: ' + entry.name)
            if 'instrument' not in entry:
                _logger.error('no measurement group found in %s, unable toretrieve frames' % entry.name)
                continue
            instrument_grp = entry['instrument']
            for key in instrument_grp:
                if 'NX_class' in instrument_grp[key].attrs and instrument_grp[key].attrs['NX_class'] == 'NXdetector':
                    _logger.debug('Found one detector at %s for %s.' % (
                     key, entry.name))
                    if key not in VALID_CAMERA_NAME:
                        _logger.info('ignore %s, not a `valid` camera name' % key)
                        continue
                    detector_node = instrument_grp[key]
                    if 'data_cast' in detector_node:
                        _logger.warning('!!! looks like this data has been cast. Take cast data for %s!!!' % detector_node)
                        data_dataset = detector_node['data_cast']
                    else:
                        data_dataset = detector_node['data']
                    assert data_dataset.ndim == 3, 'data dataset of detector should be 3D'
                    shape = data_dataset.shape
                    n_frame = shape[0]
                    n_frames += n_frame
                    if dim_1 is None:
                        dim_2 = shape[1]
                        dim_1 = shape[2]
                    else:
                        if dim_1 != shape[2] or dim_2 != shape[1]:
                            raise ValueError('Inconsistency in detector shapes')
                    if data_type is None:
                        data_type = data_dataset.dtype
                    else:
                        if data_type != data_dataset.dtype:
                            raise ValueError('detector frames have incoherent data types')
                        _image_key_control.extend([image_key_control.value] * n_frame)
                        _image_key.extend([image_key.value] * n_frame)
                        v_source = h5py.VirtualSource(input_file_path, (data_dataset.name),
                          shape=shape)
                        _virtual_sources.append(v_source)
                        _virtual_sources_len.append(n_frame)
                        rots = self._get_rotation_angle(instrument_grp=instrument_grp, n_frame=n_frame)
                        _rotation_angle.extend(rots)
                        _x_translation.extend(self._get_x_translation(instrument_grp=instrument_grp, n_frame=n_frame))
                        _y_translation.extend(self._get_y_translation(instrument_grp=instrument_grp, n_frame=n_frame))
                        _z_translation.extend(self._get_z_translation(instrument_grp=instrument_grp, n_frame=n_frame))
                        _acq_expo_time.extend(self._get_expo_time(detector_grp=detector_node, n_frame=n_frame))

        self._x_translation = _x_translation
        self._y_translation = _y_translation
        self._z_translation = _z_translation
        self._image_key = tuple(_image_key)
        self._image_key_control = tuple(_image_key_control)
        self._rotation_angle = _rotation_angle
        self._n_frames = n_frames
        self._data_type = data_type
        self._virtual_sources = _virtual_sources
        self._dim_1 = dim_1
        self._dim_2 = dim_2
        self._virtual_sources_len = _virtual_sources_len
        self._acq_expo_time = _acq_expo_time

    def _get_rotation_angle(self, instrument_grp, n_frame) -> list:
        """return the list of rotation angle for each frame"""
        return self._get_node_values_for_frame_array(node=(instrument_grp['positioners']), n_frame=n_frame,
          keys=_ROT_ANGLE_KEYS)

    def _get_x_translation(self, instrument_grp, n_frame) -> list:
        """return the list of translation for each frame"""
        return self._get_node_values_for_frame_array(node=(instrument_grp['positioners']), n_frame=n_frame,
          keys=_X_TRANS_KEYS)

    def _get_y_translation(self, instrument_grp, n_frame) -> list:
        """return the list of translation for each frame"""
        return self._get_node_values_for_frame_array(node=(instrument_grp['positioners']), n_frame=n_frame,
          keys=_Y_TRANS_KEYS)

    def _get_z_translation(self, instrument_grp, n_frame) -> list:
        """return the list of translation for each frame"""
        return self._get_node_values_for_frame_array(node=(instrument_grp['positioners']), n_frame=n_frame,
          keys=_Z_TRANS_KEYS)

    def _get_expo_time(self, detector_grp, n_frame) -> list:
        """return expo time for each frame"""
        return self._get_node_values_for_frame_array(node=(detector_grp['acq_parameters']), n_frame=n_frame,
          keys=_ACQ_EXPO_TIME_KEYS)

    @staticmethod
    def _get_node_values_for_frame_array(node: h5py.Group, n_frame: int, keys: typing.Iterable):

        def get_values():
            for possible_key in keys:
                if possible_key in node:
                    return node[possible_key][()]

        values = get_values()
        if values is None:
            raise ValueError('Unable to retrieve rotation angle for %s' % node.name)
        else:
            if numpy.isscalar(values):
                return [
                 values] * n_frame
            if len(values) == n_frame:
                return values.tolist()
            if len(values) == n_frame + 1:
                return values[:-1].tolist()
            raise ValueError('incoherent number of angle position compare to the number of frame')

    def _write_beam(self, root_node, request_input):
        beam_node = root_node.create_group('beam')
        energy, unit = self._get_energy(ask_if_0=request_input)
        if energy is not None:
            beam_node['incident_energy'] = energy
            beam_node['incident_energy'].attrs['unit'] = unit

    def _write_instrument(self, root_node):
        instrument_node = root_node.create_group('instrument')
        instrument_node.attrs['NX_class'] = 'NXinstrument'
        detector_node = instrument_node.create_group('detector')
        detector_node.attrs['NX_class'] = 'NXdetector'
        if self._virtual_sources is not None:
            self._create_data_virtual_dataset(detector_node)
        if self.image_key is not None:
            detector_node['image_key'] = self.image_key
        if self.image_key_control is not None:
            detector_node['image_key_control'] = self.image_key_control
        if self._acq_expo_time is not None:
            detector_node['count_time'] = self._acq_expo_time
        distance, unit = self._get_distance()
        if distance is not None:
            detector_node['distance'] = distance
            detector_node['distance'].attrs['unit'] = unit
        x_pixel_size, unit = self._get_pixel_size('x')
        if x_pixel_size is not None:
            detector_node['x_pixel_size'] = x_pixel_size
            detector_node['x_pixel_size'].attrs['unit'] = unit
        y_pixel_size, unit = self._get_pixel_size('y')
        if y_pixel_size is not None:
            detector_node['y_pixel_size'] = y_pixel_size
            detector_node['y_pixel_size'].attrs['unit'] = unit
        x_magnified_pix_size, unit = self._get_magnified_pixel_size('x')
        if x_magnified_pix_size is not None:
            detector_node['x_magnified_pixel_size'] = x_magnified_pix_size
            detector_node['x_magnified_pixel_size'].attrs['unit'] = unit
        y_magnified_pix_size, unit = self._get_magnified_pixel_size('y')
        if y_magnified_pix_size is not None:
            detector_node['y_magnified_pixel_size'] = y_magnified_pix_size
            detector_node['y_magnified_pixel_size'].attrs['unit'] = unit

    def _create_data_virtual_dataset--- This code section failed: ---

 L. 610         0  LOAD_FAST                'self'
                2  LOAD_ATTR                n_frames
                4  LOAD_CONST               None
                6  COMPARE_OP               is
                8  POP_JUMP_IF_TRUE     40  'to 40'
               10  LOAD_FAST                'self'
               12  LOAD_ATTR                dim_1
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_TRUE     40  'to 40'
               20  LOAD_FAST                'self'
               22  LOAD_ATTR                dim_2
               24  LOAD_CONST               None
               26  COMPARE_OP               is
               28  POP_JUMP_IF_TRUE     40  'to 40'

 L. 611        30  LOAD_FAST                'self'
               32  LOAD_ATTR                data_type
               34  LOAD_CONST               None
               36  COMPARE_OP               is
               38  POP_JUMP_IF_FALSE    48  'to 48'
             40_0  COME_FROM            28  '28'
             40_1  COME_FROM            18  '18'
             40_2  COME_FROM             8  '8'

 L. 612        40  LOAD_GLOBAL              ValueError
               42  LOAD_STR                 'Preprocessing could not deduce all information for creating the `data` virtual dataset'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  RAISE_VARARGS_1       1  'exception instance'
             48_0  COME_FROM            38  '38'

 L. 614        48  LOAD_GLOBAL              h5py
               50  LOAD_ATTR                VirtualLayout
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                n_frames
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                dim_2
               60  LOAD_FAST                'self'
               62  LOAD_ATTR                dim_1
               64  BUILD_TUPLE_3         3 

 L. 615        66  LOAD_FAST                'self'
               68  LOAD_ATTR                data_type
               70  LOAD_CONST               ('shape', 'dtype')
               72  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               74  STORE_FAST               'layout'

 L. 616        76  LOAD_CONST               0
               78  STORE_FAST               'last'

 L. 617        80  SETUP_LOOP          132  'to 132'
               82  LOAD_GLOBAL              zip
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                _virtual_sources
               88  LOAD_FAST                'self'
               90  LOAD_ATTR                _virtual_sources_len
               92  CALL_FUNCTION_2       2  '2 positional arguments'
               94  GET_ITER         
               96  FOR_ITER            130  'to 130'
               98  UNPACK_SEQUENCE_2     2 
              100  STORE_FAST               'v_source'
              102  STORE_FAST               'vs_len'

 L. 618       104  LOAD_FAST                'v_source'
              106  LOAD_FAST                'layout'
              108  LOAD_FAST                'last'
              110  LOAD_FAST                'vs_len'
              112  LOAD_FAST                'last'
              114  BINARY_ADD       
              116  BUILD_SLICE_2         2 
              118  STORE_SUBSCR     

 L. 619       120  LOAD_FAST                'last'
              122  LOAD_FAST                'vs_len'
              124  INPLACE_ADD      
              126  STORE_FAST               'last'
              128  JUMP_BACK            96  'to 96'
              130  POP_BLOCK        
            132_0  COME_FROM_LOOP       80  '80'

 L. 621       132  LOAD_FAST                'detector_node'
              134  LOAD_METHOD              create_virtual_dataset
              136  LOAD_STR                 'data'
              138  LOAD_FAST                'layout'
              140  CALL_METHOD_2         2  '2 positional arguments'
              142  POP_TOP          

 L. 622       144  LOAD_STR                 'image'
              146  LOAD_FAST                'detector_node'
              148  LOAD_STR                 'data'
              150  BINARY_SUBSCR    
              152  LOAD_ATTR                attrs
              154  LOAD_STR                 'interpretation'
              156  STORE_SUBSCR     

Parse error at or near `COME_FROM' instruction at offset 48_0

    def _check_has_metadata(self):
        if self._initialization_entry is None:
            raise ValueError('no initialization entry specify, unable toretrieve energy')

    def _write_sample(self, root_node):
        sample_node = root_node.create_group('sample')
        sample_node.attrs['NX_class'] = 'NXsample'
        name = self._get_name()
        if name:
            sample_node['name'] = name
        if self.rotation_angle is not None:
            sample_node['rotation_angle'] = self.rotation_angle
        if self.x_translation is not None:
            sample_node['x_translation'] = self.x_translation
        if self.y_translation is not None:
            sample_node['y_translation'] = self.y_translation
        if self.z_translation is not None:
            sample_node['z_translation'] = self.z_translation

    def _get_name(self):
        """return name of the acquisition"""
        self._check_has_metadata()
        if self._NAME_PATH in self._initialization_entry:
            return self._initialization_entry[self._NAME_PATH][()]
        _logger.warning('No name describing the acquisition has been found, Name dataset will be skip')
        return

    def _get_energy(self, ask_if_0):
        """return tuple(energy, unit)"""
        self._check_has_metadata()
        if self._ENERGY_PATH in self._initialization_entry:
            energy = self._initialization_entry[self._ENERGY_PATH][()]
            unit = self._get_unit((self._initialization_entry[self._ENERGY_PATH]), default_unit='kev')
            if ask_if_0:
                en = input('Energy has not been registered. Please enter incoming beam energy (in kev):')
                energy = float(en)
            return (
             energy, unit)
        _logger.warning('unable to find energy. Energy dataset will be skip')
        return (None, None)

    def _get_distance(self):
        """return tuple(distance, unit)"""
        self._check_has_metadata()
        if self._DISTANCE_PATH in self._initialization_entry:
            node = self.initialization_entry[self._DISTANCE_PATH]
            distance = node[()]
            unit = self._get_unit(node, default_unit='cm')
            return (distance, unit)
        _logger.warning('unable to find distance. Will be skip')
        return (None, None)

    def _get_pixel_size(self, axis):
        """return tuple(pixel_size, unit)"""
        assert axis in ('x', 'y')
        self._check_has_metadata()
        path = self._X_PIXEL_SIZE_PATH if axis == 'x' else self._Y_PIXEL_SIZE_PATH
        if path in self._initialization_entry:
            node = self.initialization_entry[path]
            size_ = node[()][0]
            unit = self._get_unit(node, default_unit='micrometer')
            return (size_, unit)
        _logger.warning('unable to find %s pixel size. Will be skip' % axis)
        return (None, None)

    def _get_magnified_pixel_size(self, axis):
        """return tuple(pixel_size, unit)"""
        assert axis in ('x', 'y')
        self._check_has_metadata()
        path = self._X_MAGNIFIED_PIXEL_SIZE if axis == 'x' else self._Y_MAGNIFIED_PIXEL_SIZE
        if path in self._initialization_entry:
            node = self.initialization_entry[path]
            size_ = node[()]
            unit = self._get_unit(node, default_unit='micrometer')
            return (size_, unit)
        _logger.warning('unable to find %s magnified pixel size. Will be skip' % axis)
        return (None, None)

    def _get_unit(self, node: h5py.Dataset, default_unit):
        """Simple process to retrieve unit from an attribute"""
        if 'unit' in node.attrs:
            return node.attrs['unit']
        if 'units' in node.attrs:
            return node.attrs['units']
        _logger.warning('no unit found for %s, take default unit: %s' % (
         node.name, default_unit))
        return default_unit