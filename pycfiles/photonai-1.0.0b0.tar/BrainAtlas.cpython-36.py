# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/neuro/BrainAtlas.py
# Compiled at: 2019-08-30 10:14:32
# Size of source mod 2**32: 21850 bytes
import inspect, glob, time, numpy as np, nibabel as nib
from os import path
from pathlib import Path
from sklearn.base import BaseEstimator
from nilearn import image, masking, _utils
from nilearn.input_data import NiftiMasker
from nilearn._utils.niimg import _safe_get_data
from ..photonlogger.Logger import Logger, Singleton

class RoiObject:

    def __init__(self, index=0, label='', size=None, mask=None):
        self.index = index
        self.label = label
        self.size = size
        self.mask = mask
        self.is_empty = False


class MaskObject:

    def __init__(self, name: str='', mask_file: str='', mask=None):
        self.name = name
        self.mask_file = mask_file
        self.mask = mask
        self.is_empty = False


class AtlasObject:

    def __init__(self, name='', path='', labels_file='', mask_threshold=None, affine=None, shape=None, indices=list()):
        self.name = name
        self.path = path
        self.labels_file = labels_file
        self.mask_threshold = mask_threshold
        self.indices = indices
        self.roi_list = list()
        self.map = None
        self.atlas = None
        self.affine = affine
        self.shape = shape


