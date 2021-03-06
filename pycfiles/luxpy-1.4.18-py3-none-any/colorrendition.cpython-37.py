# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cri\colorrendition.py
# Compiled at: 2018-05-03 02:47:45
# Size of source mod 2**32: 7531 bytes
"""
cri: sub-package suppporting color rendition calculations (colorrendition.py)
=============================================================================

utils/init_cri_defaults_database.py
-----------------------------------

 :_CRI_TYPE_DEFAULT: Default cri_type.

 :_CRI_DEFAULTS: default parameters for color fidelity and gamut area metrics 
                 (major dict has 9 keys (04-Jul-2017): 
                 sampleset [str/dict], 
                 ref_type [str], 
                 cieobs [str], 
                 avg [fcn handle], 
                 scale [dict], 
                 cspace [dict], 
                 catf [dict], 
                 rg_pars [dict], 
                 cri_specific_pars [dict])
                 
                * Supported cri-types:
                    * 'ciera','ciera-8','ciera-14','cierf',
                    * 'iesrf','iesrf-tm30-15','iesrf-tm30-18',
                    * 'cri2012','cri2012-hl17','cri2012-hl1000','cri2012-real210',
                    * 'mcri',
                    * 'cqs-v7.5','cqs-v9.0'

 :process_cri_type_input(): load a cri_type dict but overwrites any keys that 
                            have a non-None input in calling function.

utils/DE_scalers.py
-------------------

 :linear_scale(): | Linear color rendering index scale from CIE13.3-1974/1995:
                  | Rfi,a = 100 - c1*DEi,a. (c1 = 4.6)

 :log_scale(): | Log-based color rendering index scale from Davis & Ohno (2009):
               | Rfi,a = 10 * ln(exp((100 - c1*DEi,a)/10) + 1)

 :psy_scale(): | Psychometric based color rendering index scale from Smet et al. (2013):
               | Rfi,a = 100 * (2 / (exp(c1*abs(DEi,a)**(c2) + 1))) ** c3

utils/helpers.py
----------------

 :gamut_slicer(): Slices the gamut in nhbins slices and provides normalization 
                  of test gamut to reference gamut.

 :jab_to_rg(): Calculates gamut area index, Rg.

 :jab_to_rhi(): | Calculate hue bin measures: 
                |   Rfhi (local (hue bin) color fidelity)
                |   Rcshi (local chroma shift) 
                |   Rhshi (local hue shift)

 :spd_to_jab_t_r(): Calculates jab color values for a sample set illuminated
                    with test source and its reference illuminant.

 :spd_to_rg(): Calculates the color gamut index of spectral data 
               for a sample set illuminated with test source (data) 
               with respect to some reference illuminant.

 :spd_to_DEi(): Calculates color difference (~fidelity) of spectral data 
                between sample set illuminated with test source (data) 
                and some reference illuminant.

 :optimize_scale_factor(): Optimize scale_factor of cri-model in cri_type 
                           such that average Rf for a set of light sources is 
                           the same as that of a target-cri (default: 'ciera')

 :spd_to_cri(): Calculates the color rendering fidelity index 
                (CIE Ra, CIE Rf, IES Rf, CRI2012 Rf) of spectral data. 
                Can also output Rg, Rfhi, Rcshi, Rhshi, cct, duv, ...

utils/graphics.py
-----------------

 :plot_hue_bins(): Makes basis plot for Color Vector Graphic (CVG).

 :plot_ColorVectorGraphic(): Plots Color Vector Graphic (see IES TM30).

indices/indices.py
------------------

 :wrapper_functions_for_fidelity_type_metrics:
      | spd_to_ciera(): CIE 13.3 1995 version 
      | spd_to_ciera_133_1995(): CIE 13.3 1995 version
      | spd_to_cierf(): latest version
      | spd_to_cierf_224_2017(): CIE224-2017 version

      | spd_to_iesrf(): latest version
      | spd_to_iesrf_tm30(): latest version
      | spd_to_iesrf_tm30_15(): TM30-15 version
      | spd_to_iesrf_tm30_18(): TM30-18 version

      | spd_to_cri2012()
      | spd_to_cri2012_hl17()
      | spd_to_cri2012_hl1000()
      | spd_to_cri2012_real210()

 :wrapper_functions_for_gamut_area_metrics:
      | spd_to_iesrg(): latest version
      | spd_to_iesrg_tm30(): latest version
      | spd_to_iesrg_tm30_15(): TM30-15 version
      | spd_to_iesrg_tm30_18(): TM30-18 version

indices/mcri.py
---------------

 :spd_to_mcri(): | Calculates the memory color rendition index, Rm:  
                 | K. A. G. Smet, W. R. Ryckaert, M. R. Pointer, G. Deconinck, and P. Hanselaer, (2012) 
                 | “A memory colour quality metric for white light sources,” 
                 | Energy Build., vol. 49, no. C, pp. 216–225.

indices/cqs.py
--------------

 :spd_to_cqs(): | versions 7.5 and 9.0 are supported.  
                | W. Davis and Y. Ohno, 
                | “Color quality scale,” (2010), 
                | Opt. Eng., vol. 49, no. 3, pp. 33602–33616.

iestm30/iestm30_metrics.py
-------------------------- 

 :spd_to_ies_tm30_metrics(): Calculates IES TM30 metrics from spectral data.

iestm30/iestm30_graphics.py
---------------------------

 :plot_cri_graphics(): Plot graphical information on color rendition properties.

VFPX
----

 :Module_for_VectorField_and_Pixelation_CRI models.
  * see ?luxpy.cri.VFPX

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from utils.DE_scalers import linear_scale, log_scale, psy_scale
from utils.helpers import gamut_slicer, jab_to_rg, jab_to_rhi, jab_to_DEi, spd_to_DEi, spd_to_rg, spd_to_cri
from .indices.indices import *
from .utils.graphics import *
from .VFPX import VF_PX_models as VFPX
from iestm30.ies_tm30_graphics import plot_cri_graphics
from iestm30.ies_tm30_metrics import spd_to_ies_tm30_metrics
__all__ = [
 'linear_scale', 'log_scale', 'psy_scale']
__all__ += ['gamut_slicer', 'jab_to_rg', 'jab_to_rhi', 'jab_to_DEi',
 'spd_to_DEi', 'spd_to_rg', 'spd_to_cri']
__all__ += ['spd_to_ciera', 'spd_to_cierf',
 'spd_to_ciera_133_1995', 'spd_to_cierf_224_2017']
__all__ += ['spd_to_iesrf', 'spd_to_iesrg',
 'spd_to_iesrf_tm30', 'spd_to_iesrg_tm30',
 'spd_to_iesrf_tm30_15', 'spd_to_iesrg_tm30_15',
 'spd_to_iesrf_tm30_18', 'spd_to_iesrg_tm30_18']
__all__ += ['spd_to_cri2012', 'spd_to_cri2012_hl17', 'spd_to_cri2012_hl1000', 'spd_to_cri2012_real210']
__all__ += ['spd_to_mcri']
__all__ += ['spd_to_cqs']
__all__ += ['plot_hue_bins', 'plot_ColorVectorGraphic']
__all__ += ['VFPX']
__all__ += ['spd_to_ies_tm30_metrics']
__all__ += ['plot_cri_graphics']