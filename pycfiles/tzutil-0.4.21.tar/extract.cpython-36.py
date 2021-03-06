# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n8f5s77x/tzutil/tzutil/extract.py
# Compiled at: 2018-12-04 01:36:04
# Size of source mod 2**32: 2437 bytes


def extract_table(begin, html):
    li = []
    table = extract(begin, '</table>', html)
    if table:
        for i in table.split('</tr>'):
            td = extract_li('<td', '</td>', i)
            if td:
                td = [x.split('>', 1)[1] for x in td]
                li.append(td)

    return li


def extract(begin, end, html):
    if not html:
        return ''
    else:
        if begin is None:
            start = 0
        else:
            start = html.find(begin)
            if start >= 0:
                start += len(begin)
            else:
                return
        if end is not None:
            end = html.find(end, start)
        if end is None or end >= 0:
            return html[start:end].strip()


def extract_li(begin, end, html):
    return list(map(str.strip, _extract_li(begin, end, html)))


def _extract_li(begin, end, html):
    if not html:
        return ''
    else:
        html = str(html)
        result = []
        from_pos = 0
        while True:
            start = html.find(begin, from_pos)
            if start >= 0:
                start += len(begin)
                endpos = html.find(end, start)
                if endpos >= 0:
                    result.append(html[start:endpos])
                    from_pos = endpos + len(end)
                    continue
            break

        return result


def line_strip(txt):
    if not txt:
        return ''
    else:
        txt = txt.replace('\u3000', ' ').split('\n')
        return '\n'.join(i for i in [i.strip() for i in txt] if i)


def extract_strip(begin, end, html):
    if not html:
        return ''
    t = extract(begin, end, html)
    if t:
        return strip_line(t)


def extract_map(begin, end, html, func):
    txt = []
    result = []
    prepos = None
    preend = 0
    len_end = len(end)
    len_begin = len(begin)
    while True:
        if prepos is None:
            pos = html.find(begin)
        else:
            pos = html.find(begin, prepos)
        if pos >= 0:
            endpos = html.find(end, pos)
        if pos < 0 or end < 0:
            result.append(html[preend:])
            break
        endpos = endpos + len_end
        result.append(html[preend:pos])
        tmp = func(html[pos:endpos])
        if tmp:
            result.append(tmp)
        prepos = pos + len_begin
        preend = endpos

    return ''.join(result)


if __name__ == '__main__':
    import _env
    from model.po.blog import Po
    from z42.lib.base.txt2html import txt_withlink
    txt = Po.mc_get(10501881)
    txt_withlink(txt.txt)