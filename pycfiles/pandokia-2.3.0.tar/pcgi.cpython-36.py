# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jhunk/Downloads/pandokia/pandokia/pcgi.py
# Compiled at: 2018-06-04 12:38:26
# Size of source mod 2**32: 6426 bytes
import cgi, os, os.path, sys, cgitb, pandokia, pandokia.common as common
cfg = pandokia.cfg

def form_to_dict(f):
    d = {}
    for x in f:
        l = f.getlist(x)
        if len(l) > 0:
            d[x] = l

    return d


def run():
    global cginame
    global form
    global output_format
    if cfg.debug:
        cgitb.enable()
    else:
        if cfg.server_maintenance:
            sys.stdout.write('content-type: text/html\n\n\nWeb page unavailable because of pandokia server maintenance<p>\n\n')
            if isinstance(cfg.server_maintenance, str):
                sys.stdout.write('%s\n' % cfg.server_maintenance)
            sys.exit(0)
        else:
            if not common.check_auth():
                sys.stdout.write('content-type: text/html\n\n\nAUTHENTICATION FAILED\n\n')
                sys.exit(0)
            else:
                cginame = os.getenv('SCRIPT_NAME')
                form = cgi.FieldStorage(keep_blank_values=1)
                if 'format' in form:
                    output_format = form.getvalue('format')
                else:
                    output_format = 'html'
                if 'query' not in form:
                    import re
                    sys.stdout.write('Content-type: text/html\n\n')
                    f = os.path.dirname(os.path.abspath(__file__)) + '/top_level.html'
                    header = common.page_header()
                    f = open(f, 'r')
                    x = f.read()
                    f.close()
                    if common.current_user() in common.cfg.admin_user_list:
                        x = re.sub('ADMINLINK', '<br> <a href=CGINAME?query=admin>Admin</a> <br>', x)
                    else:
                        x = re.sub('ADMINLINK', '', x)
                    x = re.sub('CGINAME', cginame, x)
                    x = re.sub('PAGEHEADER', header, x)
                    sys.stdout.write(x)
                    sys.exit(0)
                query = form.getvalue('query')
                if query == 'treewalk':
                    import pandokia.pcgi_treewalk as x
                    x.treewalk()
                    sys.exit(0)
                if query == 'qid_op':
                    import pandokia.pcgi_qid_op as x
                    x.run()
                    sys.exit(0)
                if query == 'qid_list':
                    import pandokia.pcgi_qid_op as x
                    x.qid_list()
                    sys.exit(0)
                if query == 'treewalk.linkout':
                    import pandokia.pcgi_treewalk as x
                    x.linkout()
                    sys.exit(0)
                if query == 'summary':
                    import pandokia.pcgi_summary as x
                    x.run()
                    sys.exit(0)
                if query == 'detail':
                    import pandokia.pcgi_detail as x
                    x.run()
                    sys.exit(0)
                if query == 'test_history':
                    import pandokia.pcgi_detail as x
                    x.test_history()
                    sys.exit(0)
                if query.startswith('day_report.'):
                    import pandokia.pcgi_day_report as x
                    if query == 'day_report.1':
                        x.rpt1()
                    if query == 'day_report.2':
                        x.rpt2()
                    if query == 'day_report.3':
                        x.rpt3()
                    sys.exit(0)
                if query.startswith('delete_run.'):
                    import pandokia.pcgi_delete as x
                    if query == 'delete_run.ays':
                        x.delete_are_you_sure()
                    if query == 'delete_run.conf':
                        x.delete_confirmed()
                    sys.exit(0)
                if query == 'flagok':
                    import pandokia.pcgi_flagok as x
                    x.flagok()
                    sys.exit(0)
                if query == 'action':
                    import pandokia.pcgi_action as x
                    x.run()
                    sys.exit(0)
                if query == 'prefs':
                    import pandokia.pcgi_preferences as x
                    x.run()
                    sys.exit(0)
                if query == 'killproc':
                    print('content-type: text/html')
                    print('')
                    pid = form.getvalue('pid')
                    sig = form.getvalue('sig')
                    if common.current_user() in common.cfg.admin_user_list:
                        os.kill(int(pid), int(sig))
                    print('done')
                    sys.exit(0)
                if query == 'hostinfo':
                    import pandokia.pcgi_misc as x
                    x.hostinfo()
                    sys.exit(0)
                if query == 'set_hostinfo':
                    import pandokia.pcgi_misc as x
                    x.set_hostinfo()
                    sys.exit(0)
                if query == 'magic_html_log':
                    import pandokia.pcgi_detail as x
                    x.magic_html_log()
                    sys.exit(0)
                if query == 'expected':
                    import pandokia.pcgi_misc as x
                    x.expected()
                    sys.exit(0)
                if query == 'new':
                    import pandokia.pcgi_reports as x
                    x.cluster_report()
                    sys.exit(0)
            if query == 'latest':
                import pandokia.pcgi_misc as x
                x.latest()
                sys.exit(0)
        error_1201()
        if cfg.debug or common.current_user() in common.cfg.admin_user_list:
            print('YOU ARE ADMIN, DEBUG FOLLOWS')
            for x in form:
                if isinstance(form[x], list):
                    for y in form[x]:
                        print('%s %s<br>' % (x, y))

                else:
                    print('%s %s<br>' % (x, form.getvalue(x)))


def error_1201():
    sys.stdout.write('content-type: text/html\n\n\n<font color=red><blink>1201</blink></font>\n')