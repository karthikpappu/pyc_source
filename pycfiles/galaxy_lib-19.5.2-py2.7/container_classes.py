# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/galaxy/tools/deps/container_classes.py
# Compiled at: 2019-04-28 04:54:30
import os, string
from abc import ABCMeta, abstractmethod
import six
from galaxy.containers.docker_model import DockerVolume
from galaxy.util import asbool, in_directory
from . import docker_util, singularity_util
from .requirements import DEFAULT_CONTAINER_RESOLVE_DEPENDENCIES, DEFAULT_CONTAINER_SHELL
DOCKER_CONTAINER_TYPE = 'docker'
SINGULARITY_CONTAINER_TYPE = 'singularity'
LOAD_CACHED_IMAGE_COMMAND_TEMPLATE = '\npython << EOF\nfrom __future__ import print_function\n\nimport json\nimport re\nimport subprocess\nimport tarfile\n\nt = tarfile.TarFile("${cached_image_file}")\nmeta_str = t.extractfile(\'repositories\').read()\nmeta = json.loads(meta_str)\ntag, tag_value = meta.items()[0]\nrev, rev_value = tag_value.items()[0]\ncmd = "${images_cmd}"\nproc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)\nstdo, stde = proc.communicate()\nfound = False\nfor line in stdo.split("\\n"):\n    tmp = re.split(r\'\\s+\', line)\n    if tmp[0] == tag and tmp[1] == rev and tmp[2] == rev_value:\n        found = True\nif not found:\n    print("Loading image")\n    cmd = "cat ${cached_image_file} | ${load_cmd}"\n    subprocess.check_call(cmd, shell=True)\nEOF\n'

@six.add_metaclass(ABCMeta)
class Container(object):

    def __init__(self, container_id, app_info, tool_info, destination_info, job_info, container_description):
        self.container_id = container_id
        self.app_info = app_info
        self.tool_info = tool_info
        self.destination_info = destination_info
        self.job_info = job_info
        self.container_description = container_description

    def prop(self, name, default):
        destination_name = 'docker_%s' % name
        return self.destination_info.get(destination_name, default)

    @property
    def resolve_dependencies(self):
        if not self.container_description:
            return DEFAULT_CONTAINER_RESOLVE_DEPENDENCIES
        return self.container_description.resolve_dependencies

    @property
    def shell(self):
        if not self.container_description:
            return DEFAULT_CONTAINER_SHELL
        return self.container_description.shell

    @abstractmethod
    def containerize_command(self, command):
        """
        Use destination supplied container configuration parameters,
        container_id, and command to build a new command that runs
        input command in container.
        """
        pass


def preprocess_volumes(volumes_raw_str, container_type):
    """Process Galaxy volume specification string to either Docker or Singularity specification.

    Galaxy allows the mount try "default_ro" which translates to ro for Docker and
    ro for Singularity iff no subdirectories are rw (Singularity does not allow ro
    parent directories with rw subdirectories).

    >>> preprocess_volumes("/a/b", DOCKER_CONTAINER_TYPE)
    ['/a/b:rw']
    >>> preprocess_volumes("/a/b:ro,/a/b/c:rw", DOCKER_CONTAINER_TYPE)
    ['/a/b:ro', '/a/b/c:rw']
    >>> preprocess_volumes("/a/b:default_ro,/a/b/c:rw", DOCKER_CONTAINER_TYPE)
    ['/a/b:ro', '/a/b/c:rw']
    >>> preprocess_volumes("/a/b:default_ro,/a/b/c:rw", SINGULARITY_CONTAINER_TYPE)
    ['/a/b:rw', '/a/b/c:rw']
    """
    volumes_raw_strs = [ v.strip() for v in volumes_raw_str.split(',') ]
    volumes = []
    rw_paths = []
    for volume_raw_str in volumes_raw_strs:
        volume_parts = volume_raw_str.split(':')
        if len(volume_parts) > 2:
            raise Exception('Unparsable volumes string in configuration [%s]' % volumes_raw_str)
        if len(volume_parts) == 1:
            volume_parts.append('rw')
        volumes.append(volume_parts)
        if volume_parts[1] == 'rw':
            rw_paths.append(volume_parts[0])

    for volume in volumes:
        path = volume[0]
        how = volume[1]
        if how == 'default_ro':
            how = 'ro'
            if container_type == SINGULARITY_CONTAINER_TYPE:
                for rw_path in rw_paths:
                    if in_directory(rw_path, path):
                        how = 'rw'

        volume[1] = how

    return [ (':').join(v) for v in volumes ]


