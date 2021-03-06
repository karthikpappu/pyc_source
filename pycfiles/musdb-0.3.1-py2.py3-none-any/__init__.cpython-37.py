# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/faro/repositories/sigsep-mus-tools/build/lib/musdb/__init__.py
# Compiled at: 2018-03-02 02:52:03
# Size of source mod 2**32: 16074 bytes
from __future__ import print_function
from .audio_classes import Track, Source, Target
from os import path as op
from six.moves import map
import multiprocessing, soundfile as sf, collections, numpy as np, functools, signal, yaml, tqdm, os, musdb
__version__ = '0.2.3'

class DB(object):
    __doc__ = '\n    The musdb DB Object\n\n    Parameters\n    ----------\n    root_dir : str, optional\n        musdb Root path. If set to `None` it will be read\n        from the `MUSDB_PATH` environment variable\n\n    subsets : str or list, optional\n        select a _musdb_ subset `train` or `test` (defaults to both)\n\n    is_wav : boolean, optional\n        expect subfolder with wav files for each source instead stems,\n        defaults to stems\n\n\n    Attributes\n    ----------\n    setup_file : str\n        path to yaml file. default: `setup.yaml`\n    root_dir : str\n        musdb Root path. Default is `MUSDB_PATH` env\n    sources_dir : str\n        path to Sources directory\n    sources_names : list[str]\n        list of names of sources\n    targets_names : list[str]\n        list of names of targets\n    setup : Dict\n        loaded yaml configuration\n\n    Methods\n    -------\n    load_mus_tracks()\n        Iterates through the musdb folder structure and\n        returns ``Track`` objects\n    test(user_function)\n        Test the musdb processing\n    run(user_function=None, estimates_dir=None)\n        Run the musdb processing and saving the estimates\n\n    '

    def __init__(self, root_dir=None, setup_file=None, is_wav=False):
        if root_dir is None:
            if 'MUSDB_PATH' in os.environ:
                self.root_dir = os.environ['MUSDB_PATH']
            else:
                raise RuntimeError('Variable `MUSDB_PATH` has not been set.')
        else:
            self.root_dir = root_dir
        if setup_file is not None:
            setup_path = op.join(self.root_dir, setup_file)
        else:
            setup_path = os.path.join(musdb.__path__[0], 'configs', 'mus.yaml')
        with open(setup_path, 'r') as (f):
            self.setup = yaml.load(f)
        self.sources_names = list(self.setup['sources'].keys())
        self.targets_names = list(self.setup['targets'].keys())
        self.is_wav = is_wav

    def load_mus_tracks(self, subsets=None, tracknames=None):
        """Parses the musdb folder structure, returns list of `Track` objects

        Parameters
        ==========
        subsets : list[str], optional
            select a _musdb_ subset `train` or `test`.
            Default `None` loads both sets.

        tracknames : list[str], optional
            select musdb track names, defaults to all tracks

        Returns
        -------
        list[Track]
            return a list of ``Track`` Objects
        """
        if subsets is not None:
            if isinstance(subsets, str):
                subsets = [
                 subsets]
            else:
                subsets = subsets
        else:
            subsets = [
             'train', 'test']
        tracks = []
        for subset in subsets:
            subset_folder = op.join(self.root_dir, subset)
            for _, folders, files in os.walk(subset_folder):
                if self.is_wav:
                    for track_name in sorted(folders):
                        if tracknames is not None:
                            if track_name not in tracknames:
                                continue
                        track_folder = op.join(subset_folder, track_name)
                        track = Track(name=track_name,
                          path=(op.join(track_folder, self.setup['mixture'])),
                          subset=subset,
                          stem_id=(self.setup['stem_ids']['mixture']),
                          is_wav=(self.is_wav))
                        sources = {}
                        for src, source_file in list(self.setup['sources'].items()):
                            abs_path = op.join(track_folder, source_file)
                            if os.path.exists(abs_path):
                                sources[src] = Source(name=src,
                                  path=abs_path,
                                  stem_id=(self.setup['stem_ids'][src]),
                                  is_wav=(self.is_wav))

                        track.sources = sources
                        targets = collections.OrderedDict()
                        for name, target_srcs in list(self.setup['targets'].items()):
                            target_sources = []
                            for source, gain in list(target_srcs.items()):
                                if source in list(track.sources.keys()):
                                    track.sources[source].gain = float(gain)
                                    target_sources.append(sources[source])

                            if target_sources:
                                targets[name] = Target(sources=target_sources)

                        track.targets = targets
                        tracks.append(track)

                else:
                    for track_name in sorted(files):
                        if 'stem' in track_name:
                            if track_name.endswith('.mp4'):
                                if tracknames is not None:
                                    if track_name.split('.stem.mp4')[0] not in tracknames:
                                        continue
                            track = Track(name=track_name,
                              path=(op.join(subset_folder, track_name)),
                              subset=subset,
                              stem_id=(self.setup['stem_ids']['mixture']),
                              is_wav=(self.is_wav))
                            sources = {}
                            for src, source_file in list(self.setup['sources'].items()):
                                abs_path = op.join(subset_folder, track_name)
                                if os.path.exists(abs_path):
                                    sources[src] = Source(name=src,
                                      path=abs_path,
                                      stem_id=(self.setup['stem_ids'][src]),
                                      is_wav=(self.is_wav))

                            track.sources = sources
                            targets = collections.OrderedDict()
                            for name, target_srcs in list(self.setup['targets'].items()):
                                target_sources = []
                                for source, gain in list(target_srcs.items()):
                                    if source in list(track.sources.keys()):
                                        track.sources[source].gain = float(gain)
                                        target_sources.append(sources[source])

                                if target_sources:
                                    targets[name] = Target(sources=target_sources)

                            track.targets = targets
                            tracks.append(track)

        return tracks

    def _save_estimates(self, user_estimates, track, estimates_dir, write_stems=False):
        track_estimate_dir = op.join(estimates_dir, track.subset, track.name)
        if not os.path.exists(track_estimate_dir):
            os.makedirs(track_estimate_dir)
        for target, estimate in list(user_estimates.items()):
            target_path = op.join(track_estimate_dir, target + '.wav')
            sf.write(target_path, estimate, track.rate)

    def test(self, user_function):
        """Test the musdb user_function output

        Parameters
        ----------
        user_function : callable, optional
            function which separates the mixture into estimates.

        Raises
        ------
        TypeError
            If the provided function handle is not callable.

        ValueError
            If the output is not compliant to the bsseval methods

        See Also
        --------
        run : Process the musdb
        """
        if not hasattr(user_function, '__call__'):
            raise TypeError('Please provide a function.')
        test_track = Track(name='test - test')
        signal = np.random.random((66000, 2))
        test_track.audio = signal
        test_track.rate = 44100
        test_track.subset = 'test'
        sources = {}
        for src, source_file in list(self.setup['sources'].items()):
            source = Source(name=src)
            source.audio = signal
            source.rate = test_track.rate
            sources[src] = source

        test_track.sources = sources
        targets = collections.OrderedDict()
        for name, target_srcs in list(self.setup['targets'].items()):
            target_sources = []
            for source, gain in list(target_srcs.items()):
                if source in list(test_track.sources.keys()):
                    test_track.sources[source].gain = float(gain)
                    target_sources.append(sources[source])

            if target_sources:
                targets[name] = Target(sources=target_sources)

        test_track.targets = targets
        user_results = user_function(test_track)
        if isinstance(user_results, dict):
            for target, audio in list(user_results.items()):
                if target not in self.targets_names:
                    raise ValueError("Target '%s' not supported!" % target)
                d = audio.dtype
                if not np.issubdtype(d, np.float32):
                    if not np.issubdtype(d, np.float64):
                        raise ValueError('Estimate is not of type numpy.float32 or float64')
                    if audio.shape != signal.shape:
                        raise ValueError('Shape of estimate does not match input shape')

        else:
            raise ValueError('output needs to be a dict')
        return True

    def _process_function(self, track, user_function, estimates_dir):
        user_results = user_function(track)
        if estimates_dir is not None:
            if user_results is None:
                raise ValueError('Processing did not yield any results, please set estimate_dir to None')
            else:
                self._save_estimates(user_results, track, estimates_dir)

    def run(self, user_function, tracks=None, estimates_dir=None, subsets=None, parallel=False, cpus=4):
        """Run the musdb processing

        Parameters
        ----------
        user_function : callable
            function which separates the mixture into estimates.
        tracks : list[Track], optional
            select a list of tracks
        subsets : list[str], optional
            select a _musdb_ subset `train` or `test`. Defaults to both
        estimates_dir : str, optional
            path to the user provided estimates. Directory will be
            created if it does not exist. Default is `none` which means that
            the results are not saved.
        parallel: bool, optional
            activate multiprocessing
        cpus: int, optional
            set number of cores if `parallel` mode is active, defaults to 4

        Raises
        ------
        RuntimeError
            If the provided function handle is not callable.

        Returns
        -------
        results : Dict
            returns the return value of the user_function

        See Also
        --------
        test : Test the user provided function
        """
        if user_function is None:
            raise RuntimeError('Provide a function!')
        else:
            if tracks is None:
                tracks = self.load_mus_tracks(subsets=subsets)
            results = False
            if parallel:
                pool = multiprocessing.Pool(cpus, initializer=init_worker)
                results = list(tqdm.tqdm(pool.imap_unordered(func=functools.partial(process_function_alias,
                  self,
                  user_function=user_function,
                  estimates_dir=estimates_dir),
                  iterable=tracks,
                  chunksize=1),
                  total=(len(tracks))))
                pool.close()
                pool.join()
            else:
                results = list(tqdm.tqdm((map(lambda x: self._process_function(x, user_function, estimates_dir), tracks)),
                  total=(len(tracks))))
        return results


def process_function_alias(obj, *args, **kwargs):
    return (obj._process_function)(*args, **kwargs)


def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)