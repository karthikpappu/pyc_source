# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/utils.py
# Compiled at: 2014-01-15 13:01:31
# Size of source mod 2**32: 3844 bytes
import subprocess, os, os.path, yaml, shlex, re, urllib.parse, shutil, urllib.request

def exe(cmd):
    if type(cmd) != type([]):
        cmd = shlex.split(cmd)
    return subprocess.Popen(cmd)


def exe_pipes(cmd):
    if type(cmd) != type([]):
        cmd = shlex.split(cmd)
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def exe_flos(cmd, fout, ferr):
    if type(cmd) != type([]):
        cmd = shlex.split(cmd)
    out = open(fout, 'w')
    err = open(ferr, 'w')
    return (
     subprocess.Popen(cmd, stdout=out, stderr=err), out, err)


def dw_file_to(url, path, callback):
    """Saves file from url to path
        """
    urllib.request.urlretrieve(url, path, callback)


def set_dir(directory, create=True):
    if os.path.isdir(directory):
        return directory
    if create:
        os.makedirs(directory)
        return directory
    raise Exception('Tried to assign invalid directory: "%s"' % directory)


def set_file(f, create=True):
    if os.path.isfile(f):
        return f
    if create:
        open(f, 'wb').close()
        return f
    Exception('Tried to assign invalid file: "%s"' % f)


def write_to_file(path, content):
    fd = open(path, 'w')
    fd.write(content)
    fd.close()


def get_url_info(url):
    """Retrieves information about given url
        """
    settings = load_config()
    try:
        download_link_getter = exe_pipes('plowdown --9kweu ' + settings['captcha-api-key'] + ' -v1 --skip-final --printf "%%f%%n%%d" %s' % url)
        stdout, stderr = download_link_getter.communicate()
        res_list = stdout.decode('utf8').split('\n')
        res_err = stderr.decode('utf8')
        retc = download_link_getter.returncode
    except:
        res_list = []
        retc = 2
        res_err = ''

    return (
     url, res_list, res_err, retc)


def parse_url_info(url, res_list, res_err, retc):
    """Parses information about given url, returns false on error
        """
    if len(res_list) != 3:
        if retc == 2 or retc == 0:
            fname = url_to_filename(url)
            if len(fname) != 0:
                return (
                 fname, url)
        print('Error while getting link info: ' + repr(res_err) + ' (' + str(retc) + ')')
        return False
    else:
        return (
         res_list[0], res_list[1])


def load_file(url, path, callback):
    """Downloads url to file.
                Returns true on success, otherwise false
        """
    print("Saving '%s' to '%s'" % (url, path))
    try:
        dw_file_to(url, path, callback)
        return True
    except Exception as e:
        print('Error while downloading: ' + str(e))
        return False


def set_config_path(path):
    global config_path
    config_path = path


def load_config():
    if os.path.isfile(config_path):
        return yaml.load(open(config_path, 'r'))
    print('No config file present, creating default one (path: %s)' % config_path)
    create_default_config(config_path)
    try:
        return yaml.load(open(config_path, 'r'))
    except:
        raise Exception('[FATAL] - Could not create config (path: %s)' % config_path)


def create_default_config(path='./config.yaml'):
    basic_conf = 'download-dir: downloads\ncaptcha-api-key: xyz\nport: 50505'
    with open(path, 'w') as (fd):
        fd.write(basic_conf)


def clean_links(raw_data):
    return re.findall('(?:ftp|https|http)?://(?:[a-zA-Z]|[0-9]|[$-_@.&+~]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', raw_data)


def url_to_filename(url):
    res = urllib.parse.urlparse(url)
    return os.path.basename(res.path)


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if num < 1024.0:
            return '%3.1f%s' % (num, x)
        num /= 1024.0

    return '%3.1f%s' % (num, 'TB')