class HasDockerLikeVolumes(object):
    """Mixin to share functionality related to Docker volume handling.

    Singularity seems to have a fairly compatible syntax for volume handling.
    """

    def _expand_volume_str(self, value):
        if not value:
            return value
        else:
            template = string.Template(value)
            variables = dict()

            def add_var(name, value):
                if value:
                    if not value.startswith('$'):
                        value = os.path.abspath(value)
                    variables[name] = value

            add_var('working_directory', self.job_info.working_directory)
            add_var('tmp_directory', self.job_info.tmp_directory)
            add_var('job_directory', self.job_info.job_directory)
            add_var('tool_directory', self.job_info.tool_directory)
            add_var('galaxy_root', self.app_info.galaxy_root_dir)
            add_var('default_file_path', self.app_info.default_file_path)
            add_var('library_import_dir', self.app_info.library_import_dir)
            if self.job_info.job_directory and self.job_info.job_directory_type == 'pulsar':
                defaults = '$job_directory:default_ro,$tool_directory:default_ro,$job_directory/outputs:rw,$working_directory:rw'
            else:
                defaults = '$galaxy_root:default_ro,$tool_directory:default_ro'
                if self.job_info.job_directory:
                    defaults += ',$job_directory:default_ro'
                if self.job_info.tmp_directory is not None:
                    defaults += ',$tmp_directory:rw'
                if self.app_info.outputs_to_working_directory:
                    defaults += ',$working_directory:rw,$default_file_path:default_ro'
                else:
                    defaults += ',$working_directory:rw,$default_file_path:rw'
            if self.app_info.library_import_dir:
                defaults += ',$library_import_dir:default_ro'
            variables['defaults'] = string.Template(defaults).safe_substitute(variables)
            return template.safe_substitute(variables)


class DockerContainer(Container, HasDockerLikeVolumes):
    container_type = DOCKER_CONTAINER_TYPE

    @property
    def docker_host_props(self):
        docker_host_props = dict(docker_cmd=self.prop('cmd', docker_util.DEFAULT_DOCKER_COMMAND), sudo=asbool(self.prop('sudo', docker_util.DEFAULT_SUDO)), sudo_cmd=self.prop('sudo_cmd', docker_util.DEFAULT_SUDO_COMMAND), host=self.prop('host', docker_util.DEFAULT_HOST))
        return docker_host_props

    def build_pull_command(self):
        return docker_util.build_pull_command(self.container_id, **self.docker_host_props)

    def containerize_command(self, command):
        env_directives = []
        for pass_through_var in self.tool_info.env_pass_through:
            env_directives.append('"%s=$%s"' % (pass_through_var, pass_through_var))

        for key, value in six.iteritems(self.destination_info):
            if key.startswith('docker_env_'):
                env = key[len('docker_env_'):]
                env_directives.append('"%s=%s"' % (env, value))

        working_directory = self.job_info.working_directory
        if not working_directory:
            raise Exception('Cannot containerize command [%s] without defined working directory.' % working_directory)
        volumes_raw = self._expand_volume_str(self.destination_info.get('docker_volumes', '$defaults'))
        preprocessed_volumes_list = preprocess_volumes(volumes_raw, self.container_type)
        volumes = [ DockerVolume.from_str(v) for v in preprocessed_volumes_list ]
        if self.job_info.tmp_directory is not None:
            volumes.append(DockerVolume.from_str('%s:/tmp:rw' % self.job_info.tmp_directory))
        volumes_from = self.destination_info.get('docker_volumes_from', docker_util.DEFAULT_VOLUMES_FROM)
        docker_host_props = self.docker_host_props
        cached_image_file = self.__get_cached_image_file()
        if not cached_image_file:
            cache_command = docker_util.build_docker_cache_command(self.container_id, **docker_host_props)
        else:
            cache_command = self.__cache_from_file_command(cached_image_file, docker_host_props)
        run_command = docker_util.build_docker_run_command(command, self.container_id, volumes=volumes, volumes_from=volumes_from, env_directives=env_directives, working_directory=working_directory, net=self.prop('net', 'none'), auto_rm=asbool(self.prop('auto_rm', docker_util.DEFAULT_AUTO_REMOVE)), set_user=self.prop('set_user', docker_util.DEFAULT_SET_USER), run_extra_arguments=self.prop('run_extra_arguments', docker_util.DEFAULT_RUN_EXTRA_ARGUMENTS), **docker_host_props)
        return '%s\n%s' % (cache_command, run_command)

    def __cache_from_file_command(self, cached_image_file, docker_host_props):
        images_cmd = docker_util.build_docker_images_command(truncate=False, **docker_host_props)
        load_cmd = docker_util.build_docker_load_command(**docker_host_props)
        return string.Template(LOAD_CACHED_IMAGE_COMMAND_TEMPLATE).safe_substitute(cached_image_file=cached_image_file, images_cmd=images_cmd, load_cmd=load_cmd)

    def __get_cached_image_file(self):
        container_id = self.container_id
        cache_directory = os.path.abspath(self.__get_destination_overridable_property('container_image_cache_path'))
        cache_path = docker_cache_path(cache_directory, container_id)
        if os.path.exists(cache_path):
            return cache_path
        else:
            return

    def __get_destination_overridable_property(self, name):
        prop_name = 'docker_%s' % name
        if prop_name in self.destination_info:
            return self.destination_info[prop_name]
        else:
            return getattr(self.app_info, name)


