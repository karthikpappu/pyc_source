# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_docker_list.py
# Compiled at: 2019-11-14 13:57:46
import doctest, pytest
from insights.parsers import docker_list
from insights.parsers import SkipException
from insights.tests import context_wrap
DOCKER_LIST_IMAGES = ('\nREPOSITORY                           TAG                 DIGEST              IMAGE ID                                                           CREATED             VIRTUAL SIZE\nrhel6_vsftpd                         latest              <none>              412b684338a1178f0e5ad68a5fd00df01a10a18495959398b2cf92c2033d3d02   37 minutes ago      459.5 MB\nrhel7_imagemagick                    latest              <none>              882ab98aae5394aebe91fe6d8a4297fa0387c3cfd421b2d892bddf218ac373b2   4 days ago          785.4 MB\nrhel6_nss-softokn                    latest              <none>              dd87dad2c7841a19263ae2dc96d32c501ee84a92f56aed75bb67f57efe4e48b5   5 days ago          449.7 MB\n<none>                               <none>              <none>              34c167d900afb820ecab622a214ce3207af80ec755c0dcb6165b425087ddbc3a   5 days ago          205.3 MB\n').strip()
DOCKER_LIST_CONTAINERS = ('\nCONTAINER ID                                                       IMAGE                                                              COMMAND                                            CREATED             STATUS                      PORTS                  NAMES               SIZE\n03e2861336a76e29155836113ff6560cb70780c32f95062642993b2b3d0fc216   rhel7_httpd                                                        "/usr/sbin/httpd -DFOREGROUND"                     45 seconds ago      Up 37 seconds               0.0.0.0:8080->80/tcp   angry_saha          796 B (virtual 669.2 MB)\n95516ea08b565e37e2a4bca3333af40a240c368131b77276da8dec629b7fe102   bd8638c869ea40a9269d87e9af6741574562af9ee013e03ac2745fb5f59e2478   "/bin/sh -c \'yum install -y vsftpd-2.2.2-6.el6\'"   18 hours ago        Exited (137) 18 hours ago                          tender_rosalind     4.751 MB (virtual 200.4 MB)\n').strip()
DOCKER_LIST_IMAGES_NO_DATA = '\nREPOSITORY                           TAG                 DIGEST              IMAGE ID                                                           CREATED             VIRTUAL SIZE\n'

def test_docker_list_images():
    result = docker_list.DockerListImages(context_wrap(DOCKER_LIST_IMAGES))
    assert len(result.rows) == 4
    assert result.rows[0].get('REPOSITORY') == 'rhel6_vsftpd'
    assert result.rows[0].get('TAG') == 'latest'
    assert result.rows[0].get('DIGEST') == '<none>'
    assert result.rows[0].get('IMAGE ID') == '412b684338a1178f0e5ad68a5fd00df01a10a18495959398b2cf92c2033d3d02'
    assert result.rows[0].get('CREATED') == '37 minutes ago'
    assert result.rows[0].get('VIRTUAL SIZE') == '459.5 MB'
    assert result.rows[3].get('REPOSITORY') == '<none>'
    assert result.rows[1].get('TAG') == 'latest'
    assert result.rows[3].get('IMAGE ID') == '34c167d900afb820ecab622a214ce3207af80ec755c0dcb6165b425087ddbc3a'
    assert result.rows[2].get('REPOSITORY') == 'rhel6_nss-softokn'
    assert result.rows[2].get('TAG') == 'latest'
    assert result.rows[2].get('IMAGE ID') == 'dd87dad2c7841a19263ae2dc96d32c501ee84a92f56aed75bb67f57efe4e48b5'
    assert result.data['rhel6_vsftpd']['CREATED'] == '37 minutes ago'
    assert result.data['rhel6_vsftpd'] == result.rows[0]
    assert '<none>' not in result.data


def test_docker_list_containers():
    result = docker_list.DockerListContainers(context_wrap(DOCKER_LIST_CONTAINERS))
    assert len(result.rows) == 2
    assert result.rows[0].get('CONTAINER ID') == '03e2861336a76e29155836113ff6560cb70780c32f95062642993b2b3d0fc216'
    assert result.rows[0].get('COMMAND') == '"/usr/sbin/httpd -DFOREGROUND"'
    assert result.rows[0].get('SIZE') == '796 B (virtual 669.2 MB)'
    assert result.rows[0].get('CREATED') == '45 seconds ago'
    assert result.rows[0].get('PORTS') == '0.0.0.0:8080->80/tcp'
    assert result.rows[1].get('CONTAINER ID') == '95516ea08b565e37e2a4bca3333af40a240c368131b77276da8dec629b7fe102'
    assert result.rows[1].get('COMMAND') == '"/bin/sh -c \'yum install -y vsftpd-2.2.2-6.el6\'"'
    assert result.rows[1]['STATUS'] == 'Exited (137) 18 hours ago'
    assert result.rows[1].get('PORTS') == ''
    assert sorted(result.data.keys()) == sorted(['angry_saha', 'tender_rosalind'])
    assert result.data['angry_saha'] == result.rows[0]
    assert result.data['tender_rosalind'] == result.rows[1]


def test_docker_list_images_no_data():
    with pytest.raises(SkipException) as (ex):
        docker_list.DockerListImages(context_wrap(DOCKER_LIST_IMAGES_NO_DATA))
    assert 'No data.' in str(ex)


def test_undefined_key_field():
    with pytest.raises(NotImplementedError):
        assert docker_list.DockerList(context_wrap(DOCKER_LIST_CONTAINERS)).key_field is None
    return


def test_documentation():
    failed_count, tests = doctest.testmod(docker_list, globs={'images': docker_list.DockerListImages(context_wrap(DOCKER_LIST_IMAGES)), 'containers': docker_list.DockerListContainers(context_wrap(DOCKER_LIST_CONTAINERS))})
    assert failed_count == 0