@Singleton
class AtlasLibrary:
    ATLAS_DICTIONARY = {'AAL':'AAL.nii.gz', 
     'HarvardOxford_Cortical_Threshold_25':'HarvardOxford-cort-maxprob-thr25.nii.gz', 
     'HarvardOxford_Subcortical_Threshold_25':'HarvardOxford-sub-maxprob-thr25.nii.gz', 
     'HarvardOxford_Cortical_Threshold_50':'HarvardOxford-cort-maxprob-thr50.nii.gz', 
     'HarvardOxford_Subcortical_Threshold_50':'HarvardOxford-sub-maxprob-thr50.nii.gz', 
     'Yeo_7':'Yeo2011_7Networks_MNI152_FreeSurferConformed1mm.nii.gz', 
     'Yeo_7_Liberal':'Yeo2011_7Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii.gz', 
     'Yeo_17':'Yeo2011_17Networks_MNI152_FreeSurferConformed1mm.nii.gz', 
     'Yeo_17_Liberal':'Yeo2011_17Networks_MNI152_FreeSurferConformed1mm_LiberalMask.nii.gz'}
    MASK_DICTIONARY = {'MNI_ICBM152_GrayMatter':'mni_icbm152_gm_tal_nlin_sym_09a.nii.gz', 
     'MNI_ICBM152_WhiteMatter':'mni_icbm152_wm_tal_nlin_sym_09a.nii.gz', 
     'MNI_ICBM152_WholeBrain':'mni_icbm152_t1_tal_nlin_sym_09a_mask.nii.gz', 
     'Cerebellum':'P_08_Cere.nii.gz'}

    def __init__(self):
        self.photon_atlases = self._load_photon_atlases()
        self.photon_masks = self._load_photon_masks()
        self.library = dict()

    def _load_photon_atlases(self):
        dir_atlases = path.dirname(inspect.getfile(BrainAtlas)) + '/' + 'Atlases/'
        photon_atlases = dict()
        for atlas_id, atlas_info in self.ATLAS_DICTIONARY.items():
            atlas_file = glob.glob(path.join(dir_atlases, path.join('*', atlas_info)))[0]
            atlas_basename = path.basename(atlas_file)[:-7]
            atlas_dir = path.dirname(atlas_file)
            photon_atlases[atlas_id] = AtlasObject(name=atlas_id, path=atlas_file, labels_file=(path.join(atlas_dir, atlas_basename + '_labels.txt')))

        return photon_atlases

    def _load_photon_masks(self):
        dir_atlases = path.dirname(inspect.getfile(BrainAtlas)) + '/' + 'Atlases/'
        photon_masks = dict()
        for mask_id, mask_info in self.MASK_DICTIONARY.items():
            mask_file = glob.glob(path.join(dir_atlases, path.join('*', mask_info)))[0]
            photon_masks[mask_id] = MaskObject(name=mask_id, mask_file=mask_file)

        return photon_masks

    def list_rois(self, atlas: str):
        if atlas not in self.ATLAS_DICTIONARY.keys():
            Logger().info('Atlas {} is not supported.'.format(atlas))
            return
        else:
            atlas = self.get_atlas(atlas)
            roi_names = [roi.label for roi in atlas.roi_list]
            Logger().info(str(roi_names))
            return roi_names

    def _add_atlas_to_library(self, atlas_name, target_affine=None, target_shape=None, mask_threshold=None):
        print('Adding atlas to library: {} - Shape {} - Affine {} - Threshold {}'.format(atlas_name, target_shape, target_affine, mask_threshold))
        if atlas_name in self.photon_atlases.keys():
            original_atlas_object = self.photon_atlases[atlas_name]
        else:
            print('Checking custom atlas')
            original_atlas_object = self._check_custom_atlas(atlas_name)
        atlas_object = AtlasObject(name=(original_atlas_object.name), path=(original_atlas_object.path),
          labels_file=(original_atlas_object.labels_file),
          mask_threshold=mask_threshold,
          affine=target_affine,
          shape=target_shape)
        img = image.load_img(atlas_object.path)
        resampled_img = self._resample(img, target_affine=target_affine, target_shape=target_shape)
        atlas_object.atlas = resampled_img
        atlas_object.map = np.asarray(atlas_object.atlas.get_data())
        if mask_threshold is not None:
            atlas_object.map[atlas_object.map < mask_threshold] = 0
            atlas_object.map = atlas_object.map.astype(int)
        else:
            atlas_object.indices = list(np.unique(atlas_object.map))
            if Path(atlas_object.labels_file).is_file():
                labels_dict = dict()
                with open(atlas_object.labels_file) as (f):
                    for line in f:
                        key, val = line.split('\t')
                        labels_dict[int(key)] = val

                if not sorted(atlas_object.indices) == sorted(list(labels_dict.keys())):
                    print('\n                The indices in map image ARE NOT the same as those in your *_labels.txt! Ignoring *_labels.txt.\n                MapImage: \n                {}\n                File:\n                {}\n                '.format(str(sorted(self.indices)), str(sorted(list(labels_dict.keys())))))
                    atlas_object.roi_list = [RoiObject(index=i, label=(str(i)), size=(np.sum(i == atlas_object.map))) for i in atlas_object.indices]
                else:
                    for i in range(len(atlas_object.indices)):
                        roi_index = atlas_object.indices[i]
                        new_roi = RoiObject(index=roi_index, label=(labels_dict[roi_index].replace('\n', '')), size=(np.sum(roi_index == atlas_object.map)))
                        atlas_object.roi_list.append(new_roi)

            else:
                atlas_object.roi_list = [RoiObject(index=i, label=(str(i)), size=(np.sum(i == atlas_object.map))) for i in atlas_object.indices]
        for roi in atlas_object.roi_list:
            if roi.size == 0:
                pass
            else:
                roi.mask = image.new_img_like(atlas_object.path, atlas_object.map == roi.index)
                if np.sum(roi.mask.dataobj != 0) == 0:
                    roi.is_empty = True

        self.library[(atlas_name, str(target_affine), str(target_shape), str(mask_threshold))] = atlas_object
        print('Done adding atlas to library!')

    def _add_mask_to_library(self, mask_name: str='', target_affine=None, target_shape=None, mask_threshold=None):
        print('Adding mask to library: {} - Shape {} - Affine {} - Threshold {}'.format(mask_name, target_shape, target_affine, mask_threshold))
        if mask_name in self.photon_masks.keys():
            original_mask_object = self.photon_masks[mask_name]
        else:
            print('Checking custom mask')
            original_mask_object = self._check_custom_mask(mask_name)
        mask_object = MaskObject(name=mask_name, mask_file=(original_mask_object.mask_file))
        mask_object.mask = masking.compute_background_mask(mask_object.mask_file)
        if target_affine is not None:
            if target_shape is not None:
                mask_object.mask = self._resample((mask_object.mask), target_affine=target_affine, target_shape=target_shape)
        if np.sum(mask_object.mask.dataobj != 0) == 0:
            print('No voxels in mask after resampling (' + mask_object.name + ').')
            mask_object.is_empty = True
        self.library[(mask_object.name, str(target_affine), str(target_shape), str(mask_threshold))] = mask_object
        print('Done adding mask to library!')

    def get_atlas(self, atlas_name, target_affine=None, target_shape=None, mask_threshold=None):
        if (
         atlas_name, str(target_affine), str(target_shape), str(mask_threshold)) not in self.library:
            self._add_atlas_to_library(atlas_name, target_affine, target_shape, mask_threshold)
        return self.library[(atlas_name, str(target_affine), str(target_shape), str(mask_threshold))]

    def get_mask(self, mask_name, target_affine=None, target_shape=None, mask_threshold=None):
        if (
         mask_name, str(target_affine), str(target_shape)) not in self.library:
            self._add_mask_to_library(mask_name, target_affine, target_shape, mask_threshold)
        return self.library[(mask_name, str(target_affine), str(target_shape), str(mask_threshold))]

    @staticmethod
    def _resample(mask, target_affine, target_shape):
        if target_affine is not None:
            if target_shape is not None:
                mask = image.resample_img(mask, target_affine=target_affine, target_shape=target_shape, interpolation='nearest')
                orient_data = ''.join(nib.aff2axcodes(target_affine))
                orient_roi = ''.join(nib.aff2axcodes(mask.affine))
                if not orient_roi == orient_data:
                    print('Orientation of mask and data are not the same: ' + orient_roi + ' (mask) vs. ' + orient_data + ' (data)')
        return mask

    @staticmethod
    def _check_custom_mask(mask_file):
        if not path.isfile(mask_file):
            raise FileNotFoundError('Cannot find custom mask {}'.format(mask_file))
        return MaskObject(name=mask_file, mask_file=mask_file)

    @staticmethod
    def _check_custom_atlas(atlas_file):
        if not path.isfile(atlas_file):
            raise FileNotFoundError('Cannot find custom atlas {}'.format(atlas_file))
        labels_file = path.split(atlas_file)[0] + '_labels.txt'
        if not path.isfile(labels_file):
            print("Didn't find .txt file with ROI labels. Using indices as labels.")
        return AtlasObject(name=atlas_file, path=atlas_file, labels_file=labels_file)

    @staticmethod
    def find_rois_by_label(atlas_obj, query_list):
        return [i for i in atlas_obj.roi_list if i.label in query_list]

    @staticmethod
    def find_rois_by_index(atlas_obj, query_list):
        return [i for i in atlas_obj.roi_list if i.index in query_list]

    @staticmethod
    def get_nii_files_from_folder(folder_path, extension='.nii.gz'):
        return glob.glob(folder_path + '*' + extension)


