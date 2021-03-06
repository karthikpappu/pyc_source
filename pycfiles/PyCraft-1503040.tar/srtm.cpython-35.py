# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/pathprof/srtm.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 19885 bytes
__doc__ = "\nNote, there are various versions of SRTM data. Quasi-official are Versions 1\nand 2.1 available on https://dds.cr.usgs.gov/srtm/. There is even a NASA\nversion 3, but we couldn't find a site for direct download. It may work\nwith an EarthData Account on https://lpdaac.usgs.gov/data_access/data_pool.\n\nThen, there is V4.1 by CGIAR\n(ftp://srtm.csi.cgiar.org/SRTM_V41/SRTM_Data_GeoTiff/)\nand an unofficial version by viewfinderpanoramas.org (see\nhttp://viewfinderpanoramas.org/Coverage%20map%20viewfinderpanoramas_org3.htm).\n\nFor automatic download we should use the 2.1 version by NASA. V4.1 is in\nGeoTiff format, which we currently don't support. viewfinderpanoramas.org\nis probably superior to 2.1 (maybe even to V4.1), but not official.\n\nV4.1 and viewfinderpanoramas forbid commercial use (without explicit\npermission).\n"
from __future__ import absolute_import, unicode_literals, division, print_function
import os, warnings, shutil
from zipfile import ZipFile
import re, json, glob
from functools import lru_cache
import numpy as np
from scipy.interpolate import RegularGridInterpolator, RectBivariateSpline
from astropy.utils.data import get_pkg_data_filename, download_file
from astropy import units as apu
from .. import utils
__all__ = [
 'TileNotAvailableOnServerError',
 'TileNotAvailableOnDiskError',
 'TileNotAvailableOnDiskWarning',
 'TilesSizeError',
 'SrtmConf', 'srtm_height_data']
_NASA_JSON_NAME = get_pkg_data_filename('data/nasa.json')
_VIEWPANO_NAME = get_pkg_data_filename('data/viewpano.npy')
with open(_NASA_JSON_NAME, 'r') as (f):
    NASA_TILES = json.load(f)
VIEWPANO_TILES = np.load(_VIEWPANO_NAME)

class TileNotAvailableOnServerError(Exception):
    pass


class TileNotAvailableOnDiskError(Exception):
    pass


class TileNotAvailableOnDiskWarning(UserWarning):
    pass


class TilesSizeError(Exception):
    pass


class SrtmConf(utils.MultiState):
    """SrtmConf"""
    _attributes = ('srtm_dir', 'download', 'server', 'interp', 'spline_opts', 'tile_size',
                   'hgt_res')
    srtm_dir = os.environ.get('SRTMDATA', '.')
    download = 'never'
    server = 'nasa_v2.1'
    interp = 'linear'
    spline_opts = (3, 0)
    tile_size = 1201
    hgt_res = 90.0

    @classmethod
    def validate(cls, **kwargs):
        """
        This checks, if the provided inputs for `download` and `server` are
        allowed. Possible values are:

        - `download`:  'never', 'missing', 'always'
        - `server`:  'nasa_v2.1', 'nasa_v1.0', 'viewpano'
        - `interp`:  'nearest', 'linear', 'spline'
        - `spline_opts`:  tuple(k, s) (k = degree, s = smoothing factor)

        """
        for k, v in kwargs.items():
            if k == 'srtm_dir':
                if not isinstance(v, str):
                    raise ValueError('"srtm_dir" option must be a string.')
                if k == 'download' and v not in ('never', 'missing', 'always'):
                    raise ValueError('Only the values "never", "missing", and "always" are supported for "download" option.')
                if k == 'server' and v not in ('nasa_v2.1', 'nasa_v1.0', 'viewpano'):
                    raise ValueError('Only the values "nasa_v2.1", "nasa_v1.0", and "viewpano" are supported for "server" option.')
                if k == 'interp' and v not in ('nearest', 'linear', 'spline'):
                    raise ValueError('Only the values "nearest", "linear", and "spline" are supported for "interp" option.')
                if k == 'spline_opts':
                    if not isinstance(v, tuple):
                        raise ValueError('"spline_opts" option must be a tuple (k, s).')
                    if not len(v) == 2:
                        raise ValueError('"spline_opts" option must be a tuple (k, s).')
                    if not isinstance(v[0], int):
                        raise ValueError('"spline_opts" k-value must be an int.')
                    if not isinstance(v[1], (int, float)):
                        raise ValueError('"spline_opts" s-value must be a float.')
                    if k in ('tile_size', 'hgt_res'):
                        raise KeyError('Setting the {} manually not allowed! (This is automatically inferred from data.)'.format(k))

        return kwargs

    @classmethod
    def hook(cls, **kwargs):
        if 'srtm_dir' in kwargs and kwargs['srtm_dir'] != cls.srtm_dir:
            get_tile_interpolator.cache_clear()
        if 'download' in kwargs and kwargs['download'] != cls.download:
            get_tile_interpolator.cache_clear()
        if 'server' in kwargs and kwargs['server'] != cls.server:
            get_tile_interpolator.cache_clear()

    @classmethod
    def __repr__(cls):
        return '<SrtmConf dir: {}, download: {}, server: {}, interp: {}, spline_opts: {}>'.format(cls.srtm_dir, cls.download, cls.server, cls.interp, cls.spline_opts)

    @classmethod
    def __str__(cls):
        return 'SrtmConf\n  directory: {}\n  download: {}\n  server: {}\n  interp: {}\n  spline_opts: {}'.format(cls.srtm_dir, cls.download, cls.server, cls.interp, cls.spline_opts)


