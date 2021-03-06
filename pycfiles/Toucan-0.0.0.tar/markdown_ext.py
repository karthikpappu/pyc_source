# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/web-portfolio/webmaster/markdown_ext.py
# Compiled at: 2016-01-01 03:35:42
"""
A utils for Markdown

html : render markdown to html
toc : Get the Table of Content
extract_images: Return a list of images, can be used to extract the top image

"""
import markdown
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension

class ExtractImagesExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        ext = ExtractImagesTreeprocessor(md)
        md.treeprocessors.add('imageextractor', ext, '_end')


class ExtractImagesTreeprocessor(Treeprocessor):

    def run(self, root):
        """Find all images and append to markdown.images. """
        self.markdown.images = []
        for image in root.getiterator('img'):
            self.markdown.images.append(image.attrib['src'])


class LazyImageExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        ext = LazyImageTreeprocessor(md)
        md.treeprocessors.add('lazyimage', ext, '_end')


class LazyImageTreeprocessor(Treeprocessor):

    def run(self, root):
        for image in root.getiterator('img'):
            image.set('data-src', image.attrib['src'])
            image.set('src', '')
            image.set('class', 'lazy')


class OEmbedExtension(Extension):

    def extendMarkdown(self, md, md_globals):
        ext = OEmbedTreeprocessor(md)
        md.treeprocessors.add('oembedextension', ext, '_end')


class OEmbedTreeprocessor(Treeprocessor):

    def run(self, root):
        for a in root.getiterator('a'):
            if a.text.strip() == '[embed]':
                a.text = ''
                a.set('class', 'WM-oembed')
                a.set('target', '_blank')


def html(text, lazy_images=False):
    """
    To render a markdown format text into HTML.

    - If you want to also build a Table of Content inside of the markdow,
    add the tags: [TOC]
    It will include a <ul><li>...</ul> of all <h*>

    :param text:
    :param lazy_images: bool - If true, it will activate the LazyImageExtension
    :return:
    """
    extensions = [
     'markdown.extensions.nl2br',
     'markdown.extensions.sane_lists',
     'markdown.extensions.toc',
     'markdown.extensions.tables',
     OEmbedExtension()]
    if lazy_images:
        extensions.append(LazyImageExtension())
    return markdown.markdown(text, extensions=extensions)


def toc(text):
    """
    Return a table of context list
    :param text:
    :return:
    """
    extensions = [
     'markdown.extensions.toc']
    mkd = markdown.Markdown(extensions=extensions)
    html = mkd.convert(text)
    return mkd.toc


def extract_images(text):
    """
    Extract all images in the content
    :param text:
    :return:
    """
    extensions = [
     ExtractImagesExtension()]
    mkd = markdown.Markdown(extensions=extensions)
    html = mkd.convert(text)
    return mkd.images