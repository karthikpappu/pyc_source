# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/app.py
# Compiled at: 2019-12-18 08:49:55
# Size of source mod 2**32: 4937 bytes
import ast, yaml, click, os, shutil
_START_SCRIPT = 'server.py'
_MANIFEST_YAML = 'manifest.yaml'
_DOCKER_FILE = 'Dockerfile'
_DEFAULT_DOCKER_FILE_TPL = 'FROM registry.cn-beijing.aliyuncs.com/tlab/busybox:torch as builder\n\nFROM python:3.7\n\n{cmd}\n\nWORKDIR /app\n\nADD requirements.txt ./\n\nRUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple\n\nCOPY . .\n\nEXPOSE {port}\n\nENV TZ="Asia/Shanghai" PARAMS=" "\n\nCMD python server.py $PARAMS\n'
_START_SCRIPT_CODE = "from grpclib import *\n\nif __name__ == '__main__':\n    server = GrpcServer()\n    server.run()\n"

@click.group()
def cli():
    pass


def find_manifest():
    if os.path.exists(_MANIFEST_YAML):
        with open(_MANIFEST_YAML, 'r') as (f):
            return yaml.safe_load(f)


def parse_manifest(manifest):
    """
    解析清单文件
    :param manifest:
    :return:
    """
    if manifest:
        app = manifest['app']
        rpc_items = []
        if 'docker' in app and 'tpl' in app['docker'] and app['docker']['tpl'] and os.path.exists(app['docker']['tpl']):
            with open(app['docker']['tpl'], 'r') as (f):
                app['docker']['tpl'] = f.read()
        else:
            app['docker']['tpl'] = _DEFAULT_DOCKER_FILE_TPL
        for item in app['rpc']:
            pkg = item['pkg']
            func_name = item['func']
            note = item['note']
            with open(os.sep.join(str(pkg).split('.')) + '.py', 'r') as (f):
                ast_tree = ast.parse(f.read())
                for func in ast_tree.body:
                    if isinstance(func, ast.FunctionDef) and func.name == func_name:
                        arg_names = [arg.arg for arg in func.args.args]
                        rpc_items.append((pkg, func.name, arg_names, note))

        return (
         app, rpc_items)


def _remove_if_exist(path):
    if os.path.exists(path):
        os.remove(path)


def clear_env():
    shutil.rmtree('rpc', ignore_errors=True)
    _remove_if_exist(_DOCKER_FILE)
    _remove_if_exist(_START_SCRIPT)


def create_rpc(app, rpc_items):
    os.makedirs('rpc', exist_ok=True)
    with open('rpc/__init__.py', 'w') as (f):
        pass
    py_file_name = app['name'].capitalize() + 'RpcServer.py'
    py_file_path = os.path.join('rpc', py_file_name)
    with open(py_file_path, 'w') as (f):
        write_line_func = lambda level=0, code='': f.write('{indent}{code}'.format(indent=(level * '\t'), code=code))
        for rpc_item in rpc_items:
            write_line_func(level=0, code=('from {pkg} import {func} as {_func}'.format(pkg=(str(rpc_item[0])), func=(str(rpc_item[1])),
              _func=('_' + str(rpc_item[1]))) + os.linesep))

        f.write(os.linesep * 2)
        for rpc_item in rpc_items:
            func_name = rpc_item[1]
            _func_name = '_' + func_name
            arg_names = rpc_item[2]
            note = rpc_item[3]
            write_line_func(level=0,
              code=('def {func_name}({args}):'.format(func_name=func_name, args=(', '.join(arg_names))) + os.linesep))
            if note:
                write_line_func(level=1, code=('"""' + os.linesep))
                write_line_func(level=1, code=(note + os.linesep))
                write_line_func(level=1, code=('"""' + os.linesep))
            write_line_func(level=1, code=('return {func_name}({args})'.format(func_name=_func_name, args=(', '.join(arg_names))) + os.linesep))
            f.write(os.linesep * 2)


def create_docker(app):
    with open(_DOCKER_FILE, 'w') as (f):
        tpl = app['docker']['tpl']
        app['docker'].pop('tpl')
        fmt_args = {}
        for k in dict(app['docker']).keys():
            v = app['docker'][k]
            if type(v) == list:
                fmt_args[k] = os.linesep.join(v)
            else:
                fmt_args[k] = v

        f.write((tpl.format)(**fmt_args))


def create_startpy():
    """
    创建启动脚本
    :return: 
    """
    with open(_START_SCRIPT, 'w') as (f):
        f.write(_START_SCRIPT_CODE)


@cli.command()
def aic():
    manifest = find_manifest()
    app, rpc_items = parse_manifest(manifest)
    if not (app and rpc_items):
        raise AssertionError('manifest文件解析异常')
    clear_env()
    create_rpc(app, rpc_items)
    create_docker(app)
    create_startpy()


if __name__ == '__main__':
    aic()