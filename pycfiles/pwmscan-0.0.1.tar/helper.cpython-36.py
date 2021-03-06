# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/rahul/.pyenv/versions/py3.6.2/lib/python3.6/site-packages/pwmodel/helper.py
# Compiled at: 2018-02-24 18:57:03
# Size of source mod 2**32: 9627 bytes
import itertools, operator, os, random, re, string, struct, sys
from functools import reduce
import bz2, gzip, functools
from math import sqrt
import dawg
BASE_DIR = os.getcwd()
sys.path.append(BASE_DIR)
MAX_INT = 18446744073709551615
DEBUG = os.getenv('DEBUG', False)
START = '\x01'
END = '\x02'
home = os.path.expanduser('~')
thisdir = os.path.dirname(os.path.abspath(__file__))
ROCKYOU_TOTAL_CNT = 32603388.0
pw_characters = string.ascii_letters + string.digits + string.punctuation + ' '

class memoized(object):
    """memoized"""

    def __init__(self, func):
        self.func = func
        self.cache = {}

    def __call__(self, *args):
        try:
            return self.cache[args[0]][args[1:]]
        except KeyError:
            value = (self.func)(*args)
            try:
                self.cache[args[0]][args[1:]] = value
            except KeyError:
                self.cache[args[0]] = {args[1:]: value}

            return value

    def __repr__(self):
        """Return the function's docstring."""
        return self.func.__doc__

    def __get__(self, obj, objtype):
        """Support instance methods."""
        return functools.partial(self.__call__, obj)


class random:

    @staticmethod
    def randints(s, e, n=1):
        """
        returns n uniform random numbers from [s, e]
        """
        assert e >= s, 'Wrong range: [{}, {})'.format(s, e)
        n = max(1, n)
        arr = [s + a % (e - s) for a in struct.unpack('<%dL' % n, os.urandom(4 * n))]
        return arr

    @staticmethod
    def randint(s, e):
        """
        returns one random integer between s and e. Try using @randints in case you need
        multiple random integer. @randints is more efficient
        """
        return random.randints(s, e, 1)[0]

    @staticmethod
    def choice(arr):
        i = random.randint(0, len(arr))
        return arr[i]

    @staticmethod
    def sample(arr, n, unique=False):
        if unique:
            arr = set(arr)
            assert len(arr) > n, 'Cannot sample uniquely from a small array.'
            if len(arr) == n:
                return arr
            if n > len(arr) / 2:
                res = list(arr)
                while len(res) > n:
                    del res[random.randint(0, len(res))]

            else:
                res = []
                arr = list(arr)
                while len(res) < n:
                    i = random.randint(0, len(arr))
                    res.append(arr[i])
                    del arr[i]

        else:
            return [arr[i] for i in random.randints(0, len(arr), n)]


def gen_n_random_num(n, MAX_NUM=MAX_INT, unique=True):
    """
    Returns @n @unique random unsigned integers (4 bytes)     between 0 and @MAX_NUM.
    """
    fmt = '<%dI' % n
    t = struct.calcsize(fmt)
    D = [d % MAX_NUM for d in struct.unpack(fmt, os.urandom(t))]
    if unique:
        D = set(D)
        assert MAX_NUM > n, 'Cannot have {0} unique integers less than {1}'.format(n, MAX_NUM)
        while len(D) < n:
            print('Number of collision: {}. Regenerating!'.format(n - len(D)))
            fmt = '<%dI' % (n - len(D))
            t = struct.calcsize(fmt)
            extra = struct.unpack(fmt, os.urandom(t))
            D |= set(d % MAX_NUM for d in extra)

        D = list(D)
    return D


def sample_following_dist(handle_iter, n, totalf):
    """Samples n passwords following the distribution from the handle
    @handle_iter is an iterator that gives (pw,f) @n is the total
    number of samle asked for @totalf is the total number of users,
    which is euqal to sum(f for pw,f in handle_iter)
    As, handle_iterator is an iterator and can only traverse once, @totalf
    needs to be supplied to the funciton.
    
    Returns, an array of @n tuples (id, pw) sampled from @handle_iter.
    """
    multiplier = 1.0
    if totalf == 1.0:
        multiplier = 100000000.0
    else:
        totalf = totalf * multiplier
        print('# Population Size', totalf)
        A = gen_n_random_num(n, totalf, unique=False)
        A.sort(reverse=True)
        assert len(A) == n, 'Not enough randomnumbers generatedRequried {}, generated only {}'.format(n, len(A))
    j = 0
    sampled = 0
    val = A.pop()
    for w, f in handle_iter:
        j += f * multiplier
        if not A:
            break
        while val < j:
            sampled += 1
            if sampled % 5000 == 0:
                print('Sampled:', sampled)
            yield (
             val, w)
            if A:
                val = A.pop()
            else:
                break

    print('# Stopped at:', w, f, j, '\n')
    while A and val < j:
        yield (
         val, w)
        if A:
            i, val = A.pop()
        else:
            break


