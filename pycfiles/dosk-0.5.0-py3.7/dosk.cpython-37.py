# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/dosk/dosk.py
# Compiled at: 2020-04-23 17:59:41
# Size of source mod 2**32: 15982 bytes
import argparse, json, asyncio, functools, logging, os, shlex, signal, string, sys
from ruamel.yaml import YAML
import string, random, copy, coloredlogs, shutil
from distutils.dir_util import copy_tree
from pathlib import Path
log = logging.getLogger(name='dosk')
FORMAT = '%(asctime)s-%(levelname)s-%(name)s %(message)s'
env_cmd = ';jq -n env > {}.json'

def main():
    args = parse_args()
    coloredlogs.install(fmt=FORMAT, level=(args.verbose))
    path = str(Path(os.getcwd()))
    if args.local:
        path = local_build(path)
    tasks = TaskDefs('dosk.yml', path)
    try:
        task = tasks[args.task]
    except KeyError:
        error('Task {} not defined. {}'.format(args.task, tasks))

    loop = asyncio.get_event_loop()
    for sig in (signal.SIGTERM, signal.SIGINT, signal.SIGQUIT):
        handler = functools.partial(handle_signal, sig, task)
        loop.add_signal_handler(sig, handler)

    loop.run_until_complete(task.run())


def local_build(path):
    os.mkdir(str(path) + '/local')
    fromDirectory = str(path)
    path = str(path) + '/local'
    copy_tree(fromDirectory, path)
    shutil.rmtree(path + '/local')
    return path


def parse_args():
    parser = argparse.ArgumentParser(prog='dock', description='Do Task - The Simple DevOps Task Runner')
    parser.add_argument('task', nargs='?', help='Name of task to execute')
    parser.add_argument('--local', '-l', action='store_const', const=True, default=False,
      dest='local',
      help='Load local variables')
    verbose = parser.add_mutually_exclusive_group()
    verbose.add_argument('--verbose', '-v', action='store_const', const='DEBUG', default='INFO', help='Print additional information')
    verbose.add_argument('--quiet', '-q', action='store_const', dest='verbose', const='WARNING', help='Print less information')
    args = parser.parse_args()
    if not args.task:
        parser.error('Must specify a task')
    return args


def error(message):
    """ Give error message and exit"""
    log.error(message)
    sys.exit(1)


def _extract_env_and_vars(parsed):
    end = {}
    with open('dosk.yml') as (f):
        datafile = f.readlines()
    env = os.environ.copy()
    for line in datafile:
        try:
            dollar = find(line, '$')
            for i, d in enumerate(dollar):
                for idx, letter in enumerate(line):
                    if letter.isalpha() or idx > dollar[i]:
                        end[i] = idx
                        break

                out = line[int(d + 1):int(end[i])]
                if out not in env:
                    os.environ[out] = ''

        except ValueError:
            pass

    vars = {}
    if 'vars' in parsed:
        o_vars = parsed['vars']
    vars = json.loads(json.dumps(o_vars))
    return vars


async def env_ject(string):
    if string.startswith('$'):
        out = os.getenv(string[1:])
    else:
        out = string
    return out


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


async def condition_clean(old_string):
    print(old_string)
    dollar = find(old_string, '$')
    space = find(old_string, ' ')
    print(dollar, space)
    for i, d in enumerate(dollar):
        out = old_string[int(d):int(space[i] - 1)]
        print(out)

    new = ''
    return new


async def env_string(line):
    end = {}
    env_var = ''
    try:
        dollar = find(line, '$')
        for i, d in enumerate(dollar):
            for idx, letter in enumerate(line):
                if not letter.isalpha():
                    if idx > dollar[i]:
                        end[i] = idx
                        break
                if idx + 1 == len(line):
                    end[i] = idx + 1

            env_var = line[int(d + 1):int(end[i])]

    except ValueError:
        pass

    if env_var:
        out = line.replace('$' + env_var, os.getenv(env_var))
    else:
        out = line
    return out


async def load_env(rando):
    with open('{}.json'.format(rando), 'r') as (file):
        data = file.read()
    env_json = json.loads(data)
    for i, attribute in enumerate(env_json):
        os.environ[attribute] = env_json[attribute]

    os.remove('{}.json'.format(rando))


def random_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join((random.choice(chars) for x in range(size)))


async def _inplace_change(filename, old_string, new_string):
    reading_file = open(filename, 'r')
    new_file_content = ''
    for line in reading_file:
        new_line = line.replace(old_string, new_string)
        new_file_content += new_line

    reading_file.close()
    writing_file = open(filename, 'w')
    writing_file.write(new_file_content)
    writing_file.close()


