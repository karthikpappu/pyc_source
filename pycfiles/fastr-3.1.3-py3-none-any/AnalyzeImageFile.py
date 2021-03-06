# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/datatypes/AnalyzeImageFile.py
# Compiled at: 2019-06-04 03:03:06
import urlparse, fastr
from fastr.data import url
from fastr.datatypes import URLType

class AnalyzeImageFile(URLType):
    description = 'Analyze Image file formate'
    extension = 'hdr'

    @classmethod
    def content(cls, invalue, outvalue=None):
        fastr.log.debug(('Determining content of AnalyzeImageFile from invalue "{}" and outvalue "{}"').format(invalue, outvalue))

        def substitute_extension(path):
            fastr.log.debug(('Substituting: {}').format(path))
            suffixes = {'.hdr.gz': '.img.gz', '.hdr': '.img'}
            for hdr_suffix, img_suffix in suffixes.items():
                if path.endswith(hdr_suffix):
                    return path[:-len(hdr_suffix)] + img_suffix

            raise ValueError(('Extension is not valid for AnalyzeImageFile {}').format(path))

        if url.isurl(invalue):
            parts = urlparse.urlparse(invalue)
            fastr.log.debug(('input URL parts found: {}').format(parts))
            path = substitute_extension(parts.path)
            in_img = urlparse.urlunparse((parts.scheme, parts.netloc, path, parts.params, parts.query, parts.fragment))
        else:
            in_img = substitute_extension(invalue)
            fastr.log.debug(('input path found: {} -> {}').format(invalue, in_img))
        if outvalue is not None:
            if url.isurl(outvalue):
                parts = urlparse.urlparse(outvalue)
                fastr.log.debug(('output URL parts found: {}').format(parts))
                path = substitute_extension(parts.path)
                out_img = urlparse.urlunparse((parts.scheme, parts.netloc, path, parts.params, parts.query, parts.fragment))
            else:
                out_img = substitute_extension(outvalue)
                fastr.log.debug(('output path found: {} -> {}').format(outvalue, out_img))
            contents = [(invalue, outvalue), (in_img, out_img)]
        else:
            contents = [
             invalue, in_img]
        return contents