# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/processes/convert.py
# Compiled at: 2020-03-23 15:53:29
# Size of source mod 2**32: 3902 bytes
import logging
from rasterio.dtypes import dtype_ranges
logger = logging.getLogger(__name__)

def execute(mp, resampling='nearest', band_indexes=None, td_matching_method='gdal', td_matching_max_zoom=None, td_matching_precision=8, td_fallback_to_higher_zoom=False, clip_pixelbuffer=0, scale_ratio=1.0, scale_offset=0.0, clip_to_output_dtype=None, **kwargs):
    """
    Convert and optionally clip input raster data.

    Inputs
    ------
    raster
        Singleband or multiband data input.
    clip (optional)
        Vector data used to clip output.

    Parameters
    ----------
    resampling : str (default: 'nearest')
        Resampling used when reading from TileDirectory.
    band_indexes : list
        Bands to be read.
    td_matching_method : str ('gdal' or 'min') (default: 'gdal')
        gdal: Uses GDAL's standard method. Here, the target resolution is
            calculated by averaging the extent's pixel sizes over both x and y
            axes. This approach returns a zoom level which may not have the
            best quality but will speed up reading significantly.
        min: Returns the zoom level which matches the minimum resolution of the
            extents four corner pixels. This approach returns the zoom level
            with the best possible quality but with low performance. If the
            tile extent is outside of the destination pyramid, a
            TopologicalError will be raised.
    td_matching_max_zoom : int (optional, default: None)
        If set, it will prevent reading from zoom levels above the maximum.
    td_matching_precision : int (default: 8)
        Round resolutions to n digits before comparing.
    td_fallback_to_higher_zoom : bool (default: False)
        In case no data is found at zoom level, try to read data from higher
        zoom levels. Enabling this setting can lead to many IO requests in
        areas with no data.
    clip_pixelbuffer : int
        Use pixelbuffer when clipping output by geometry. (default: 0)
    scale_ratio : float
        Scale factor for input values. (default: 1.0)
    scale_offset : float
        Offset to add to input values. (default: 0.0)
    clip_to_output_dtype : str
        Clip output values to range of given dtype. (default: None)

    Output
    ------
    np.ndarray
    """
    if 'clip' in mp.params['input']:
        clip_geom = mp.open('clip').read()
        if not clip_geom:
            logger.debug('no clip data over tile')
            return 'empty'
    else:
        clip_geom = []
    with mp.open('raster') as (raster):
        logger.debug('reading input raster')
        raster_data = raster.read(indexes=band_indexes, resampling=resampling, matching_method=td_matching_method, matching_max_zoom=td_matching_max_zoom, matching_precision=td_matching_precision, fallback_to_higher_zoom=td_fallback_to_higher_zoom)
        if raster_data.mask.all():
            logger.debug('raster empty')
            return 'empty'
    if scale_offset != 0.0:
        logger.debug('apply scale offset %s', scale_offset)
        raster_data = raster_data.astype('float64', copy=False) + scale_offset
    if scale_ratio != 1.0:
        logger.debug('apply scale ratio %s', scale_ratio)
        raster_data = raster_data.astype('float64', copy=False) * scale_ratio
    if (scale_offset != 0.0 or scale_ratio != 1.0) and clip_to_output_dtype in dtype_ranges:
        logger.debug('clip to output dtype ranges')
        raster_data.clip(*dtype_ranges[clip_to_output_dtype], out=raster_data)
    if clip_geom:
        logger.debug('clipping output with geometry')
        return mp.clip(raster_data, clip_geom, clip_buffer=clip_pixelbuffer)
    else:
        return raster_data