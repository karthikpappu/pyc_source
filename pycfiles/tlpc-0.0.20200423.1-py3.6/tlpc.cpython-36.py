# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tlp/tlpc.py
# Compiled at: 2020-04-23 19:40:12
# Size of source mod 2**32: 9543 bytes
import argparse, io, json, os, os.path, re, shutil, subprocess, sys
from typing import Dict, List, Optional, TextIO, Tuple
import haoda.backend.xilinx, tlp.core

def main():
    parser = argparse.ArgumentParser(prog='tlpc',
      description='Task-Level Parallelization (TLP) for High-Level Synthesis (HLS) compiler')
    parser.add_argument('--tlpcc', type=str,
      metavar='file',
      dest='tlpcc',
      help='override tlpcc')
    parser.add_argument('--work-dir',
      type=str,
      metavar='dir',
      dest='work_dir',
      help='use a specific working directory instead of a temporary one')
    parser.add_argument('--top', type=str,
      dest='top',
      metavar='TASK_NAME',
      help='name of the top-level task')
    parser.add_argument('--clock-period', type=str,
      dest='clock_period',
      help='clock period in nanoseconds')
    parser.add_argument('--part-num', type=str,
      dest='part_num',
      help='part number')
    parser.add_argument('--platform', type=str,
      dest='platform',
      help='SDAccel platform')
    parser.add_argument('--cflags', type=str,
      dest='cflags',
      help='cflags for kernel, space separated')
    parser.add_argument('--output', '-o',
      type=str,
      dest='output_file',
      metavar='file',
      help='output file')
    parser.add_argument('--directive', type=(argparse.FileType('r')),
      dest='directive',
      help='partitioning directive json')
    parser.add_argument('--constraint', type=(argparse.FileType('w')),
      dest='constraint',
      help='partitioning constraint tcl')
    parser.add_argument(type=str, dest='input_file',
      metavar='file',
      help='tlp source code or tlp program json')
    group = parser.add_argument_group('steps')
    group.add_argument('--run-tlpcc', action='count',
      dest='run_tlpcc',
      help='run tlpcc and create program.json')
    group.add_argument('--extract-cpp', action='count',
      dest='extract_cpp',
      help='extract HLS C++ files from program.json')
    group.add_argument('--run-hls', action='count',
      dest='run_hls',
      help='run HLS and generate RTL tarballs')
    group.add_argument('--extract-rtl', action='count',
      dest='extract_rtl',
      help='untar RTL tarballs')
    group.add_argument('--instrument-rtl', action='count',
      dest='instrument_rtl',
      help='instrument RTL')
    group.add_argument('--pack-xo', action='count',
      dest='pack_xo',
      help='package as Xilinx object')
    args = parser.parse_args()
    all_steps = True
    last_step = ''
    for arg in ('run_tlpcc', 'extract_cpp', 'run_hls', 'extract_rtl', 'instrument_rtl',
                'pack_xo'):
        if getattr(args, arg) is not None:
            all_steps = False
            last_step = arg

    if all_steps:
        last_step = arg
    elif last_step == 'run_tlpcc':
        if args.output_file is None:
            parser.error('output file must be set if tlpcc is the last step')
        if last_step == 'pack_xo':
            if args.output_file is None:
                parser.error('output file must be set if pack xo is the last step')
    else:
        if not all_steps:
            if last_step != 'run_tlpcc':
                if args.work_dir is None:
                    parser.error("steps beyond run tlpcc won't work with --work-dir unset")
        if all_steps or args.run_tlpcc is not None:
            tlpcc_cmd = []
            if args.tlpcc is None:
                tlpcc = shutil.which('tlpcc')
            else:
                tlpcc = args.tlpcc
            if tlpcc is None:
                parser.error('cannot find tlpcc')
            tlpcc_cmd += (tlpcc, args.input_file)
            if args.top is None:
                parser.error('tlpcc cannot run without --top')
            tlp_include_dir = os.path.join(os.path.dirname(sys.argv[0]), '..', '..', 'src')
            tlpcc_cmd += ('-top', args.top, '--', '-I', tlp_include_dir)
            for clang_version in ('10', '9', '8', '7', '6.0', '5.0', '4.0', '3.9',
                                  '3.8', '3.7', '3.6', '3.5'):
                clang_include = os.path.join('/', 'usr', 'lib', 'clang', clang_version, 'include')
                if os.path.isdir(clang_include):
                    break
            else:
                parser.error('tlpcc cannot run without clang headers')

            tlpcc_cmd += ('-I', clang_include)
            proc = subprocess.run(tlpcc_cmd, stdout=(subprocess.PIPE),
              universal_newlines=True,
              check=False)
            if proc.returncode != 0:
                parser.exit(status=(proc.returncode))
            tlp_program_json_dict = json.loads(proc.stdout)
            input_file_basename = os.path.basename(args.input_file)
            input_file_dirname = os.path.dirname(args.input_file)
            deps = subprocess.check_output([
             'clang++-' + clang_version,
             '-MM',
             input_file_basename,
             '-I',
             tlp_include_dir],
              cwd=input_file_dirname,
              universal_newlines=True)
            deps = deps.rstrip('\n').partition('.o: ')[(-1)].replace('\\\n', ' ')
            dep_set = {x.replace('\\ ', ' ') for x in re.split('(?<!\\\\) ', deps)}
            dep_set = set(filter(lambda x: not os.path.isabs(x) and x not in {
             '',
             input_file_basename,
             os.path.join(tlp_include_dir, 'tlp.h')}, dep_set))
            for dep in dep_set:
                tlp_program_json_dict.setdefault('headers', {})
                with open(os.path.join(input_file_dirname, dep), 'r') as (dep_fp):
                    tlp_program_json_dict['headers'][dep] = dep_fp.read()

            tlp_program_json_str = json.dumps(tlp_program_json_dict, indent=2)
            if args.work_dir is not None or last_step == 'run_tlpcc':
                if last_step == 'run_tlpcc':
                    tlp_program_json_file = args.output_file
                else:
                    tlp_program_json_file = os.path.join(args.work_dir, 'program.json')
                os.makedirs((os.path.dirname(tlp_program_json_file)), exist_ok=True)
                with open(tlp_program_json_file, 'w') as (output_fp):
                    output_fp.write(tlp_program_json_str)
            tlp_program_json = lambda : io.StringIO(tlp_program_json_str)
        else:
            if args.input_file.endswith('.json') or args.work_dir is None:
                tlp_program_json = lambda : open(args.input_file)
            else:
                tlp_program_json = lambda : open(os.path.join(args.work_dir, 'program.json'))
    cflags = ' -I' + os.path.join(os.path.dirname(tlp.__file__), 'assets', 'cpp')
    if args.cflags is not None:
        cflags += ' ' + args.cflags
    with tlp_program_json() as (tlp_program_json_obj):
        program = tlp.core.Program(tlp_program_json_obj, cflags=cflags,
          work_dir=(args.work_dir))
    if all_steps or args.extract_cpp is not None:
        program.extract_cpp()
    if all_steps or args.run_hls is not None:
        platform = args.platform
        if platform is not None:
            platform = os.path.join(os.path.dirname(platform), os.path.basename(platform).replace(':', '_').replace('.', '_'))
        if platform is not None:
            if not os.path.isdir(platform):
                platform = os.path.join('/', 'opt', 'xilinx', 'platforms', platform)
        if platform is None or not os.path.isdir(platform):
            if args.clock_period is None:
                parser.error('--platform is not valid and neither is --clock-period')
            if args.part_num is None:
                parser.error('--platform is not valid and neither is --part-num')
            hls_kwargs = {'clock_period':args.clock_period,  'part_num':args.part_num}
        else:
            hls_kwargs = haoda.backend.xilinx.get_device_info(platform)
        if args.clock_period is not None:
            hls_kwargs['clock_period'] = args.clock_period
        if args.part_num is not None:
            hls_kwargs['part_num'] = args.part_num
        (program.run_hls)(**hls_kwargs)
    if all_steps or args.extract_rtl is not None:
        program.extract_rtl()
    if all_steps or args.instrument_rtl is not None:
        directive = None
        if args.directive is not None:
            if args.constraint is not None:
                directive = (
                 json.load(args.directive), args.constraint)
        program.instrument_rtl(directive)
    if all_steps or args.pack_xo is not None:
        with open(args.output_file, 'wb') as (packed_obj):
            program.pack_rtl(packed_obj)


if __name__ == '__main__':
    main()