# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/qiniuManager/run.py
# Compiled at: 2017-10-04 23:43:58
from __future__ import print_function
import os, sys
from qiniuManager import manager, utils, __version__, __author__
__all__ = [
 'parser', 'command']

def parser():
    u"""
    终端参数解析
    :return: (args, parser)
    """
    import argparse
    parse = argparse.ArgumentParser(description='七牛云存储管理助手 Qiniu Manager', formatter_class=argparse.RawTextHelpFormatter, conflict_handler='resolve', epilog=('\x1b[01;31m首次使用\x1b[00m请设置密钥对\r\nqiniu [-k|--key] <access key> <secret key>\r\n\r\n必要情况下请设置\x1b[01;31m默认空间名\x1b[00m\r\n\r\n查看更多帮助信息\r\nhttps://github.com/{}/qiniu_manager/blob/v{}/README.md').format(__author__, __version__))
    parse.add_argument('-v', '--version', action='store_true', help='显示程序版本号以及运行环境')
    parse.add_argument('-h', '--help', action='store_true', help='显示此帮助信息')
    parse.add_argument('-x', dest='export', action='append', nargs='?', metavar='ns', help='导出默认或指定空间文件下载链接')
    parse.add_argument('-l', '--list', action='append', nargs='?', metavar='ns', help='显示文件列表')
    parse.add_argument('--size', action='store_true', help='按大小排序')
    parse.add_argument('--revert', action='store_false', help='反向排序')
    parse.add_argument('-la', '--list-all', action='store_true', help='显示本地已知所有空间文件列表')
    parse.add_argument('-ld', dest='list_debug', action='append', nargs='?', metavar='ns', help='调试文件列表输出')
    parse.add_argument('-s', dest='space_check', action='append', nargs='?', metavar='ns', help='添加、设置默认空间或查看空间列表')
    parse.add_argument('--alias', help='指定空间关联域名')
    parse.add_argument('-sr', dest='space_remove', metavar='ns', help='删除本地空间')
    parse.add_argument('-c', dest='check', action='store_true', help='查看文件状态')
    parse.add_argument('-cd', dest='check_debug', action='store_true', help='调试查看文件状态的输出')
    parse.add_argument('-r', '--remove', action='store_true', help='删除云文件')
    parse.add_argument('-rf', '--force-remove', action='store_true', help='强制删除云文件')
    parse.add_argument('-d', '--download', action='store_true', help='下载文件')
    parse.add_argument('-t', dest='target', help='选择下载`目录`')
    parse.add_argument('-dd', dest='download_debug', action='store_true', help='调试下载')
    parse.add_argument('-p', '--private', dest='private_link', action='store_true', help='获取私有下载链接')
    parse.add_argument('-i', '--link', action='store_true', help='获取公开下载链接')
    parse.add_argument('-rn', dest='rename', metavar='name', nargs='?', help='文件重命名')
    parse.add_argument('-rd', dest='rename_debug', metavar='name', nargs='?', help='调试文件重命名')
    parse.add_argument('-f', '--find', action='store_true', help='搜索文件')
    parse.add_argument('-gt', dest='greater', action='store_true', help='大于指定大小的文件列表')
    parse.add_argument('-lt', dest='littler', action='store_true', help='小于指定大小的文件列表')
    parse.add_argument('file', nargs='?', help='文件名')
    parse.add_argument('space', nargs='?', help='空间名')
    parse.add_argument('-k', '--key', nargs=argparse.REMAINDER, help='查看或添加as、ak')
    return (
     parse.parse_args(), parse)