async def _append_line(filename, line):
    append_file = open(filename, 'a')
    append_file.write('\n' + line)
    append_file.close()


async def watch(stream, cmd):
    async for line in stream:
        print(line.decode().strip())


@asyncio.coroutine
def inplace_change(filename, old_string, new_string):
    reading_file = open(filename, 'r')
    new_file_content = ''
    for line in reading_file:
        new_line = line.replace(old_string, new_string)
        new_file_content += new_line

    reading_file.close()
    writing_file = open(filename, 'w')
    writing_file.write(new_file_content)
    writing_file.close()


class TaskDefs(dict):

    def __init__(self, taskfile, path):
        self.taskfile = Path(taskfile)
        self.path = path
        with open(taskfile) as (config):
            yaml = YAML()
            parsed = yaml.load(config)
            self.vars = _extract_env_and_vars(parsed)
            self.tasks = self._parse_tasks(parsed)

    def __getitem__(self, key):
        return self.tasks[key]

    def __str__(self):
        to_str = [
         'Available tasks:']
        to_str.extend(['\t{}'.format(task) for task in self.tasks])
        return '\n'.join(to_str)

    def _parse_tasks(self, parsed):
        tasks = {}
        for taskname, obj in parsed.items():
            subtasks = []
            path = Path(os.getcwd())
            self.run_vars = {}
            directory = self.path
            if 'dir' in obj:
                post = obj['dir']
                directory = directory + '/' + post.replace('$', '')
            self.run_vars['dir'] = directory
            if 'condition' in obj:
                self.run_vars['condition'] = obj['condition'].replace('$', '')
            if 'replace' in obj:
                self.run_vars['replace'] = obj['replace']
            if 'inject' in obj:
                self.run_vars['inject'] = obj['inject']
            if 'append' in obj:
                self.run_vars['append'] = obj['append']
            if 'loop' in obj:
                if isinstance(obj['loop'], int):
                    self.run_vars['loop'] = obj['loop']
                else:
                    self.run_vars['loop'] = obj['loop'].replace('$', '')
            if 'task' in obj:
                logging.debug('Parsing `{}`'.format(obj['task']))
                if isinstance(obj['task'], str):
                    subtasks.append(Task(obj['task'], directory))
                else:
                    for subspec in obj['task']:
                        try:
                            subtasks.append(tasks[subspec])
                        except KeyError:
                            subtasks.append(Task(subspec, directory))

            self.run_vars.update(self.vars)
            if taskname.endswith('@'):
                tasks[taskname[:-1]] = AsyncTaskList(subtasks, self.run_vars)
            else:
                tasks[taskname] = SequentialTaskList(subtasks, self.run_vars)

        return tasks


class Task(object):

    def __init__(self, cmd, directory):
        logging.debug('Creating task with command "{}"'.format(cmd))
        self.cmd = cmd
        self.dir = directory
        self.proc = None

    def __str__(self):
        to_str = [
         'cmd: ']
        to_str.extend(['{}'.format(cmd) for cmd in self.cmd])
        return ''.join(to_str)

    def terminate(self):
        try:
            if self.proc.returncode is None:
                log.debug('Terminating {}'.format(self.cmd))
                self.proc.terminate()
        except AttributeError:
            pass

    def update(self, vars):
        self.vars = vars
        self.cmd = (self.cmd.format)(**self.vars)

    async def run(self, args=None):
        rando = random_generator()
        env_rnd = env_cmd.format(rando)
        cmd = self.cmd + env_rnd
        if args:
            cmd = ' '.join([
             cmd, ' '.join((shlex.quote(token) for token in args))])
        os.chdir(self.dir)
        self.proc = await asyncio.create_subprocess_shell(cmd, stdout=(asyncio.subprocess.PIPE), stderr=(asyncio.subprocess.PIPE))
        log.info(self.cmd)
        await asyncio.gather(watch(self.proc.stdout, self.cmd), watch(self.proc.stderr, '[stderr]'))
        await self.proc.wait()
        await load_env(rando)


class PythonTask(object):

    def __init__(self, program):
        logging.debug('Creating task with command "{}"'.format(program))
        self.program = program
        self.proc = None

    def __str__(self):
        to_str = [
         'python: ']
        to_str.extend(list(self.program))
        return ''.join(to_str)

    def terminate(self):
        try:
            if self.proc.returncode is None:
                log.debug('Terminating {}'.format(self.program))
                self.proc.terminate()
        except AttributeError:
            pass

    async def run(self, args=None):
        program = self.program
        log.info(self.program)
        self.proc = asyncio.create_task(self.program)
        await self.proc


