# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/lib/config/samconfig.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 5665 bytes
"""
Class representing the samconfig.toml
"""
import os, logging
from pathlib import Path
import tomlkit
from samcli.lib.config.version import SAM_CONFIG_VERSION, VERSION_KEY
from samcli.lib.config.exceptions import SamConfigVersionException
LOG = logging.getLogger(__name__)
DEFAULT_CONFIG_FILE_NAME = 'samconfig.toml'
DEFAULT_ENV = 'default'

class SamConfig:
    __doc__ = '\n    Class to interface with `samconfig.toml` file.\n    '
    document = None

    def __init__(self, config_dir, filename=None):
        """
        Initialize the class

        Parameters
        ----------
        config_dir : string
            Directory where the configuration file needs to be stored

        filename : string
            Optional. Name of the configuration file. It is recommended to stick with default so in the future we
            could automatically support auto-resolving multiple config files within same directory.
        """
        self.filepath = Path(config_dir, filename or DEFAULT_CONFIG_FILE_NAME)

    def get_all(self, cmd_names, section, env=DEFAULT_ENV):
        """
        Gets a value from the configuration file for the given environment, command and section

        Parameters
        ----------
        cmd_names : list(str)
            List of representing the entire command. Ex: ["local", "generate-event", "s3", "put"]

        section : str
            Specific section within the command to look into Ex: `parameters`

        env : str
            Optional, Name of the environment

        Returns
        -------
        dict
            Dictionary of configuration options in the file. None, if the config doesn't exist.

        Raises
        ------
        KeyError
            If the config file does *not* have the specific section

        tomlkit.exceptions.TOMLKitError
            If the configuration file is invalid
        """
        env = env or DEFAULT_ENV
        self._read()
        return self.document[env][self._to_key(cmd_names)][section]

    def put(self, cmd_names, section, key, value, env=DEFAULT_ENV):
        """
        Writes the `key=value` under the given section. You have to call the `flush()` method after `put()` in
        order to write the values back to the config file. Otherwise they will be just saved in-memory, available
        for future access, but never saved back to the file.

        Parameters
        ----------
        cmd_names : list(str)
            List of representing the entire command. Ex: ["local", "generate-event", "s3", "put"]

        section : str
            Specific section within the command to look into Ex: `parameters`

        key : str
            Key to write the data under

        value
            Value to write. Could be any of the supported TOML types.

        env : str
            Optional, Name of the environment

        Raises
        ------
        tomlkit.exceptions.TOMLKitError
            If the data is invalid
        """
        if not self.document:
            self._read()
            self.document.update({env: {self._to_key(cmd_names): {section: {key: value}}}})
        self.document[env][self._to_key(cmd_names)][section].update({key: value})

    def flush(self):
        """
        Write the data back to file

        Raises
        ------
        tomlkit.exceptions.TOMLKitError
            If the data is invalid

        """
        self._write()

    def sanity_check(self):
        """
        Sanity check the contents of samconfig
        """
        try:
            self._read()
        except tomlkit.exceptions.TOMLKitError:
            return False
        else:
            return True

    def exists(self):
        return self.filepath.exists()

    def path(self):
        return str(self.filepath)

    @staticmethod
    def config_dir(template_file_path=None):
        """
        SAM Config file is always relative to the SAM Template. If it the template is not
        given, then it is relative to cwd()
        """
        if template_file_path:
            return os.path.dirname(template_file_path)
        return os.getcwd()

    def _read(self):
        if not self.document:
            try:
                txt = self.filepath.read_text()
                self.document = tomlkit.loads(txt)
                self._version_sanity_check(self._version())
            except OSError:
                self.document = tomlkit.document()

        if self.document.body:
            self._version_sanity_check(self._version())
        return self.document

    def _write(self):
        if not self.document:
            return
            if not self.exists():
                open(self.filepath, 'a+').close()
        else:
            current_version = self._version() if self._version() else SAM_CONFIG_VERSION
            try:
                self.document.add(VERSION_KEY, current_version)
            except tomlkit.exceptions.KeyAlreadyPresent:
                pass

        self.filepath.write_text(tomlkit.dumps(self.document))

    def _version(self):
        return self.document.get(VERSION_KEY, None)

    def _version_sanity_check(self, version):
        if not isinstance(version, float):
            raise SamConfigVersionException(f"'{VERSION_KEY}' key is not present or is in unrecognized format. ")

    @staticmethod
    def _to_key(cmd_names):
        return '_'.join([cmd.replace('-', '_').replace(' ', '_') for cmd in cmd_names])