def _hgt_filename(ilon, ilat):
    return '{:1s}{:02d}{:1s}{:03d}.hgt'.format('N' if ilat >= 0 else 'S', abs(ilat), 'E' if ilon >= 0 else 'W', abs(ilon))


def _check_availability(ilon, ilat):
    server = SrtmConf.server
    tile_name = _hgt_filename(ilon, ilat)
    if server.startswith('nasa_v'):
        for continent, tiles in NASA_TILES.items():
            if tile_name in tiles:
                break
        else:
            raise TileNotAvailableOnServerError('No tile found for ({}d, {}d) in list of available tiles.'.format(ilon, ilat))

        return continent
    if server == 'viewpano':
        tiles = VIEWPANO_TILES['tile']
        idx = np.where(tiles == tile_name)
        if len(tiles[idx]) == 0:
            raise TileNotAvailableOnServerError('No tile found for ({}d, {}d) in list of available tiles.'.format(ilon, ilat))
        return VIEWPANO_TILES['zipfile'][idx][0]


def _check_consistent_tile_sizes(srtm_dir):
    all_files = glob.glob(os.path.join(srtm_dir, '**', '*.hgt'), recursive=True)
    file_sizes = set(os.stat(fname).st_size for fname in all_files)
    if len(file_sizes) == 0:
        raise OSError('No .hgt tiles found in given srtm path.')
    elif len(file_sizes) > 1:
        raise TilesSizeError('Inconsistent tile sizes found in given srtm path. All tiles must be the same size!')
    tile_size = int(np.sqrt(file_sizes.pop() / 2) + 0.5)
    return tile_size


def _download(ilon, ilat):
    srtm_dir = SrtmConf.srtm_dir
    server = SrtmConf.server
    tile_name = _hgt_filename(ilon, ilat)
    tile_path = os.path.join(srtm_dir, tile_name)
    if server.startswith('nasa_v'):
        if server == 'nasa_v1.0':
            base_url = 'https://dds.cr.usgs.gov/srtm/version1/'
        elif server == 'nasa_v2.1':
            base_url = 'https://dds.cr.usgs.gov/srtm/version2_1/SRTM3/'
        continent = _check_availability(ilon, ilat)
        full_url = base_url + continent + '/' + tile_name + '.zip'
        tmp_path = download_file(full_url)
        shutil.move(tmp_path, tile_path + '.zip')
        with ZipFile(tile_path + '.zip', 'r') as (zf):
            zf.extractall(srtm_dir)
        try:
            os.remove(tile_path + '.zip')
        except (FileNotFoundError, PermissionError):
            pass

    if server == 'viewpano':
        base_url = 'http://viewfinderpanoramas.org/dem3/'
        zipfile_name = _check_availability(ilon, ilat)
        super_tile_path = os.path.join(srtm_dir, zipfile_name)
        full_url = base_url + zipfile_name
        tmp_path = download_file(full_url)
        shutil.move(tmp_path, super_tile_path)
        with ZipFile(super_tile_path, 'r') as (zf):
            zf.extractall(srtm_dir)
        try:
            os.remove(super_tile_path)
        except (FileNotFoundError, PermissionError):
            pass


def _extract_hgt_coords(hgt_name):
    """
    Extract coordinates from hgt-filename (lower left corner).

    Properly handles EW and NS substrings. Longitude range: -180 .. 179 deg
    """
    _codes = {'E': 1, 'W': -1, 'N': 1, 'S': -1}
    yc, wy0, xc, wx0 = re.search('.*([NS])(-?\\d*)([EW])(\\d*).hgt.*', hgt_name).groups()
    return (
     _codes[xc] * int(wx0), _codes[yc] * int(wy0))


def _get_hgt_diskpath(tile_name):
    srtm_dir = SrtmConf.srtm_dir
    _files = glob.glob(os.path.join(srtm_dir, '**', tile_name), recursive=True)
    if len(_files) > 1:
        raise IOError('{} exists {} times in {} and its sub-directories'.format(tile_name, len(_files), srtm_dir))
    else:
        if len(_files) == 0:
            return
        else:
            return _files[0]


def get_hgt_file(ilon, ilat):
    _check_availability(ilon, ilat)
    srtm_dir = SrtmConf.srtm_dir
    tile_name = _hgt_filename(ilon, ilat)
    hgt_file = _get_hgt_diskpath(tile_name)
    download = SrtmConf.download
    if download == 'always' or hgt_file is None and download == 'missing':
        _download(ilon, ilat)
    hgt_file = _get_hgt_diskpath(tile_name)
    if hgt_file is None:
        raise TileNotAvailableOnDiskError('No hgt-file found for ({}d, {}d), was looking for {}\nin directory: {}'.format(ilon, ilat, tile_name, srtm_dir))
    return hgt_file


