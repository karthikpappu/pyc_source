# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/app/senpy/plugins/postprocessing/emotion/centroids.py
# Compiled at: 2019-07-10 06:17:55
# Size of source mod 2**32: 7093 bytes
from senpy.plugins import EmotionConversionPlugin
from senpy.models import EmotionSet, Emotion, Error
import logging
logger = logging.getLogger(__name__)

class CentroidConversion(EmotionConversionPlugin):
    __doc__ = '\n    This plugin converts emotion annotations from a dimensional model to a\n    categorical one, and vice versa. The centroids used in the conversion\n    are configurable and appear in the semantic description of the plugin.\n    '

    def __init__(self, info, *args, **kwargs):
        if 'centroids' not in info:
            raise Error('Centroid conversion plugins should provide the centroids in their senpy file')
        else:
            if 'onyx:doesConversion' not in info:
                if 'centroids_direction' not in info:
                    raise Error('Please, provide centroids direction')
                cf, ct = info['centroids_direction']
                info['onyx:doesConversion'] = [
                 {'onyx:conversionFrom':cf, 
                  'onyx:conversionTo':ct},
                 {'onyx:conversionFrom':ct, 
                  'onyx:conversionTo':cf}]
            if 'aliases' in info:
                aliases = info['aliases']
                ncentroids = {}
                for k1, v1 in info['centroids'].items():
                    nv1 = {}
                    for k2, v2 in v1.items():
                        nv1[aliases.get(k2, k2)] = v2

                    ncentroids[aliases.get(k1, k1)] = nv1

                info['centroids'] = ncentroids
            (super(CentroidConversion, self).__init__)(info, *args, **kwargs)
            self.dimensions = set()
            for c in self.centroids.values():
                self.dimensions.update(c.keys())

            self.neutralPoints = self.get('neutralPoints', dict())
            if not self.neutralPoints:
                for i in self.dimensions:
                    self.neutralPoints[i] = self.get('neutralValue', 0)

    def _forward_conversion(self, original):
        """Sum the VAD value of all categories found weighted by intensity.
        Intensities are scaled by onyx:maxIntensityValue if it is present, else maxIntensityValue
        is assumed to be one. Emotion entries that do not have onxy:hasEmotionIntensity specified
        are assumed to have maxIntensityValue. Emotion entries that do not have
        onyx:hasEmotionCategory specified are ignored."""
        res = Emotion()
        maxIntensity = float(original.get('onyx:maxIntensityValue', 1))
        for e in original.onyx__hasEmotion:
            category = e.get('onyx:hasEmotionCategory', None)
            if not category:
                pass
            else:
                intensity = e.get('onyx:hasEmotionIntensity', maxIntensity) / maxIntensity
                if not intensity:
                    continue
            centroid = self.centroids.get(category, None)
            if centroid:
                for dim, value in centroid.items():
                    neutral = self.neutralPoints[dim]
                    if dim not in res:
                        res[dim] = 0
                    res[dim] += (value - neutral) * intensity + neutral

        return res

    def _backwards_conversion(self, original):
        """Find the closest category"""
        centroids = self.centroids
        neutralPoints = self.neutralPoints
        dimensions = self.dimensions

        def distance_k(centroid, original, k):
            return (centroid.get(k, neutralPoints[k]) - original.get(k, neutralPoints[k])) ** 2

        def distance(centroid):
            return sum(distance_k(centroid, original, k) for k in dimensions)

        distances = {k:distance(centroids[k]) for k in centroids}
        logger.debug('Converting %s', original)
        logger.debug('Centroids: %s', centroids)
        logger.debug('Distances: %s', distances)
        emotion = min(distances, key=(lambda x: distances[x]))
        result = Emotion(onyx__hasEmotionCategory=emotion)
        result.onyx__algorithmConfidence = distance(centroids[emotion])
        return result

    def convert(self, emotionSet, fromModel, toModel, params):
        cf, ct = self.centroids_direction
        logger.debug('{}\n{}\n{}\n{}'.format(emotionSet, fromModel, toModel, params))
        e = EmotionSet()
        if fromModel == cf:
            if toModel == ct:
                e.onyx__hasEmotion.append(self._forward_conversion(emotionSet))
        elif fromModel == ct:
            if toModel == cf:
                for i in emotionSet.onyx__hasEmotion:
                    e.onyx__hasEmotion.append(self._backwards_conversion(i))

        else:
            raise Error('EMOTION MODEL NOT KNOWN. Cannot convert from {} to {}'.format(fromModel, toModel))
        yield e

    def test(self, info=None):
        if not info:
            info = {'name':'CentroidTest',  'description':'Centroid test', 
             'version':0, 
             'centroids':{'c1':{'V1':0.5, 
               'V2':0.5}, 
              'c2':{'V1':-0.5, 
               'V2':0.5}, 
              'c3':{'V1':-0.5, 
               'V2':-0.5}, 
              'c4':{'V1':0.5, 
               'V2':-0.5}}, 
             'aliases':{'V1':'X-dimension', 
              'V2':'Y-dimension'}, 
             'centroids_direction':[
              'emoml:big6', 'emoml:fsre-dimensions']}
        else:
            c = CentroidConversion(info)
            es1 = EmotionSet()
            e1 = Emotion()
            e1.onyx__hasEmotionCategory = 'c1'
            es1.onyx__hasEmotion.append(e1)
            res = c._forward_conversion(es1)
            assert res['X-dimension'] == 0.5
            assert res['Y-dimension'] == 0.5
            e2 = Emotion()
            e2.onyx__hasEmotionCategory = 'c2'
            es1.onyx__hasEmotion.append(e2)
            res = c._forward_conversion(es1)
            assert res['X-dimension'] == 0
            assert res['Y-dimension'] == 1
            e = Emotion()
            e['X-dimension'] = -0.2
            e['Y-dimension'] = -0.3
            res = c._backwards_conversion(e)
            assert res['onyx:hasEmotionCategory'] == 'c3'
            e = Emotion()
            e['X-dimension'] = -0.2
            e['Y-dimension'] = 0.3
            res = c._backwards_conversion(e)
            assert res['onyx:hasEmotionCategory'] == 'c2'