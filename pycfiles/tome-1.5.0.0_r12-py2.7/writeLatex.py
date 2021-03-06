# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\tome\writeLatex.py
# Compiled at: 2013-05-16 20:29:48
"""
Copyright 2013 Brian Mearns

This file is part of Tome.

Tome is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Tome is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with Tome.  If not, see <http://www.gnu.org/licenses/>.
"""
import Tome, templ.templ, templ.texec, templ.ttypes, templ.tstreams, cStringIO, pkg_resources, wrapUtil

def latexEscape(text):
    return text.replace('\\', '\\\\').replace('_', '\\_').replace('{', '\\{').replace('}', '\\}')


def latexEscapeVerbatim(text):
    return text.replace('\\', '\\\\')


def writeBlockSegment(ostream, begin, end, segment, dropCap=False, verbatim=False, prefix='', suffix=''):
    ostream.write(begin)
    notFirst = False
    for par in segment:
        if isinstance(par, Tome.TextSegment) and len(par.text().strip()) == 0:
            continue
        if not isinstance(par, Tome.TaggedSegment) or par.tag() != 'p':
            raise Exception('Block node may only contain "p" elements: found "%s"' % par.tag())
        if notFirst:
            ostream.write('\n\n' + prefix)
        notFirst = True
        for cseg in par:
            writeSegment(ostream, cseg, dropCap, verbatim)
            dropCap = False

        ostream.write(suffix)

    ostream.write(end)


def writeSegment(ostream, segment, dropCap=False, verbatim=False):
    if isinstance(segment, Tome.TaggedSegment):
        tag = segment.tag()
        if tag == 'pre':
            ostream.write('\\begin{samepage}\n\\begin{verbatim}\n')
            close = '\\end{verbatim}\n\\end{samepage}\n'
            verbatim = True
        else:
            if tag == 'b':
                ostream.write('\\textbf{')
                close = '}'
            elif tag == 'i':
                ostream.write('\\textit{')
                close = '}'
            elif tag == 'em':
                ostream.write('{\\em ')
                close = '}'
            elif tag == 'u':
                ostream.write('\\underline{')
                close = '}'
            elif tag == 'grave':
                ostream.write('\\`{')
                close = '}'
            elif tag == 'acute':
                ostream.write("\\'{")
                close = '}'
            elif tag == 'circumflex':
                ostream.write('\\^{')
                close = '}'
            elif tag == 'umlaut':
                ostream.write('\\"{')
                close = '}'
            elif tag == 'tilde':
                ostream.write('\\~{')
                close = '}'
            elif tag == 'cedilla':
                ostream.write('\\c{')
                close = '}'
            else:
                if tag == 'ellips':
                    ostream.write('{\\ldots}')
                    return
                if tag == 'md':
                    ostream.write('---')
                    return
                if tag == 'nd':
                    ostream.write('--')
                    return
                if tag == 'sp':
                    ostream.write(' ')
                    return
                if tag == 'lnbrk':
                    ostream.write('\n')
                    return
                if tag == 'q':
                    return writeBlockSegment(ostream, '``', "''", segment, dropCap, verbatim=verbatim, prefix='``')
                if tag == 'sq':
                    return writeBlockSegment(ostream, '`', "'", segment, dropCap, verbatim=verbatim, prefix='`')
                if tag == 'n':
                    return writeBlockSegment(ostream, '\\footnote{', '}', segment, dropCap, verbatim=verbatim)
                if tag == 'bq':
                    return writeBlockSegment(ostream, '\\begin{quote}\n', '\n\\end{quote}\n', segment, dropCap, verbatim=verbatim)
                raise Exception('Unhandled tag: %s' % tag)
            for seg in segment:
                writeSegment(ostream, seg, dropCap, verbatim)
                dropCap = False

        ostream.write(close)
    elif isinstance(segment, Tome.TextSegment):
        content = segment.text()
        if verbatim:
            escape = lambda text: latexEscapeVerbatim(text)
        else:
            escape = lambda text: latexEscape(text)
        if dropCap and len(content) > 0:
            content = '\\dropcap{%s}%s' % (escape(content[0]), escape(content[1:]))
        else:
            content = escape(content)
        if not isinstance(content, unicode):
            content = unicode(content, 'utf-8')
        ostream.write(content.encode('utf-8'))
    else:
        raise TypeError('Unexpected type for segment.')