def get_tile_data(ilon, ilat):
    try:
        hgt_file = get_hgt_file(ilon, ilat)
        _check_consistent_tile_sizes(SrtmConf.srtm_dir)
        tile = np.fromfile(hgt_file, dtype='>i2')
        tile_size = int(np.sqrt(tile.size) + 0.5)
        hgt_res = 108000.0 / (tile_size - 1)
        SrtmConf.set(tile_size=tile_size, _do_validate=False)
        SrtmConf.set(hgt_res=hgt_res, _do_validate=False)
        tile = tile.reshape((tile_size, tile_size))[::-1]
        bad_mask = (tile == 32768) | (tile == -32768)
        tile = tile.astype(np.float32)
        tile[bad_mask] = np.nan
    except TileNotAvailableOnServerError:
        tile_size = 5
        tile = np.zeros((tile_size, tile_size), dtype=np.float32)
    except TileNotAvailableOnDiskError:
        tile_size = 5
        tile = np.zeros((tile_size, tile_size), dtype=np.float32)
        tile_name = _hgt_filename(ilon, ilat)
        srtm_dir = SrtmConf.srtm_dir
        warnings.warn('\nNo hgt-file found for ({}d, {}d) - was looking for file {}\nin directory: {}\nWill set terrain heights in this area to zero. Note, you can have pycraf\ndownload missing tiles automatically - just use "pycraf.pathprof.SrtmConf"\n(see its documentation).'.format(ilon, ilat, tile_name, srtm_dir), category=TileNotAvailableOnDiskWarning, stacklevel=1)

    dx = dy = 1.0 / (tile_size - 1)
    x, y = np.ogrid[0:tile_size, 0:tile_size]
    lons, lats = x * dx + ilon, y * dy + ilat
    return (
     lons, lats, tile)


@lru_cache(maxsize=36, typed=False)
def get_tile_interpolator(ilon, ilat, interp, spline_opts):
    lons, lats, tile = get_tile_data(ilon, ilat)
    tile = np.nan_to_num(tile)
    if interp in ('nearest', 'linear'):
        _tile_interpolator = RegularGridInterpolator((
         lons[:, 0], lats[0]), tile.T, method=interp)
    elif interp == 'spline':
        kx = ky = spline_opts[0]
        s = spline_opts[1]
        _tile_interpolator = RectBivariateSpline(lons[:, 0], lats[0], tile.T, kx=kx, ky=ky, s=s)
    return _tile_interpolator


def _srtm_height_data(lons, lats):
    lons_g, lats_g = np.broadcast_arrays(lons, lats)
    heights = np.empty(lons_g.shape, dtype=np.float32)
    ilons = np.floor(lons).astype(np.int32)
    ilats = np.floor(lats).astype(np.int32)
    interp = SrtmConf.interp
    spl_opts = SrtmConf.spline_opts
    for uilon in np.unique(ilons):
        for uilat in np.unique(ilats):
            mask = (ilons == uilon) & (ilats == uilat)
            if interp in ('nearest', 'linear'):
                ifunc = get_tile_interpolator(uilon, uilat, interp, None)
                heights[mask] = ifunc((lons_g[mask], lats_g[mask]))
            elif interp == 'spline':
                ifunc = get_tile_interpolator(uilon, uilat, interp, spl_opts)
                heights[mask] = ifunc(lons_g[mask], lats_g[mask], grid=False)

    return heights


@utils.ranged_quantity_input(lons=(
 -180, 180, apu.deg), lats=(
 -90, 90, apu.deg), strip_input_units=True, output_unit=apu.m)
def srtm_height_data(lons, lats):
    """
    Interpolated SRTM terrain data extracted from ".hgt" files.

    Parameters
    ----------
    lons, lats : `~astropy.units.Quantity`
        Geographic longitudes/latitudes for which to return height data [deg]

    Returns
    -------
    heights : `~astropy.units.Quantity`
        SRTM heights [m]

    Raises
    ------
    TileNotAvailableOnDiskWarning : UserWarning
        If a tile is requested that should exist on the chosen server
        but is not available on disk (at least not in the search path)
        a warning is raised. In this case, the tile height data is set
        to Zeros.

    Notes
    -----
    - `SRTM <https://www2.jpl.nasa.gov/srtm/>`_ data tiles (`*.hgt`) need
      to be accessible by `pycraf`.  It is assumed that these are either
      present in the current working directory or in the path defined by the
      `SRTMDATA` environment variable (sub-directories are also parsed).
      Alternatively, use the `~pycraf.pathprof.SrtmConf` manager to
      change the directory, where `pycraf` looks for SRTM data, during
      run-time. The `~pycraf.pathprof.SrtmConf` manager also offers
      additional features such as automatic downloading of missing
      tiles or applying different interpolation methods (e.g., splines).
      For details see :ref:`working_with_srtm`.
    """
    return _srtm_height_data(lons, lats)


if __name__ == '__main__':
    print('This not a standalone python program! Use as module.')