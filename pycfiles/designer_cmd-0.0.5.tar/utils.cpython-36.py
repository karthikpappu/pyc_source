# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: designer_cmd\utils\utils.py
# Compiled at: 2020-05-09 08:05:39
# Size of source mod 2**32: 4196 bytes
import logging, sys, os.path as path, os, subprocess
logger = logging.getLogger(__file__)

def windows_platform() -> bool:
    return 'win' in sys.platform


def get_platform_path(version: str='') -> str:
    """
    Вычисляет путь к исполняемому файлу платформы

    :param version: Версия платформы.
    :return:
    """
    if windows_platform():
        platform_path = __get_platform_path_windows(version)
    else:
        platform_path = __get_platform_path_linux(version)
    return platform_path


def __get_version_path(dir_1c, version) -> str:
    bin_path = 'bin\\1cv8.exe'
    exept_dir = ['common', 'conf']
    versions = [dir_name for dir_name in os.listdir(dir_1c) if dir_name not in exept_dir]
    if len(versions) == 0:
        return ''
    if version == '':
        return path.join(dir_1c, sorted(versions, key=get_version_weight, reverse=True)[0], bin_path)
    else:
        if version in versions:
            return path.join(dir_1c, version, bin_path)
        return ''


def get_version_weight(element: str) -> int:
    """
    Вычисляет вес версии, для сравнения версий
    Подразумевается, что версии, для которых будет вычисляться октавы имеют одинаковые длины октавово
    и их длина не больше 4

    :param element:
    :return:
    """
    octs_first = element.split('.')
    octs_first.reverse()
    koef = 1000
    summ = 0
    for i, val in enumerate(octs_first):
        if len(val) > 4:
            logger.error(f"Длина октава {val} в версии {element} больше 4, вычисление веса не поддерживается.")
            raise ValueError('Ошибка вычисления веса версии, длинна октава не должна быть больше 4.')
        summ += int(val) * koef ** i

    return summ


def __get_platform_path_windows(version: str) -> str:
    version_path = __get_version_path(path.join(os.getenv('ProgramW6432'), '1cv8'), version)
    if version_path == '':
        version_path = __get_version_path(path.join(os.getenv('ProgramFiles'), '1cv8'), version)
    if version_path == '':
        if version == '':
            logger.critical('Не обнаружена установленная 1с. Выполнение невозможно.')
            raise EnvironmentError('Не обнаружена установленная 1с.')
        else:
            logger.critical(f"Не обнаружена установленная версия 1с номер версии:{version}. Выполнение невозможно.")
            raise EnvironmentError(f"Не обнаружена версия {version} 1с.")
    return version_path


def __get_platform_path_linux(version: str) -> str:
    platform_path = ''
    return platform_path


def execute_command(command: str, params: list) -> tuple:
    """
    Выполняет команду в системе.

    :param command: Команда
    :param: params: Параметры команды
    :return:
    """
    if windows_platform():
        result = __execute_windows_command(command, params)
    else:
        result = __execute_linux_command(command)
    return result


def __execute_windows_command(command: str, params: list) -> tuple:
    """
    Выполняет команду системы в windows

    :param command:
    :return:
    """
    process = subprocess.run(([command] + params), stdout=(subprocess.PIPE), stderr=(subprocess.PIPE), shell=True)
    if process.returncode == 0:
        msg = process.stdout
    else:
        msg = process.stderr
    return (
     process.returncode, msg.decode('cp866'))


def __execute_linux_command(command) -> str:
    """
    Выполняет команду системы в linux

    :param command:
    :return:
    """
    pass