# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.5/site-packages/bookshelf/api_v3/cloud_instance.py
# Compiled at: 2016-08-21 18:37:21
# Size of source mod 2**32: 4132 bytes
from zope.interface import Interface, Attribute
from flufl.enum import Enum

class Distribution(Enum):
    __doc__ = '\n    Enumeration of distributions supported by the bookshelf v3 api.\n\n    :ivar CENTOS7: constant for CentOS 7.\n    :ivar UBUNTU1404: constante for Ubuntu LTS 14.04.\n    '
    CENTOS7 = 'centos7'
    UBUNTU1404 = 'ubuntu1404'


class ICloudInstanceFactory(Interface):
    __doc__ = '\n    Interface for an object that can create cloud instances either\n    from some existing serialized/saved state, or create a new cloud\n    instance from a configuration.\n    '

    def create_from_config(config, distro, region):
        """
        Creates a new instance of the specified distro from the given
        configuration.

        :param dict config: An implementation-specific configuration
            dictionary. This is most likely something read in from a
            configuration language and passed directly to this layer.
        :param Distribution distro: The distribution to spin the instance up
            as.
        :param unicode region: The region to spin the instance up within.

        :return: An :class:`ICloudInstance` provider for a newly created
            instance with type distro.
        """
        pass

    def create_from_saved_state(config, saved_state):
        """
        Re-create or connect to an existing cloud instance as specified in some
        saved state and configuration.

        :param config: An opaque dict of configuration that might be
            specific to a given implementation
        :param saved_state: The serialized state of an instance that
            has most likely been loaded from disk (e.g. a json file).
            This saved state will be used to reconnect to an existing
            instance.

        :return: An :class:`ICloudInstance` provider loaded from the
            saved_state.
        """
        pass


class ICloudInstance(Interface):
    __doc__ = '\n    Interface for interacting with a single cloud interface.\n    '
    cloud_type = Attribute('The name of the cloud this instance comes from.')
    username = Attribute('The username to use to log into the instance.')
    key_filename = Attribute('The filename of the private key to use to log into the instance.')
    ip_address = Attribute('Externally accessable IP address for the instance')
    distro = Attribute('The distribution on the instance. Should be one of the above Distributions.')
    region = Attribute('The region the instance is in.')
    image_basename = Attribute('The basename for the image. The final name will look likeimage_basename-YYYYMMDDHHMMSS')

    def create_image(image_name):
        """
        Creates an image from the boot disk of the instance, and leaves the
        instance in an up (booted) state.

        :param unicode image_name: The name of the image to create.

        :returns: The unique identifier of the image.
        """
        pass

    def delete_image(image_name):
        """
        Hack: This should not go in the instance as it's a general cloud
        operation. If more general cloud operaions are needed, they
        should be broken out of the Instance object into their own
        thing.

        Deletes an image from the cloud

        :param unicode image_name: the name of the image to delete
        """
        pass

    def destroy():
        """
        Downs and Destroys the instance.
        """
        pass

    def down():
        """
        Stops a running instance. Throws an exception if the instance is not
        running. Note that this must be done in a way where the instance can be
        started again.
        """
        pass

    def get_state():
        """
        Serializes this instance to a dictionary that can be passed to
        ``ICloudInstanceFactory.create_from_saved_state`` in order to
        re-create an :class:`ICloudInstance` that references the same
        underlying instance.

        :returns dict: A simple dictionary of plain old data that can be
            serialized using the JSON library.
        """
        pass