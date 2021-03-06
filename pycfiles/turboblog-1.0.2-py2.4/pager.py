# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/turboblog/pager.py
# Compiled at: 2007-04-02 19:58:14
"""
This is the pager decorator that slices results into
smaller parts and provides links to next/previous entries
"""
from math import ceil
from turboblog import model

def pager(sliceable, default_size=10, default_from=0):

    def decorator(fn, sliceable=sliceable, default_from=default_from, default_size=default_size):

        def wrapper(self, *args, **kw):

            def var(name):
                return 'tg_pager_' + sliceable + '_' + name

            if kw.has_key('bid'):
                blog = model.Blog.get(kw['bid'])
            else:
                blog = model.Blog.bySlug(args[0])
            pfrom = int(kw.pop(var('from'), default_from))
            read_settings = blog.get_read_settings()
            psize = read_settings.postsperpage
            d = fn(self, *args, **kw)
            try:
                ptotal = len(d[sliceable])
            except:
                ptotal = d[sliceable].count()

            if not psize:
                psize = ptotal - pfrom
                d[sliceable] = list(d[sliceable][pfrom:pfrom + psize])
            d[sliceable] = d[sliceable][pfrom:pfrom + psize]
            d[var('from')] = pfrom
            d[var('size')] = psize
            d[var('total')] = ptotal
            d[var('pages')] = int(ceil(float(ptotal) / psize))
            return d

        return wrapper

    return decorator


def add_params(k):
    if 'arc_year' in k and 'arc_month' in k:
        return ';arc_year=%d;arc_month=%d' % (k['arc_year'], k['arc_month'])
    if 'tag_name' in k:
        return ';tagged=%d' % k['tag_name'].id
    if 'untagged' in k:
        return ';untagged=%d' % k['untagged']
    return ''


def next_link(k):
    nl = ''
    if k['tg_pager_blog_posts_total'] > k['tg_pager_blog_posts_from'] + k['tg_pager_blog_posts_size']:
        nl = '<a href="%s?tg_pager_blog_posts_from=%d%s">Next Entries &raquo;</a>' % (k['blog'].link(), k['tg_pager_blog_posts_from'] + k['tg_pager_blog_posts_size'], add_params(k))
    return nl


def previous_link(k):
    pl = ''
    if k['tg_pager_blog_posts_from'] > k['tg_pager_blog_posts_pages']:
        pl = '<a href="%s?tg_pager_blog_posts_from=%d%s">&laquo; Previous Entries</a>' % (k['blog'].link(), k['tg_pager_blog_posts_from'] - k['tg_pager_blog_posts_size'], add_params(k))
    return pl