def writeLatex(tome, ostream, templateFile=None, draft=False, linewrap=None):
    if templateFile is None:
        templateFile = pkg_resources.resource_filename('tome', 'res/template.latex.tmpl')
    globs = templ.texec.getGlobalScope()
    templStack = templ.stack.Stack(globs)
    topScope = templStack.push()
    if draft:
        draft = ',draft'
    else:
        draft = ''
    topScope['DRAFT-PARAM'] = templ.ttypes.String(draft)
    titlesLatex = ''
    lmTitles = tome.allTitles()
    if len(lmTitles) > 0:
        titlesLatex += '\\title{%s}\n' % latexEscape(lmTitles[0])
        for lmSubtitle in lmTitles[1:]:
            titlesLatex += '\\subtitle{%s}\n' % latexEscape(lmSubtitle)

    topScope['TITLES-LATEX'] = templ.ttypes.String(titlesLatex)
    topScope['AUTHORS-LATEX'] = templ.ttypes.String(('\n').join('\\author{%s}' % latexEscape(author) for author in tome.authors()))
    buf = cStringIO.StringIO()
    for part in tome:
        for book in part:
            for chapter in book:
                chAllTitles = chapter.allTitles()
                if len(chAllTitles) > 0:
                    chLatTitle = latexEscape(chAllTitles[0])
                else:
                    chLatTitle = ''
                chLatSubtitles = ('\n').join('\t\\chSubtitle{%s}' % latexEscape(subtitle) for subtitle in chAllTitles[1:])
                buf.write('\n\n\n\\chapter[%s]{%s\n%s}\n' % (chLatTitle, chLatTitle, chLatSubtitles))
                chMark = chapter.shortMark()
                if chMark is not None:
                    buf.write('\\chaptermark{%s}\n' % chMark)
                buf.write('\n')
                scCount = len(chapter)
                lastScene = scCount - 1
                for i in xrange(scCount):
                    scene = chapter[i]
                    parCount = len(scene)
                    for j in xrange(parCount):
                        paragraph = scene[j]
                        parPreformatted = paragraph.tag() == 'pre'
                        if parPreformatted:
                            buf.write('\\begin{samepage}\n\\begin{verbatim}\n')
                        parBuf = cStringIO.StringIO()
                        for k in xrange(len(paragraph)):
                            writeSegment(parBuf, paragraph[k], i == 0 and j == 0 and k == 0 and not parPreformatted, verbatim=parPreformatted)

                        par = parBuf.getvalue()
                        parBuf.close()
                        if linewrap is not None and not parPreformatted:
                            lines = wrapUtil.wrapText(par, linewrap)
                            buf.write(('\n').join((' ').join(line) for line in lines))
                        else:
                            buf.write(par)
                        if parPreformatted:
                            buf.write('\\end{verbatim}\n\\end{samepage}\n')
                        buf.write('\n\n')

                    if i < lastScene:
                        buf.write('\n\\stars\n\n')

    topScope['CONTENT-LATEX'] = templ.ttypes.String(buf.getvalue())
    buf.close()
    istream = open(templateFile, 'r')
    tostream = templ.tstreams.TemplateStreamOutputStream(ostream)
    templ.templ.processWithStack(istream, tostream, templStack, templateFile, debug=False)
    istream.close()
    ostream.close()
    return


if __name__ == '__main__':
    import sys
    parser = Tome.TomeOtlParser(sys.stdin, filename='<stdin>', debug=True)
    tome = parser.tome()
    writeLatex(tome, sys.stdout, templateFile='res/template.latex.tmpl')