def docker_cache_path(cache_directory, container_id):
    file_container_id = container_id.replace('/', '_slash_')
    cache_file_name = 'docker_%s.tar' % file_container_id
    return os.path.join(cache_directory, cache_file_name)


class SingularityContainer(Container, HasDockerLikeVolumes):
    container_type = SINGULARITY_CONTAINER_TYPE

    def get_singularity_target_kwds(self):
        return dict(singularity_cmd=self.prop('cmd', singularity_util.DEFAULT_SINGULARITY_COMMAND), sudo=asbool(self.prop('sudo', singularity_util.DEFAULT_SUDO)), sudo_cmd=self.prop('sudo_cmd', singularity_util.DEFAULT_SUDO_COMMAND))

    def build_mulled_singularity_pull_command(self, cache_directory, namespace='biocontainers'):
        return singularity_util.pull_mulled_singularity_command(docker_image_identifier=self.container_id, cache_directory=cache_directory, namespace=namespace, **self.get_singularity_target_kwds())

    def containerize_command(self, command):
        env = []
        for pass_through_var in self.tool_info.env_pass_through:
            env.append((pass_through_var, '$%s' % pass_through_var))

        for key, value in six.iteritems(self.destination_info):
            if key.startswith('singularity_env_'):
                real_key = key[len('singularity_env_'):]
                env.append((real_key, value))

        working_directory = self.job_info.working_directory
        if not working_directory:
            raise Exception('Cannot containerize command [%s] without defined working directory.' % working_directory)
        volumes_raw = self._expand_volume_str(self.destination_info.get('singularity_volumes', '$defaults'))
        preprocessed_volumes_list = preprocess_volumes(volumes_raw, self.container_type)
        volumes = [ DockerVolume.from_str(v) for v in preprocessed_volumes_list ]
        run_command = singularity_util.build_singularity_run_command(command, self.container_id, volumes=volumes, env=env, working_directory=working_directory, run_extra_arguments=self.prop('run_extra_arguments', singularity_util.DEFAULT_RUN_EXTRA_ARGUMENTS), **self.get_singularity_target_kwds())
        return run_command


CONTAINER_CLASSES = dict(docker=DockerContainer, singularity=SingularityContainer)

class NullContainer(object):

    def __init__(self):
        pass

    def __bool__(self):
        return False

    __nonzero__ = __bool__


NULL_CONTAINER = NullContainer()