def MILLION(n):
    return n * 10000000.0


def sort_dict(D):
    return sorted((list(D.items())), key=(operator.itemgetter(1)))


def file_type(filename, param='rb'):
    magic_dict = {b'\x1f\x8b\x08':'gz', 
     'BZh':'bz2', 
     'PK\x03\x04':'zip'}
    if param.startswith('w'):
        return filename.split('.')[(-1)]
    else:
        max_len = max(len(x) for x in magic_dict)
        with open(filename, 'rb') as (f):
            file_start = f.read(max_len)
        for magic, filetype in list(magic_dict.items()):
            if file_start.startswith(magic):
                return filetype

        return 'no match'


def open_(filename, mode='rb'):
    type_ = file_type(filename, mode)
    errors = 'ignore' if 't' in mode else None
    if type_ == 'bz2':
        f = bz2.open(filename, mode, errors=errors)
    else:
        if type_ == 'gz':
            f = gzip.open(filename, mode, errors=errors)
        else:
            f = open(filename, mode)
    return f


def load_dawg(f, t=dawg.IntDAWG):
    if not f.endswith('.gz'):
        if not os.path.exists(f):
            f += '.gz'
    T = t()
    T.read(open_(f, 'rb'))
    return T


def save_dawg(T, fname):
    if not fname.endswith('gz'):
        fname = fname + '.gz'
    with gzip.open(fname, 'wb') as (f):
        T.write(f)


def getallgroups(arr, k=-1):
    r"""
    returns all the subset of @arr of size less than equalto @k
    the return array will be of size \sum_{i=1}^k nCi, n = len(arr)
    """
    if k < 0:
        k = len(arr)
    return itertools.chain.from_iterable(itertools.combinations(set(arr), j) for j in range(1, k + 1))


def isascii(s):
    try:
        s.encode('ascii')
        return True
    except UnicodeError:
        return False


def get_line(file_object, limit=-1, pw_filter=lambda x: True, errors='replace'):
    regex = re.compile('\\s*([0-9]+) (.*)$')
    i = 0
    for l in file_object:
        if limit > 0:
            if limit <= i:
                break
        c, w = l.rstrip('\n').lstrip().split(' ', 1)
        c = int(c)
        w = w.replace('\x00', '\\x00')
        if w and pw_filter(w) and c > 0:
            i += 1
            yield (w, c)
            continue


def open_get_line(filename, limit=-1, **kwargs):
    with open_(filename, 'rt') as (f):
        for w, c in get_line(f, limit, **kwargs):
            yield (
             w, c)


regex = '([A-Za-z_]+)|([0-9]+)|(\\W+)'

def print_err(*args):
    if DEBUG:
        sys.stderr.write(' '.join([str(a) for a in args]) + '\n')


def tokens(w):
    T = []
    while w:
        m = re.match(regex, w)
        T.append(m.group(0))
        w = w[len(T[(-1)]):]

    return T


def whatchar(c):
    if c.isalpha():
        return 'L'
    else:
        if c.isdigit():
            return 'D'
        return 'Y'


def mean_sd(arr):
    s = sum(arr)
    s2 = sum([x * x for x in arr])
    n = len(arr)
    m = s / float(n)
    sd = sqrt(float(s2) / n - m * m)
    return (
     m, sd)


def prod(arr):
    return reduce(operator.mul, arr, 1)


def convert2group(t, totalC):
    return t + random.randint(0, (MAX_INT - t) / totalC) * totalC


def warning(*objs):
    if DEBUG:
        print('WARNING: ', *objs, **{'file': sys.stderr})


def getIndex(p, A):
    p %= A[(-1)]
    i = 0
    for i, v in enumerate(A):
        p -= v
        if p < 0:
            break

    return i


def dp(**kwargs):
    print(kwargs, file=(sys.stderr))


if __name__ == '__main__':
    print(list(getallgroups([1, 2, 3, 4, 5, 6, 7, 8, 9], 5)))