# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/pyami/config.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 8016 bytes
import os, re, warnings, boto
from boto.compat import expanduser, ConfigParser, StringIO
BotoConfigPath = '/etc/boto.cfg'
BotoConfigLocations = [BotoConfigPath]
UserConfigPath = os.path.join(expanduser('~'), '.boto')
BotoConfigLocations.append(UserConfigPath)
if 'BOTO_CONFIG' in os.environ:
    BotoConfigLocations = [
     expanduser(os.environ['BOTO_CONFIG'])]
elif 'BOTO_PATH' in os.environ:
    BotoConfigLocations = []
    for path in os.environ['BOTO_PATH'].split(os.pathsep):
        BotoConfigLocations.append(expanduser(path))

class Config(ConfigParser):

    def __init__(self, path=None, fp=None, do_load=True):
        ConfigParser.__init__(self, {'working_dir': '/mnt/pyami',  'debug': '0'})
        if do_load:
            if path:
                self.load_from_path(path)
            else:
                if fp:
                    self.readfp(fp)
                else:
                    self.read(BotoConfigLocations)
            if 'AWS_CREDENTIAL_FILE' in os.environ:
                full_path = expanduser(os.environ['AWS_CREDENTIAL_FILE'])
                try:
                    self.load_credential_file(full_path)
                except IOError:
                    warnings.warn('Unable to load AWS_CREDENTIAL_FILE (%s)' % full_path)

    def load_credential_file(self, path):
        """Load a credential file as is setup like the Java utilities"""
        c_data = StringIO()
        c_data.write('[Credentials]\n')
        for line in open(path, 'r').readlines():
            c_data.write(line.replace('AWSAccessKeyId', 'aws_access_key_id').replace('AWSSecretKey', 'aws_secret_access_key'))

        c_data.seek(0)
        self.readfp(c_data)

    def load_from_path(self, path):
        file = open(path)
        for line in file.readlines():
            match = re.match('^#import[\\s\t]*([^\\s^\t]*)[\\s\t]*$', line)
            if match:
                extended_file = match.group(1)
                dir, file = os.path.split(path)
                self.load_from_path(os.path.join(dir, extended_file))
                continue

        self.read(path)

    def save_option(self, path, section, option, value):
        """
        Write the specified Section.Option to the config file specified by path.
        Replace any previous value.  If the path doesn't exist, create it.
        Also add the option the the in-memory config.
        """
        config = ConfigParser()
        config.read(path)
        if not config.has_section(section):
            config.add_section(section)
        config.set(section, option, value)
        fp = open(path, 'w')
        config.write(fp)
        fp.close()
        if not self.has_section(section):
            self.add_section(section)
        self.set(section, option, value)

    def save_user_option(self, section, option, value):
        self.save_option(UserConfigPath, section, option, value)

    def save_system_option(self, section, option, value):
        self.save_option(BotoConfigPath, section, option, value)

    def get_instance(self, name, default=None):
        try:
            val = self.get('Instance', name)
        except:
            val = default

        return val

    def get_user(self, name, default=None):
        try:
            val = self.get('User', name)
        except:
            val = default

        return val

    def getint_user(self, name, default=0):
        try:
            val = self.getint('User', name)
        except:
            val = default

        return val

    def get_value(self, section, name, default=None):
        return self.get(section, name, default)

    def get(self, section, name, default=None):
        try:
            val = ConfigParser.get(self, section, name)
        except:
            val = default

        return val

    def getint(self, section, name, default=0):
        try:
            val = ConfigParser.getint(self, section, name)
        except:
            val = int(default)

        return val

    def getfloat(self, section, name, default=0.0):
        try:
            val = ConfigParser.getfloat(self, section, name)
        except:
            val = float(default)

        return val

    def getbool(self, section, name, default=False):
        if self.has_option(section, name):
            val = self.get(section, name)
            if val.lower() == 'true':
                val = True
            else:
                val = False
        else:
            val = default
        return val

    def setbool(self, section, name, value):
        if value:
            self.set(section, name, 'true')
        else:
            self.set(section, name, 'false')

    def dump(self):
        s = StringIO()
        self.write(s)
        print(s.getvalue())

    def dump_safe(self, fp=None):
        if not fp:
            fp = StringIO()
        for section in self.sections():
            fp.write('[%s]\n' % section)
            for option in self.options(section):
                if option == 'aws_secret_access_key':
                    fp.write('%s = xxxxxxxxxxxxxxxxxx\n' % option)
                else:
                    fp.write('%s = %s\n' % (option, self.get(section, option)))

    def dump_to_sdb(self, domain_name, item_name):
        from boto.compat import json
        sdb = boto.connect_sdb()
        domain = sdb.lookup(domain_name)
        if not domain:
            domain = sdb.create_domain(domain_name)
        item = domain.new_item(item_name)
        item.active = False
        for section in self.sections():
            d = {}
            for option in self.options(section):
                d[option] = self.get(section, option)

            item[section] = json.dumps(d)

        item.save()

    def load_from_sdb(self, domain_name, item_name):
        from boto.compat import json
        sdb = boto.connect_sdb()
        domain = sdb.lookup(domain_name)
        item = domain.get_item(item_name)
        for section in item.keys():
            if not self.has_section(section):
                self.add_section(section)
            d = json.loads(item[section])
            for attr_name in d.keys():
                attr_value = d[attr_name]
                if attr_value is None:
                    attr_value = 'None'
                if isinstance(attr_value, bool):
                    self.setbool(section, attr_name, attr_value)
                else:
                    self.set(section, attr_name, attr_value)