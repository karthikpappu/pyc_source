# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/cctagutils/lookup.py
# Compiled at: 2007-03-15 10:29:40
"""Support functions for verification of embedded license claims."""
__id__ = '$Id: lookup.py 711 2007-02-20 17:43:03Z nyergler $'
__version__ = '$Revision: 711 $'
__copyright__ = '(c) 2004, Creative Commons, Nathan R. Yergler'
__license__ = 'licensed under the GNU GPL2'
import ccrdf, ccrdf.rdfextract as rdfextract
from ccrdf.aaronrdf import cc, xhtml
import cctagutils
from cctagutils.metadata import metadata

def parseClaim(claim):
    results = {}
    vtext = 'verify at '
    vloc = claim.find(vtext)
    if vloc != -1:
        results['verify at'] = claim[vloc + len(vtext):].strip()
        claim = claim[:vloc]
    ltext = 'licensed to the public under '
    lloc = claim.lower().find(ltext)
    if lloc != -1:
        results['license'] = claim[lloc + len(ltext):].strip()
        claim = claim[:lloc]
    results['copyright'] = claim.strip()
    return results


def lookup(filename):
    """Returns True of False if the embedded claim can be verified."""
    if verify(filename) > 0:
        return True
    else:
        return False


def verify(filename):
    """Extracts license claim information from a file and verifies it.
    Returns the following status codes:
    1     Verified
    0     No RDF
    -1    Work information not found (possible SHA1 mismatch)
    -2    Verification license does not match claim.

    Verification is performed against an embedded "claim" as well as
    checking the page specified by the "web statement".
    """
    status = cctagutils.VERIFY_NO_RDF
    file_metadata = metadata(filename)
    sha1 = 'urn:sha1:%s' % cctagutils.rdf.fileHash(filename)
    rdf_urls = []
    claim = file_metadata.getClaim()
    if claim:
        fileinfo = parseClaim(claim)
        rdf_urls.append(fileinfo['verify at'])
    if file_metadata.getMetadataUrl():
        rdf_urls.append(file_metadata.getMetadataUrl())
    rdf_store = ccrdf.rdfdict.rdfStore()
    extractor = rdfextract.RdfExtractor()
    for u in rdf_urls:
        extractor.extractUrlToGraph(u, rdf_store.graph)

    license_assertions = [ l for l in rdf_store.graph.objects(sha1, cc.license) ]
    license_assertions += [ l for l in rdf_store.graph.objects(sha1, xhtml.license) ]
    if len(license_assertions) == 1 and license_assertions[0] == file_metadata.getLicense():
        return cctagutils.VERIFY_VERIFIED
    elif len(license_assertions) == 0:
        return cctagutils.VERIFY_NO_MATCH
    else:
        if file_metadata.getLicense() not in license_assertions:
            return cctagutils.VERIFY_NO_MATCH
        for l in license_assertions:
            if l != file_metadata.getLicense():
                return cctagutils.VERIFY_CONFLICTING_ASSERTIONS

        return cctagutils.VERIFY_VERIFIED
    return status