def command(args, parse):
    u"""
    调用参数解析，完成指令响应
    :param args: 参数名字空间
    :param parse: 参数解析器
    :return: None
    """
    if args.help:
        parse.print_help()
    elif args.version:
        print(('Qiniu Manager {}').format(__version__))
        print('Python: ' + sys.version)
    else:
        qiniu = manager.Qiniu()
        if args.export:
            if not args.export[0]:
                _, result = qiniu.export_download_links()
            else:
                _, result = qiniu.export_download_links(args.export[0])
            print(result)
        elif args.list:
            if not args.list[0]:
                _, result = qiniu.list(reverse=args.revert, by_date=not args.size)
            else:
                _, result = qiniu.list(args.list[0], reverse=args.revert, by_date=not args.size)
            print(result)
        elif args.list_debug:
            if not args.list_debug[0]:
                _, result = qiniu.list(reverse=args.revert, by_date=not args.size, is_debug=True)
            else:
                _, result = qiniu.list(args.list_debug[0], reverse=args.revert, by_date=not args.size, is_debug=True)
            print(result)
        elif args.list_all:
            print(qiniu.list_all(reverse=args.revert, by_date=not args.size)[1])
        elif args.space_check:
            if not args.space_check[0]:
                default = qiniu.config.get_default_space()
                space_list = qiniu.config.get_space_list()
                print('已知空间名如下:')
                print(('\r\n-------------\r\n').join([ ('{}\r\n{}').format(s[0], s[1]) for s in space_list
                                                     ]))
                if default:
                    print(('\n默认空间:  \x1b[01;31m{}\x1b[00m').format(default[0]))
            elif not args.alias:
                qiniu.config.set_space(args.space_check[0])
                print(('\x1b[01;31m{}\x1b[00m 现在变为默认空间').format(args.space_check[0]))
            else:
                qiniu.config.set_space(args.space_check[0], args.alias)
                print(('\x1b[01;31m{}\x1b[00m 现在使用 {} 作为关联域名').format(args.space_check[0], args.alias))
        elif args.alias:
            default = qiniu.config.get_default_space()
            if default:
                qiniu.config.set_space(default, args.alias)
                print(('默认空间现在使用 {} 作为关联域名').format(args.alias))
            else:
                print('若不指定空间，则需要设置默认空间')
        elif args.space_remove:
            qiniu.config.remove_space(args.space_remove)
            print(('\x1b[01;31m{}\x1b[00m 已从本地数据库中删除').format(args.space_remove))
        elif args.check:
            if args.file and not args.space:
                print(qiniu.check(args.file)[1])
            elif args.file and args.space:
                print(qiniu.check(args.file, args.space)[1])
            else:
                print('请指定要查看的文件')
        elif args.check_debug:
            if args.file and not args.space:
                print(qiniu.check(args.file, is_debug=True)[1])
            elif args.file and args.space:
                print(qiniu.check(args.file, args.space, is_debug=True)[1])
            else:
                print('请指定要查看的文件')
        elif args.remove:
            if args.file:
                r = qiniu.remove(args.file, args.space)
                try:
                    while True:
                        target, space = next(r)
                        if not target:
                            prompt = ('{} 无文件匹配 `{}` ').format(space, args.file)
                        else:
                            prompt = ('删除来自 \x1b[01;34m{space}\x1b[00m 的 `\x1b[01;31m{target}\x1b[00m` ').format(space=space, target=target)
                        if utils.prompt(prompt):
                            _, ret = r.send(True)
                        else:
                            _, ret = r.send(False)
                        if ret:
                            print(ret)

                except StopIteration:
                    pass
                except Exception as e:
                    print(e)

            else:
                print('请指定要删除的文件')
                return False
        elif args.force_remove:
            if args.file:
                try:
                    r = qiniu.remove(args.file, args.space, stop=False)
                    for _, i in next(r):
                        print(i)

                    r.close()
                except StopIteration:
                    pass
                except Exception as e:
                    print(e)

            else:
                print('请指定要删除的文件')
        elif args.download:
            if not args.target:
                if args.file and not args.space:
                    print(qiniu.download(args.file)[1])
                elif args.file and args.space:
                    print(qiniu.download(args.file, space=args.space)[1])
                else:
                    print('请指定要下载的文件')
            elif args.file and not args.space:
                print(qiniu.download(args.file, space=None, directory=args.target)[1])
            elif args.file and args.space:
                print(qiniu.download(args.file, space=args.space, directory=args.target)[1])
        elif args.download_debug:
            if not args.target:
                if args.file and not args.space:
                    print(qiniu.download(args.file, is_debug=True)[1])
                elif args.file and args.space:
                    print(qiniu.download(args.file, space=args.space, is_debug=True)[1])
                else:
                    print('请指定要下载的文件')
            elif args.file and not args.space:
                print(qiniu.download(args.file, space=None, directory=args.target, is_debug=True)[1])
            elif args.file and args.space:
                print(qiniu.download(args.file, space=args.space, directory=args.target, is_debug=True)[1])
            else:
                print('请指定要下载的文件')
        elif args.private_link:
            if args.file and not args.space:
                print(qiniu.private_download_link(args.file)[1])
            elif args.file and args.space:
                print(qiniu.private_download_link(args.file, args.space)[1])
            else:
                print('请指定文件')
        elif args.link:
            if args.file and not args.space:
                print(qiniu.regular_download_link(args.file)[1])
            elif args.file and args.space:
                print(qiniu.regular_download_link(args.file, args.space)[1])
            else:
                print('请指定文件')
        elif args.rename:
            if args.file and not args.space:
                print(qiniu.rename(args.rename, args.file)[1])
            elif args.file and args.space:
                print(qiniu.rename(args.rename, args.file, args.space)[1])
            else:
                print('请给出新的文件名')
        elif args.rename_debug:
            if args.file and not args.space:
                print(qiniu.rename(args.rename_debug, args.file, is_debug=True)[1])
            elif args.file and args.space:
                print(qiniu.rename(args.rename_debug, args.file, args.space, is_debug=True)[1])
            else:
                print('请给出新的文件名')
        elif args.find:
            if args.file and not args.space:
                print(qiniu.list_all(reverse=args.revert, by_date=not args.size, find_pattern=args.file)[1])
            elif args.file and args.space:
                print(qiniu.list(space=args.space, reverse=args.revert, by_date=not args.size, find_pattern=args.file)[1])
            else:
                print('请输入要匹配的模式')
        elif args.greater:
            if args.file.isdigit() and not args.space:
                print(qiniu.list_all(reverse=args.revert, by_date=not args.size, greater=int(args.file))[1])
            elif args.file.isdigit() and args.space:
                print(qiniu.list(args.space, reverse=args.revert, by_date=not args.size, greater=int(args.file))[1])
            else:
                print('请输入正确大小，单位为字节')
        elif args.littler:
            if args.file.isdigit() and not args.space:
                print(qiniu.list_all(reverse=args.revert, by_date=not args.size, littler=int(args.file))[1])
            elif args.file.isdigit() and args.space:
                print(qiniu.list(space=args.space, reverse=args.revert, by_date=not args.size, littler=int(args.file))[1])
            else:
                print('请输入正确大小，单位为字节')
        elif type(args.key) is list:
            if len(args.key) == 0:
                key = qiniu.config.get_one_access()
                print(('AK: {}\nSK: {}').format(key[0], key[1]) if key else '数据库中暂无存储的密钥')
            elif len(args.key) == 2:
                qiniu.config.add_access(args.key[0], args.key[1])
                print('密钥添加成功')
            else:
                print('若要添加密钥，请按序输入AK、SK')
        elif args.file:
            if os.path.isfile(args.file):
                if args.space:
                    qiniu.upload(args.file, args.space)
                else:
                    qiniu.upload(args.file)
                if qiniu.state:
                    print(('\x1b[01;31m{}\x1b[00m 已上传到 \x1b[01;32m{}\x1b[00m \r\n上传速率: \x1b[01;32m{}\x1b[00m').format(os.path.basename(args.file), args.space or qiniu.default_space, qiniu.avg_speed))
                else:
                    print(('\x1b[01;31m{}\x1b[00m 上传失败\r\n错误：`{}`\r\n请检查网络或空间状态').format(os.path.basename(args.file), qiniu.fail_reason))
            else:
                print(('\x1b[01;31m{}\x1b[00m 文件不存在或为目录').format(args.file))
        else:
            parse.print_help()
    return


def run():
    command(*parser())


if __name__ == '__main__':
    run()