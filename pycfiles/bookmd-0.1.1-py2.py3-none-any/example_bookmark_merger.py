# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/example_bookmark_merger.py
# Compiled at: 2015-06-28 04:04:47
from six import print_
import bookmark_pyparser as bpp, os
from optparse import OptionParser
usage = 'usage: %prog [options] dir_path1 dir_path2\n\nAll html files in the given directories will be assumed to be firefox \nbookmark.html files.\nIf no directory is given then the current directory will be used'
parser = OptionParser(usage=usage)
parser.add_option('-r', '--recursive', action='store_true', dest='recursive', default=False, help='Recursively explore given directory for bookmark files')
parser.add_option('-o', '--outfile', dest='outfile', default='merged bookmarks.html', help='write output to FILE [default: %default]', metavar='FILE')
options, args = parser.parse_args()
outfile = options.outfile
recursive = options.recursive
if args == []:
    dir_path = '.'
else:
    dir_path = args
htmlfiles = []
for path in dir_path:
    if recursive == True:
        for root, dirs, files in os.walk(path):
            print_(root)
            htmlfiles_tmp = [ os.path.join(root, fils) for fils in files if fils.split('.')[(-1)].lower() == 'html' ]
            htmlfiles.extend(htmlfiles_tmp)

    else:
        root = os.path.abspath(path)
        files = os.listdir(path)
        print_(root)
        htmlfiles_tmp = [ os.path.join(root, fils) for fils in files if fils.split('.')[(-1)].lower() == 'html' ]
        htmlfiles.extend(htmlfiles_tmp)

print_()
result = {}
numhref = 0
for bookmarkfile in htmlfiles:
    print_('##### parsing ', os.path.relpath(bookmarkfile, path))
    parsedfile = bpp.bookmarkshtml.parseFile(open(bookmarkfile))
    numhref += len(bpp.hyperlinks(parsedfile))
    print_('#### creating a bookmarkDict ')
    bmDict = bpp.bookmarkDict(parsedfile)
    print_('#### merging latest file into result')
    result = bpp.merge_bookmarkDict(result, bmDict)

finalfile = open(outfile, 'w')
finalstr = bpp.serialize_bookmarkDict(result)
finalfile.write(finalstr)
finalfile.close()
print_('total nunber of hyperlinks found = ', numhref)
print_('number of hyperlinks in final file=', len(bpp.hyperlinks_bookmarkDict(result)))
print_('number of unique hyperlinks =', len(set(bpp.hyperlinks_bookmarkDict(result))))
print_('number of folders =', bpp.count_folders(result))