class BrainAtlas(BaseEstimator):

    def __init__(self, atlas_name: str, extract_mode: str='vec', mask_threshold=None, background_id=0, rois='all'):
        self.atlas_name = atlas_name
        self.extract_mode = extract_mode
        self.collection_mode = 'concat'
        self.mask_threshold = mask_threshold
        self.background_id = background_id
        self.rois = rois
        self.box_shape = []
        self.is_transformer = True
        self.mask_indices = None
        self.affine = None
        self.shape = None
        self.needs_y = False
        self.needs_covariates = False

    def fit(self, X, y):
        return self

    def transform(self, X, y=None, **kwargs):
        if len(X) < 1:
            raise Exception('Brain Atlas: Did not get any data in parameter X')
        else:
            if self.collection_mode == 'list' or self.collection_mode == 'concat':
                collection_mode = self.collection_mode
            else:
                collection_mode = 'concat'
                Logger().error("Collection mode {} not supported. Use 'list' or 'concat' instead.Falling back to concat mode.".format(self.collection_mode))
            self.affine, self.shape = BrainMasker.get_format_info_from_first_image(X)
            if isinstance(X, list):
                n_subjects = len(X)
                X = image.load_img(X)
            else:
                if isinstance(X, str):
                    n_subjects = 1
                    X = image.load_img(X)
                else:
                    if isinstance(X, np.ndarray):
                        n_subjects = X.shape[0]
                        X = image.load_img(X)
                    else:
                        n_subjects = X.shape[(-1)]
            atlas_obj = AtlasLibrary().get_atlas(self.atlas_name, self.affine, self.shape, self.mask_threshold)
            roi_objects = self._get_rois(atlas_obj, which_rois=(self.rois), background_id=(self.background_id))
            roi_data = [list() for i in range(n_subjects)]
            roi_data_concat = list()
            t1 = time.time()
            series = _utils.as_ndarray((_safe_get_data(X)), dtype='float32', order='C', copy=True)
            mask_indices = list()
            for i, roi in enumerate(roi_objects):
                Logger().debug('Extracting ROI {}'.format(roi.label))
                extraction = self.apply_mask(series, roi.mask)
                if collection_mode == 'list':
                    for sub_i in range(extraction.shape[0]):
                        roi_data[sub_i].append(extraction[sub_i])

                    mask_indices.append(i)
                else:
                    roi_data_concat.append(extraction)
                    mask_indices.append(np.ones(extraction[0].size) * i)

            if self.collection_mode == 'concat':
                roi_data = np.concatenate(roi_data_concat, axis=1)
                self.mask_indices = np.concatenate(mask_indices)
            else:
                self.mask_indices = mask_indices
        elapsed_time = time.time() - t1
        Logger().debug('Time for extracting {} ROIs in {} subjects: {} seconds'.format(len(roi_objects), n_subjects, elapsed_time))
        return roi_data

    def apply_mask(self, series, mask_img):
        mask_img = _utils.check_niimg_3d(mask_img)
        mask, mask_affine = masking._load_mask_img(mask_img)
        mask_img = image.new_img_like(mask_img, mask, mask_affine)
        mask_data = _utils.as_ndarray((mask_img.get_data()), dtype=(np.bool))
        return series[mask_data].T

    def inverse_transform(self, X, y=None, **kwargs):
        X = np.asarray(X)
        atlas_obj = AtlasLibrary().get_atlas(self.atlas_name, self.affine, self.shape, self.mask_threshold)
        roi_objects = self._get_rois(atlas_obj, which_rois=(self.rois), background_id=(self.background_id))
        unmasked = np.squeeze(np.zeros_like((atlas_obj.map), dtype='float32'))
        for i, roi in enumerate(roi_objects):
            mask, mask_affine = masking._load_mask_img(roi.mask)
            mask_img = image.new_img_like(roi.mask, mask, mask_affine)
            mask_data = _utils.as_ndarray((mask_img.get_data()), dtype=(np.bool))
            if self.collection_mode == 'list':
                unmasked[mask_data] = X[i]
            else:
                unmasked[mask_data] = X[(self.mask_indices == i)]

        new_image = image.new_img_like(atlas_obj.atlas, unmasked)
        return new_image

    @staticmethod
    def _get_rois(atlas_obj, which_rois='all', background_id=0):
        if isinstance(which_rois, str):
            if which_rois == 'all':
                return [roi for roi in atlas_obj.roi_list if roi.index != background_id]
            else:
                return AtlasLibrary().find_rois_by_label(atlas_obj, [which_rois])
        else:
            if isinstance(which_rois, int):
                return AtlasLibrary().find_rois_by_index(atlas_obj, [which_rois])
        if isinstance(which_rois, list):
            if isinstance(which_rois[0], str):
                if which_rois[0].lower() == 'all':
                    return [roi for roi in atlas_obj.roi_list if roi.index != background_id]
                else:
                    return AtlasLibrary().find_rois_by_label(atlas_obj, which_rois)
            else:
                return AtlasLibrary().find_rois_by_index(atlas_obj, which_rois)


