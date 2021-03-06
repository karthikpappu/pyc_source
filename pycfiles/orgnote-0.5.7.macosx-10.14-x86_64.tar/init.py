# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/LeslieZhu/.pyenv/versions/2.7.15/Python.framework/Versions/2.7/lib/python2.7/site-packages/orgnote/init.py
# Compiled at: 2019-11-27 20:06:24
"""
OrgNote  ---- A simple org-mode blog, write blog by org-mode in Emacs

author: Leslie Zhu
email: pythonisland@gmail.com

Write note by Emacs with org-mode, and convert .org file into .html file,
then use orgnote convert into new html with default theme.
"""
from __future__ import print_function
from __future__ import absolute_import

def create_emacs_init(initfile='init-orgnote.el'):
    """
    init ./scripts/init-orgnote.el
    """
    import os, os.path
    _dirname = './scripts/'
    _init_file = _dirname + initfile
    _data = ';; 设置org-mode输出中文目录\n(custom-set-variables\n \'(org-blank-before-new-entry\n      (quote ((heading) (plain-list-item))))\n\n \'(org-export-language-setup\n      (quote\n               (("en" "Author" "Date" "Table of Contents" "Footnotes") ("zh-CN" "作者" "日期" "目录" "脚注")))))\n '
    if not os.path.exists(_dirname):
        os.mkdir(_dirname)
    if not os.path.exists(_init_file):
        print('[info] create ', _init_file)
        output = open(_init_file, 'w')
        print(_data, file=output)
        output.close()


def create_about_html(name='about.hmtl'):
    import os, os.path, time, orgnote.parser
    blog = orgnote.parser.OrgNote()
    _data = '\n    <html>\n    <head>\n    <meta name="keywords" content="关于" />\n    </head>\n    <body>\n    <div id="content">\n    <h1 class="title"></h1>\n    <p>\n    此博客 <code>OrgNote</code> 基于<a href="https://github.com/LeslieZhu/OrgNote">OrgNote</a>生成。\n    </p>\n    </div>\n    </body>\n    </html>\n    '
    _dirname = blog.source_dir
    _init_file = _dirname + os.path.basename(name)
    if not os.path.exists(_dirname):
        os.makedirs(_dirname)
    if not os.path.exists(_init_file):
        print('[info] create ', _init_file)
        output = open(_init_file, 'w')
        print(_data, file=output)
        output.close()
        return _init_file
    else:
        print('File %s already exists, please use a new name!' % _init_file)
        return
        return


def create_note_file(name='links.org', text=[]):
    import os, orgnote.parser
    blog = orgnote.parser.OrgNote()
    _dirname = blog.source_dir
    _init_file = _dirname + os.path.basename(name)
    if not os.path.exists(_dirname):
        os.makedirs(_dirname)
    if not os.path.exists(_init_file):
        print('[info] create ', _init_file)
        output = open(_init_file, 'w')
        for i in text:
            print(i, file=output)

        output.close()
        return _init_file
    else:
        print('File %s already exists, please use a new name!' % _init_file)
        return
        return


def create_about_note(name='about.org'):
    import os, os.path, time, orgnote.parser
    blog = orgnote.parser.OrgNote()
    _data = '#+STARTUP: overview\n#+STARTUP: content\n#+STARTUP: showall\n#+STARTUP: showeverything\n#+STARTUP: indent\n#+STARTUP: nohideblocks\n#+OPTIONS: ^:{}\n#+OPTIONS: LaTeX:t\n#+OPTIONS: LaTeX:dvipng\n#+OPTIONS: LaTeX:nil\n#+OPTIONS: LaTeX:verbatim\n        \n#+OPTIONS: H:3\n#+OPTIONS: toc:t\n#+OPTIONS: num:t\n#+LANGUAGE: %s\n        \n#+KEYWORDS: 关于\n#+TITLE: 关于此博客\n#+AUTHOR: %s\n#+EMAIL: %s\n#+DATE: %s\n\n此博客 =%s= 基于[[https://github.com/LeslieZhu/OrgNote][OrgNote]]生成。\n' % (blog.language, blog.author, blog.email, time.strftime('%Y/%m/%d', time.localtime()), blog.title)
    _dirname = blog.source_dir
    _init_file = _dirname + os.path.basename(name)
    if not os.path.exists(_dirname):
        os.makedirs(_dirname)
    if not os.path.exists(_init_file):
        print('[info] create ', _init_file)
        output = open(_init_file, 'w')
        print(_data, file=output)
        output.close()
        return _init_file
    else:
        print('File %s already exists, please use a new name!' % _init_file)
        return
        return