class TaskList(object):

    def __init__(self, tasks, vars, *args, **kwargs):
        self.tasks = tasks
        self.vars = vars
        self.condition = False
        if 'condition' not in self.vars:
            self.condition = True
        elif 'loop' in self.vars:
            self.loop = self.vars['loop']
            if isinstance(self.loop, int):
                self.wloop = 'count < ' + str(self.loop)
            else:
                self.vars['looplist'] = self.vars[self.loop]
                length = len(self.vars['looplist'])
                self.wloop = 'count < ' + str(length)
        else:
            self.wloop = 'count < 1'

    def __str__(self):
        to_str = [
         'Task List']
        to_str.extend(['\t{}'.format(task) for task in self.tasks])
        return '\n'.join(to_str)

    def append(self, task):
        tasks.append(task)


class SequentialTaskList(TaskList):

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.kill = False
        self.current = None

    async def run(self, args=None):
        last = len(self.tasks) - 1
        env = os.environ.copy()
        self.vars.update(env)
        if self.condition == False:
            condition = await env_ject(self.vars['condition'])
            if eval(condition, self.vars):
                self.condition = True
        if 'replace' in self.vars:
            os.chdir(self.vars['dir'])
            if isinstance(self.vars['replace'], list):
                for line in self.vars['replace']:
                    old = await env_ject(line[1])
                    new = await env_ject(line[2])
                    await _inplace_change(line[0], (old.format)(**self.vars), (new.format)(**self.vars))

        if self.condition:
            count = 0
            while eval(self.wloop):
                count += 1
                self.vars['count'] = count
                if 'looplist' in self.vars:
                    self.vars['loop'] = self.vars['looplist'][(count - 1)]
                for i, task in enumerate(self.tasks):
                    run_task = copy.copy(task)
                    if isinstance(run_task, Task):
                        run_task.cmd = (run_task.cmd.format)(**self.vars)
                    if self.kill:
                        break
                    self.current = run_task
                    await run_task.run(args if i == last else None)

        if 'inject' in self.vars:
            if isinstance(self.vars['inject'], list):
                for line in self.vars['inject']:
                    old = await env_ject(line[1])
                    new = await env_ject(line[2])
                    await _inplace_change(line[0], (old.format)(**self.vars), (new.format)(**self.vars))

        if 'append' in self.vars:
            if isinstance(self.vars['append'], list):
                for line in self.vars['append']:
                    clean = await env_string(line[1])
                    await _append_line(line[0], (clean.format)(**self.vars))

    def terminate(self):
        self.kill = True
        try:
            self.current.terminate()
        except AttributeError:
            pass


class AsyncTaskList(TaskList):

    async def run(self, args=None):
        if args:
            error('Additional arguments not valid for Async tasks')
        else:
            run_tasks = copy.copy(self.tasks)
            print(run_tasks)
            count = 0
            env = os.environ.copy()
            self.vars.update(env)
            if self.condition == False:
                condition = await env_ject(self.vars['condition'])
                if eval(condition, self.vars):
                    self.condition = True
            if 'replace' in self.vars:
                os.chdir(self.vars['dir'])
                if isinstance(self.vars['replace'], list):
                    for line in self.vars['replace']:
                        old = await env_ject(line[1])
                        new = await env_ject(line[2])
                        await _inplace_change(line[0], (old.format)(**self.vars), (new.format)(**self.vars))

            while eval(self.wloop):
                count += 1
                for i, task in enumerate(self.tasks):
                    task.update(self.vars)
                    run_tasks.append(task)

            await asyncio.wait([task.run() for task in run_tasks],
              return_when=(asyncio.FIRST_EXCEPTION))
            if 'inject' in self.vars:
                if isinstance(self.vars['inject'], list):
                    for line in self.vars['inject']:
                        old = await env_ject(line[1])
                        new = await env_ject(line[2])
                        await _inplace_change(line[0], (old.format)(**self.vars), (new.format)(**self.vars))

            if 'append' in self.vars and isinstance(self.vars['append'], list):
                for line in self.vars['append']:
                    clean = await env_string(line[1])
                    await _append_line(line[0], (clean.format)(**self.vars))

    def terminate(self):
        for task in self.tasks:
            task.terminate()


def handle_signal(signum, task):
    log.debug('Caught {}'.format(signal.Signals(signum).name))
    task.terminate()


if __name__ == '__main__':
    main()