class BrainMasker(BaseEstimator):

    def __init__(self, mask_image=None, affine=None, shape=None, mask_threshold=None, extract_mode='vec'):
        self.mask_image = mask_image
        self.affine = affine
        self.shape = shape
        self.masker = None
        self.extract_mode = extract_mode
        self.mask_threshold = mask_threshold

    @staticmethod
    def get_format_info_from_first_image(X):
        if isinstance(X, str):
            img = image.load_img(X)
        else:
            if isinstance(X, list) or isinstance(X, np.ndarray):
                if isinstance(X[0], str):
                    img = image.load_img(X[0])
                elif isinstance(X[0], nib.Nifti1Image):
                    img = X[0]
            else:
                if isinstance(X, nib.Nifti1Image):
                    img = X
                else:
                    error_msg = 'Can only process strings as file paths to nifti images or nifti image object'
                    Logger().error(error_msg)
                    raise ValueError(error_msg)
            if len(img.shape) > 3:
                img_shape = img.shape[:3]
            else:
                img_shape = img.shape
        return (
         img.affine, img_shape)

    @staticmethod
    def _get_box(in_imgs, roi):
        map = roi.get_data()
        true_points = np.argwhere(map)
        corner1 = true_points.min(axis=0)
        corner2 = true_points.max(axis=0)
        box = []
        for img in in_imgs:
            if isinstance(img, str):
                data = image.load_img(img).get_data()
            else:
                data = img.get_data()
            tmp = data[corner1[0]:corner2[0] + 1, corner1[1]:corner2[1] + 1, corner1[2]:corner2[2] + 1]
            box.append(tmp)

        return np.asarray(box)

    def fit(self, X, y):
        return self

    def transform(self, X, y=None, **kwargs):
        if self.affine is None or self.shape is None:
            self.affine, self.shape = BrainMasker.get_format_info_from_first_image(X)
        else:
            if isinstance(self.mask_image, str):
                self.mask_image = AtlasLibrary().get_mask(self.mask_image, self.affine, self.shape, self.mask_threshold)
            else:
                if isinstance(self.mask_image, RoiObject):
                    pass
            if not self.mask_image.is_empty:
                self.masker = NiftiMasker(mask_img=(self.mask_image.mask), target_affine=(self.affine), target_shape=(self.shape),
                  dtype='float32')
                try:
                    single_roi = self.masker.fit_transform(X)
                except BaseException as e:
                    Logger().error(str(e))
                    single_roi = None

                if single_roi is not None:
                    if self.extract_mode == 'vec':
                        return np.asarray(single_roi)
                    else:
                        if self.extract_mode == 'mean':
                            return np.mean(single_roi, axis=1)
                        if self.extract_mode == 'box':
                            return BrainMasker._get_box(X, self.mask_image)
                        if self.extract_mode == 'img':
                            return self.masker.inverse_transform(single_roi)
                    print("Currently there are no other methods than 'vec', 'mean', and 'box' supported!")
                else:
                    print('Extracting ROI failed.')
            else:
                print('Skipping self.mask_image ' + self.mask_image.label + ' because it is empty.')

    def inverse_transform(self, X, y=None, **kwargs):
        if not self.extract_mode == 'vec':
            raise NotImplementedError('BrainMask extract_mode={} is not supported with inverse_transform'.format(self.extract_mode))
        return self.masker.inverse_transform(X)