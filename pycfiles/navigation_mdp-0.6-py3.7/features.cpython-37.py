# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/navigation_mdp/features.py
# Compiled at: 2020-04-21 17:39:05
# Size of source mod 2**32: 5545 bytes
import numpy as np
from navigation_mdp.utils import one_hot_nd

class AbstractStateFeatureSpec:

    def __init__(self, key=None):
        self.key = key

    def __call__(self, state):
        return self.compute_features(state)

    def get_key(self):
        return self.key

    def compute_features(self, state):
        raise NotImplementedError


class FeatureStateIndicator(AbstractStateFeatureSpec):

    def __init__(self, state_space):
        super().__init__(state_space)

    def compute_features(self, state):
        return state.get_idx()


class FeatureStateIndicatorOneHot(AbstractStateFeatureSpec):

    def __init__(self, key=None, dim=None):
        super().__init__(key)
        self.dim = dim

    def compute_features(self, state):
        dim = state.parent_space().n_states if self.dim is None else self.dim
        return one_hot_nd((np.asarray(state.get_idx())), N=dim)


class FeatureClassIndicator(AbstractStateFeatureSpec):

    def __init__(self, key=None):
        super().__init__(key)

    def compute_features(self, state):
        return state.get_class()


class FeatureClassIndicatorOneHot(AbstractStateFeatureSpec):

    def __init__(self, key=None, dim=None):
        super().__init__(key)
        self.dim = dim

    def compute_features(self, state):
        dim = max(state.parent_space().class_ids) + 1 if self.dim is None else self.dim
        return one_hot_nd((np.asarray(state.get_class())), N=dim)


class FeatureClassImage(AbstractStateFeatureSpec):

    def __init__(self, feature_map, key=None):
        super().__init__(key)
        self.feature_map = feature_map

    def compute_features(self, state):
        return self.feature_map[state.get_class()]


class FeatureClassImageSampler(AbstractStateFeatureSpec):

    def __init__(self, feature_sampler, key=None):
        super().__init__(key)
        self.feature_sampler = feature_sampler
        self.init_cache()

    def compute_features(self, state, resample=True):
        _class_id = state.get_class()
        if resample or _class_id not in self.cache_class_id_to_image:
            self.cache_class_id_to_image[_class_id] = self.feature_sampler(_class_id)
        return self.cache_class_id_to_image[_class_id]

    def init_cache(self):
        self.cache_class_id_to_image = {}


class ImageDiscretizer:

    def __init__(self, img, h_cells, w_cells, aug_cells=(0, 0)):
        assert len(img.shape) == 3
        self.h_cells = h_cells
        self.w_cells = w_cells
        self.aug_cell_cnt_h, self.aug_cell_cnt_w = aug_cells
        self.cell_height = int(img.shape[0] // self.h_cells)
        self.cell_width = int(img.shape[1] // self.w_cells)
        self.img_clipped = img[:self.cell_height * self.h_cells, :self.cell_width * self.w_cells]
        self.img_clipped = np.pad((self.img_clipped), (
         (
          self.aug_cell_cnt_h * self.cell_height, self.aug_cell_cnt_h * self.cell_height),
         (
          self.aug_cell_cnt_w * self.cell_width, self.aug_cell_cnt_w * self.cell_width), (0, 0)),
          mode='constant',
          constant_values=0)
        print('Note: image clipped to: {}'.format(self.img_clipped.shape))
        self.img_lst = self._create_img_grid()
        self.idxs = np.arange(h_cells * w_cells).tolist()

    def _create_img_grid(self):
        img_lst = []
        for i in range(self.h_cells):
            img_lst.append([])
            for j in range(self.w_cells):
                img_lst[(-1)].append(self.img_clipped[i * self.cell_height:(i + 2 * self.aug_cell_cnt_h + 1) * self.cell_height,
                 j * self.cell_width:(j + 2 * self.aug_cell_cnt_w + 1) * self.cell_width])

        return np.asarray(img_lst)

    def get_raw_image(self):
        return self.img_clipped

    def get_image_grid(self):
        return self.img_lst

    def get_image_cell(self, row, col):
        return self.img_lst[row][col]

    def __call__(self):
        return self.get_image_grid()


class FeatureStateIdxToArray(AbstractStateFeatureSpec):

    def __init__(self, state_idx_to_array_fn, key=None):
        super().__init__(key)
        self.state_idx_to_array_fn = state_idx_to_array_fn

    def compute_features(self, state):
        return self.state_idx_to_array_fn(state.get_idx())


class FeatureStateLocToArray(AbstractStateFeatureSpec):

    def __init__(self, state_loc_to_array_fn, key=None):
        super().__init__(key)
        self.state_loc_to_array_fn = state_loc_to_array_fn

    def compute_features(self, state):
        return (self.state_loc_to_array_fn)(*state.get_location())