def create_default_note(name='HelloOrgNote.org'):
    """
    init source_dir/template.org
    """
    import os, os.path, time, orgnote.parser
    blog = orgnote.parser.OrgNote()
    _data = '#+STARTUP: overview\n#+STARTUP: content\n#+STARTUP: showall\n#+STARTUP: showeverything\n#+STARTUP: indent\n#+STARTUP: nohideblocks\n#+OPTIONS: ^:{}\n#+OPTIONS: LaTeX:t\n#+OPTIONS: LaTeX:dvipng\n#+OPTIONS: LaTeX:nil\n#+OPTIONS: LaTeX:verbatim\n        \n#+OPTIONS: H:3\n#+OPTIONS: toc:t\n#+OPTIONS: num:t\n#+LANGUAGE: %s\n        \n#+KEYWORDS: %s\n#+TITLE: %s\n#+AUTHOR: %s\n#+EMAIL: %s\n#+DATE: %s\n\n* Hello OrgNote\n\n[[https://github.com/LeslieZhu/OrgNote][OrgNote]] is a simple blog based on org-mode, enjoy it:)\n' % (blog.language, blog.default_tag, os.path.basename(name).strip('.org'), blog.author, blog.email, time.strftime('%Y/%m/%d', time.localtime()))
    _dirname = blog.source_dir + time.strftime('%Y/%m/%d', time.localtime())
    _init_file = _dirname + '/' + os.path.basename(name)
    if not os.path.exists(_dirname):
        os.makedirs(_dirname)
    if not os.path.exists(_init_file):
        print('[info] create ', _init_file)
        output = open(_init_file, 'w')
        print(_data, file=output)
        output.close()
        return _init_file
    else:
        print('File %s already exists, please use a new name!' % _init_file)
        return
        return


def create_config_file(name='_config.yml'):
    """
    init _config.yml config file
    """
    import os, os.path
    _dir = './'
    _init_file = _dir + name
    if not os.path.exists(_init_file):
        print('[info] create ', _init_file)
        import orgnote.config
        orgnote.config.Config().default()


def create_public_file(name='public.org'):
    """
    init ./source_dir/public.org
    """
    import os, os.path, orgnote.parser
    blog = orgnote.parser.OrgNote()
    _dir = blog.source_dir
    _init_file = _dir + name
    if name == 'public.org':
        _data = ''
    else:
        _data = ''
    if not os.path.exists(_dir):
        os.mkdir(_dir)
    if not os.path.exists(_init_file):
        print('[info] create ', _init_file)
        output = open(_init_file, 'w')
        print(_data, file=output)
        output.close()


def main(args=None):
    import os, os.path, orgnote.parser
    blog = orgnote.parser.OrgNote()
    create_config_file('_config.yml')
    source_dir = blog.source_dir
    public_dir = blog.public_dir
    tags_dir = public_dir + '/tags/'
    target_list = [
     './theme/', public_dir, tags_dir, source_dir]
    for target in target_list:
        if not os.path.exists(target):
            print('[info] create ', target)
            os.mkdir(target)

    create_public_file('public.org')
    create_public_file('nopublic.org')
    create_about_note(blog.source_dir + '/about.org')
    create_about_html(blog.source_dir + '/about.html')
    link = [
     'https://github.com/LeslieZhu/OrgNote, OrgNote:为自己定制的基于org-mode博客工具, fa fa-github']
    create_note_file(blog.source_dir + '/links.org', link)
    create_note_file(blog.source_dir + '/slinks.org', link)
    job_once = 'by_once,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote'
    job_day = 'by_day,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote'
    job_week = 'by_week,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote'
    job_month = 'by_month,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote'
    job_quarter = 'by_quarter,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote'
    job_year = 'by_year,2019/11/11 10:00,查看OrgNote更新,https://github.com/LeslieZhu/OrgNote'
    create_note_file(blog.source_dir + '/calendar.org', [job_once, job_day, job_week, job_month, job_quarter, job_year])
    if not os.path.exists('theme/freemind'):
        cmd = 'git clone git@github.com:LeslieZhu/orgnote-theme-freemind.git theme/freemind'
        os.system(cmd)
        cmd = 'rm -rf theme/freemind/.git'
        os.system(cmd)
    if not os.path.exists('scripts'):
        cmd = 'git clone git@github.com:LeslieZhu/orgnote-emacs-el.git scripts/'
        os.system(cmd)
        cmd = 'rm -rf scripts/.git'
        os.system(cmd)


if __name__ == '__main__':
    import sys
    sys.exit(main())