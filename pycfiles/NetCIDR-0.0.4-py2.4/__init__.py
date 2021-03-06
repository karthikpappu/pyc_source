# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/netcidr/__init__.py
# Compiled at: 2007-12-30 21:05:54
import itertools, utils, ipmath
masks = xrange(33)

def getSpanningBlocks(start, end):
    """
    This is a special case of the getLargestBlock function, where the IP address to
    be excluded is end + 1.

    >>> start = '172.31.0.0'
    >>> end = '172.31.0.10'
    >>> blocks = getSpanningBlocks(start, end)
    >>> blocks
    [172.31.0.0/29, 172.31.0.8/31, 172.31.0.10]
    >>> for block in blocks:
    ...   block.getHostRange()
    (172.31.0.0, 172.31.0.7)
    (172.31.0.8, 172.31.0.9)
    (172.31.0.10, 172.31.0.10)

    >>> start = '10.0.7.0'
    >>> end = '10.0.10.1'
    >>> blocks = getSpanningBlocks(start, end)
    >>> blocks
    [10.0.7.0/24, 10.0.8.0/23, 10.0.10.0/31]
    >>> for block in blocks:
    ...    block.getHostRange()
    (10.0.7.0, 10.0.7.255)
    (10.0.8.0, 10.0.9.255)
    (10.0.10.0, 10.0.10.1)

    >>> start = '192.168.4.4'
    >>> end = '192.168.4.53'
    >>> blocks = getSpanningBlocks(start, end)
    >>> blocks
    [192.168.4.4/30, 192.168.4.8/29, 192.168.4.16/28, 192.168.4.32/28, 192.168.4.48/30, 192.168.4.52/31]
    >>> for block in blocks:
    ...    block.getHostRange()
    (192.168.4.4, 192.168.4.7)
    (192.168.4.8, 192.168.4.15)
    (192.168.4.16, 192.168.4.31)
    (192.168.4.32, 192.168.4.47)
    (192.168.4.48, 192.168.4.51)
    (192.168.4.52, 192.168.4.53)
    """
    nets = []
    current = start
    excluded = ipmath.int2octets(ipmath.octets2int(end) + 1)
    nets.append(_getLargestBlock(start, excluded))
    while CIDR(current) <= CIDR(end):
        current = nets[(-1)].getHostRange()[(-1)].getIP()
        current = ipmath.int2octets(ipmath.octets2int(current) + 1)
        net = _getLargestBlock(current, excluded)
        if net:
            nets.append(net)

    return nets


def _getLargestBlock(start, excluded):
    """
    We work our way from smallest mask to largest (largest network to
    smallest), so the first network we get to that doesn't have the IP that we
    want to exclude will actually be the largest network without it.

    >>> start = '172.31.0.0'
    >>> excluded = '172.31.0.10'
    >>> c = _getLargestBlock(start, excluded)
    >>> c
    172.31.0.0/29
    >>> c.getHostRange()
    (172.31.0.0, 172.31.0.7)

    >>> start = '192.168.4.112'
    >>> excluded = '192.168.4.128'
    >>> c = _getLargestBlock(start, excluded)
    >>> c
    192.168.4.112/28
    >>> c.getHostRange()
    (192.168.4.112, 192.168.4.127)
    """
    for mask in masks:
        c = CIDR('%s/%s' % (start, mask))
        if c.getHostRange()[0] != CIDR(start):
            continue
        if c and CIDR(excluded) not in Networks([c]):
            return c


def getLargestBlock(start, excludedList):
    """
    Get the largest possible network that doesn't include the given IP
    addressed.

    >>> startIP = '10.0.0.0'
    >>> exclude = ['10.0.6.50', '10.0.10.0']
    >>> c = getLargestBlock(startIP, exclude)
    >>> c
    10.0.0.0/22
    >>> c.getHostRange()
    (10.0.0.0, 10.0.3.255)

    >>> startIP = '10.0.7.0'
    >>> exclude = ['10.0.6.50', '10.0.10.0']
    >>> c = getLargestBlock(startIP, exclude)
    >>> c
    10.0.7.0/24
    >>> c.getHostRange()
    (10.0.7.0, 10.0.7.255)

    # let's test some tricky stuff
    >>> exclude = ['192.168.4.67', '192.168.4.127']
    >>> c = getLargestBlock('192.168.4.64', exclude)
    >>> c
    192.168.4.64/31
    >>> c.getHostRange()
    (192.168.4.64, 192.168.4.65)
    >>> set(exclude).intersection(c.getIPs())
    set([])

    >>> c = getLargestBlock('192.168.4.66', exclude)
    >>> c
    192.168.4.66
    >>> c.getHostRange()
    (192.168.4.66, 192.168.4.66)
    >>> set(exclude).intersection(c.getIPs())
    set([])

    >>> c = getLargestBlock('192.168.4.68', exclude)
    >>> c
    192.168.4.68/30
    >>> c.getHostRange()
    (192.168.4.68, 192.168.4.71)
    >>> set(exclude).intersection(c.getIPs())
    set([])

    >>> c = getLargestBlock('192.168.4.71', exclude)
    >>> c
    192.168.4.71
    >>> c.getHostRange()
    (192.168.4.71, 192.168.4.71)
    >>> set(exclude).intersection(c.getIPs())
    set([])

    >>> c = getLargestBlock('192.168.4.72', exclude)
    >>> c
    192.168.4.72/29
    >>> c.getHostRange()
    (192.168.4.72, 192.168.4.79)
    >>> set(exclude).intersection(c.getIPs())
    set([])

    >>> c = getLargestBlock('192.168.4.80', exclude)
    >>> c
    192.168.4.80/28
    >>> c.getHostRange()
    (192.168.4.80, 192.168.4.95)
    >>> set(exclude).intersection(c.getIPs())
    set([])

    >>> c = getLargestBlock('192.168.4.96', exclude)
    >>> c
    192.168.4.96/28
    >>> c.getHostRange()
    (192.168.4.96, 192.168.4.111)
    >>> set(exclude).intersection(c.getIPs())
    set([])
    """
    candidates = []

    def compareIPs(x, y):
        x = CIDR(x)
        y = CIDR(y)
        return cmp(x.getOctetTuple(), y.getOctetTuple())

    excludedList.sort(compareIPs)
    for excl in excludedList:
        if CIDR(start) > CIDR(excl):
            continue
        candidates.append(_getLargestBlock(start, excl))

    if candidates:
        return candidates[0]


class CIDR(object):
    """
    VLSM stands for variable length subnet mask and is the data
    after the slash. It is also called the "prefix length"

    # Let's make sure our globbing works
    >>> CIDR('10.4.1.2')
    10.4.1.2
    >>> CIDR('10.4.1.x')
    10.4.1.0/24
    >>> CIDR('10.4.x.2')
    10.4.0.0/16
    >>> CIDR('10.4.x.x')
    10.4.0.0/16
    >>> CIDR('10.*.*.*')
    10.0.0.0/8

    # Now let's check out the zeros and get some host counts
    # while we're at it
    #
    # Since there may very well be many circumstances were one
    # would have a valid single address ending in one or more
    # zeros, I don't think it's a good idea to force this
    # behavior. I will comment out for now and may completely
    # remove sometime in the future.
    #>>> CIDR('10.4.1.0')
    #10.4.1.0/24
    #>>> c = CIDR('10.4.0.0')
    #>>> c
    #10.4.0.0/16
    #>>> c.getHostCount()
    #65536
    #>>> c = CIDR('10.0.0.0')
    #>>> c
    #10.0.0.0/8
    #>>> c.getHostCount()
    #16777216
    #>>> CIDR('0.0.0.0')
    #0.0.0.0/0
    #>>> CIDR('10.0.0.2')
    #10.0.0.2/32

    # How about manual CIDR entries?
    >>> c = CIDR('172.16.4.28/31')
    >>> c
    172.16.4.28/31
    >>> c.getHostCount()
    2
    >>> c.getHostRange()
    (172.16.4.28, 172.16.4.29)
    >>> c.getOctetTuple()
    (172, 16, 4, 28)

    >>> c = CIDR('172.16.4.28/27')
    >>> c
    172.16.4.28/27
    >>> c.getHostCount()
    32
    >>> c.getHostRange()
    (172.16.4.0, 172.16.4.31)
    >>> c = CIDR('172.16.4.28/15')
    >>> c
    172.16.4.28/15
    >>> c.getHostCount()
    131072

    # What about some silly errors:
    >>> c = CIDR('10.100.2.4/12/11')
    Traceback (most recent call last):
    ValueError: There appear to be too many '/' in your network notation.
    """
    __module__ = __name__

    def __init__(self, cidrString):
        net = cidrString.split('/')
        mask = 32
        if len(net) == 2:
            (net, mask) = net
            mask = int(mask)
            utils.validateMask(mask)
        elif len(net) > 2:
            msg = "There appear to be too many '/' in your network notation."
            raise ValueError, msg
        else:
            net = net[0]
        self.mask = mask
        self.net = net
        self.octets = net.split('.')
        self.globCheck()
        self.raw = None
        return

    def __cmp__(self, other):
        """
        >>> c1 = CIDR('192.168.0.0')
        >>> c2 = CIDR('192.168.0.0')
        >>> c1 > c2
        False
        >>> c1 < c2
        False
        >>> c1 == c2
        True

        >>> c1 = CIDR('192.168.0.0')
        >>> c2 = CIDR('192.168.0.1')
        >>> c1 > c2
        False
        >>> c1 < c2
        True
        >>> c1 == c2
        False

        >>> c1 = CIDR('192.168.117.1')
        >>> c2 = CIDR('192.168.21.0')
        >>> c3 = CIDR('192.168.4.1')
        >>> c1 > c2 > c3
        True
        >>> c1 < c2 < c3
        False
        >>> c1 == c2
        False
        """
        return cmp(self.getOctetTuple(), other.getOctetTuple())

    def __repr__(self):
        if self.mask == 32:
            return self.net
        return '%s/%s' % (self.net, self.mask)

    def getIP(self):
        return self.net

    def getOctetTuple(self):
        return tuple([ int(x) for x in self.octets ])

    def globCheck(self):
        netGlobs = [
         '*', 'x', 'X']
        check = False
        for char in netGlobs:
            if char in self.net:
                check = True

        if not check:
            return False
        globIndex = None
        for index in range(len(self.octets) - 1, -1, -1):
            if self.octets[index] in netGlobs:
                globIndex = index

        for index in range(globIndex, 4):
            self.octets[index] = '0'

        if not (globIndex is None and self.mask is None):
            self.mask = globIndex * 8
        self.net = ('.').join(self.octets)
        return

    def zeroCheck(self):
        if not self.octets[3] == '0':
            return False
        zeros = [
         1, 1, 1, 0]
        if self.octets[2] == '0':
            zeros[2] = 0
            if self.octets[1] == '0':
                zeros[1] = 0
                if self.octets[0] == '0':
                    zeros[0] = 0
        self.mask = zeros.index(0) * 8
        return True

    def getHostCount(self):
        return 2 ** (32 - self.mask)

    def _getOctetRange(self, position, chunkSize):
        divide_by = 256 / chunkSize
        for i in xrange(divide_by):
            start = i * chunkSize
            end = i * chunkSize + chunkSize - 1
            if start <= position <= end:
                return (
                 start, end)

    def getHostRange(self):
        """
        XXX Convert this method to use ipmath.

        This is a lazy way of doing binary subnet math ;-)

        The first thing we do is make two copies of the CIDR octets
        stored in self.octets. We have one copy each for the address
        representing the first host in the range and then the last
        host in the range.

        Next, we check to see what octet we will be dealing with
        by looking at the netmask (self.mask). Then we get the list
        index for that octet and calculate the octet number from
        this.

        The next bit is a little strange and really deserves a
        description: chunkSize. This really means "how many times
        is the current octect divided up?" We use that number and
        the CIDR value for the octet in question to determine the
        netblock range.

        # Let's try the first octet
        >>> CIDR('172.16.4.28/31').getHostRange()
        (172.16.4.28, 172.16.4.29)
        >>> CIDR('172.16.4.27/31').getHostRange()
        (172.16.4.26, 172.16.4.27)

        >>> CIDR('172.16.4.28/30').getHostRange()
        (172.16.4.28, 172.16.4.31)
        >>> CIDR('172.16.4.27/30').getHostRange()
        (172.16.4.24, 172.16.4.27)

        >>> CIDR('172.16.4.28/29').getHostRange()
        (172.16.4.24, 172.16.4.31)
        >>> CIDR('172.16.4.31/29').getHostRange()
        (172.16.4.24, 172.16.4.31)
        >>> CIDR('172.16.4.32/29').getHostRange()
        (172.16.4.32, 172.16.4.39)

        >>> CIDR('172.16.4.27/28').getHostRange()
        (172.16.4.16, 172.16.4.31)
        >>> CIDR('172.16.4.27/27').getHostRange()
        (172.16.4.0, 172.16.4.31)
        >>> CIDR('172.16.4.27/26').getHostRange()
        (172.16.4.0, 172.16.4.63)
        >>> CIDR('172.16.4.27/25').getHostRange()
        (172.16.4.0, 172.16.4.127)
        >>> CIDR('172.16.4.27/24').getHostRange()
        (172.16.4.0, 172.16.4.255)

        # Let's work on the next octet
        >>> CIDR('172.16.4.27/23').getHostRange()
        (172.16.4.0, 172.16.5.255)
        >>> CIDR('172.16.4.27/22').getHostRange()
        (172.16.4.0, 172.16.7.255)
        >>> CIDR('172.16.4.27/21').getHostRange()
        (172.16.0.0, 172.16.7.255)
        >>> CIDR('172.16.4.27/20').getHostRange()
        (172.16.0.0, 172.16.15.255)
        >>> CIDR('172.16.4.27/19').getHostRange()
        (172.16.0.0, 172.16.31.255)
        >>> CIDR('172.16.4.27/18').getHostRange()
        (172.16.0.0, 172.16.63.255)
        >>> CIDR('172.16.4.27/17').getHostRange()
        (172.16.0.0, 172.16.127.255)
        >>> CIDR('172.16.4.27/16').getHostRange()
        (172.16.0.0, 172.16.255.255)

        # Now the next octet
        >>> CIDR('172.16.4.27/15').getHostRange()
        (172.16.0.0, 172.17.255.255)
        >>> CIDR('172.16.4.27/14').getHostRange()
        (172.16.0.0, 172.19.255.255)
        >>> CIDR('172.16.4.27/13').getHostRange()
        (172.16.0.0, 172.23.255.255)
        >>> CIDR('172.16.4.27/12').getHostRange()
        (172.16.0.0, 172.31.255.255)
        >>> CIDR('172.16.4.27/11').getHostRange()
        (172.0.0.0, 172.31.255.255)
        >>> CIDR('172.16.4.27/10').getHostRange()
        (172.0.0.0, 172.63.255.255)
        >>> CIDR('172.16.4.27/9').getHostRange()
        (172.0.0.0, 172.127.255.255)
        >>> CIDR('172.16.4.27/8').getHostRange()
        (172.0.0.0, 172.255.255.255)

        # Now the final octet
        >>> CIDR('172.16.4.27/7').getHostRange()
        (172.0.0.0, 173.255.255.255)
        >>> CIDR('172.16.4.27/6').getHostRange()
        (172.0.0.0, 175.255.255.255)
        >>> CIDR('172.16.4.27/5').getHostRange()
        (168.0.0.0, 175.255.255.255)
        >>> CIDR('172.16.4.27/4').getHostRange()
        (160.0.0.0, 175.255.255.255)
        >>> CIDR('172.16.4.27/3').getHostRange()
        (160.0.0.0, 191.255.255.255)
        >>> CIDR('172.16.4.27/2').getHostRange()
        (128.0.0.0, 191.255.255.255)
        >>> CIDR('172.16.4.27/1').getHostRange()
        (128.0.0.0, 255.255.255.255)
        >>> CIDR('172.16.4.27/0').getHostRange()
        (0.0.0.0, 255.255.255.255)
        """
        so = [ int(x) for x in self.octets ]
        eo = [ int(x) for x in self.octets ]
        if self.mask >= 24:
            sidx = 3
        elif self.mask >= 16:
            so[3] = 0
            eo[3] = 255
            sidx = 2
        elif self.mask >= 8:
            so[2] = so[3] = 0
            eo[2] = eo[3] = 255
            sidx = 1
        elif self.mask < 8:
            so[1] = so[2] = so[3] = 0
            eo[1] = eo[2] = eo[3] = 255
            sidx = 0
        octetNumber = 4 - (sidx + 1)
        chunkSize = 2 ** (32 - self.mask) / 256 ** octetNumber
        (start, end) = self._getOctetRange(so[sidx], chunkSize)
        so[sidx] = start
        eo[sidx] = end
        so = [ str(x) for x in so ]
        eo = [ str(x) for x in eo ]
        return (
         CIDR(('.').join(so)), CIDR(('.').join(eo)))

    def iterIPs(self):
        """
        An iterator for all the IP addresses in the CIDR object's range.
        """
        (start, stop) = [ x.getIP() for x in self.getHostRange() ]
        return utils.iterIPs(start, stop)

    def getIPs(self):
        """
        >>> c = CIDR('172.16.4.28/31')
        >>> ips = c.getIPs()
        >>> len(ips) == c.getHostCount() == 2
        True
        >>> ips
        ['172.16.4.28', '172.16.4.29']
        >>> c = CIDR('192.168.0.64/26')
        >>> ips = c.getIPs()
        >>> len(ips) == c.getHostCount() == 64
        True
        >>> ips[0], ips[-1]
        ('192.168.0.64', '192.168.0.127')
        """
        return list(self.iterIPs())


class Networks(list):
    """
    >>> privateBlock = CIDR('192.168.4.0/24')
    >>> corpBlock = CIDR('10.5.0.0/16')
    >>> vpnBlock = CIDR('172.16.9.5/27')

    >>> mynets = Networks([privateBlock, corpBlock, vpnBlock])

    >>> homeRouter = CIDR('192.168.4.1')
    >>> laptop1 = CIDR('192.168.4.100')
    >>> webserver = CIDR('10.5.10.10')
    >>> laptop2 = CIDR('172.16.9.17')
    >>> google = CIDR('64.233.187.99')

    >>> homeRouter in mynets
    True
    >>> laptop1 in mynets
    True
    >>> webserver in mynets
    True
    >>> laptop2 in mynets
    True
    >>> google in mynets
    False
    """
    __module__ = __name__

    def __contains__(self, cidrObj):
        """
        This allows us to use the "in" keyward with the Networks object.
        """
        for network in self:
            if self.isInRange(cidrObj, netblock=network):
                return True

        return False

    def isInRange(self, cidrObj, cidrTuple=(), netblock=None):
        """
        This might normally be a prive method, but since it might be
        generally useful, we'll make it "public."

        >>> privateBlock = CIDR('192.168.4.0/24')
        >>> mynet = Networks([privateBlock])
        >>> router = CIDR('192.168.4.1')
        >>> fileserver = CIDR('192.168.4.10')
        >>> laptop = CIDR('192.168.4.100')
        >>> mynet.isInRange(router, (fileserver, laptop))
        False
        >>> mynet.isInRange(fileserver, (router, laptop))
        True
        >>> mynet.isInRange(fileserver, cidrTuple=(router, laptop))
        True
        >>> mynet.isInRange(router, netblock=privateBlock)
        True

        >>> mynet.isInRange(router)
        Traceback (most recent call last):
        ValueError: You must provide either a tuple of CIDR objects or a CIDR object that represents a netblock.

        # let's try an edge case
        >>> ip = CIDR('192.168.4.111')
        >>> c = CIDR('192.168.4.96/28')
        >>> str(ip) in c.getIPs()
        True
        >>> n = Networks([c])
        >>> ip in n
        True
        """
        if not (cidrTuple or netblock):
            msg = 'You must provide either a tuple of CIDR objects or a ' + 'CIDR object that represents a netblock.'
            raise ValueError, msg
        if cidrTuple:
            (start, end) = cidrTuple
        else:
            (start, end) = netblock.getHostRange()
        if start <= cidrObj <= end:
            return True
        return False

    def getHostCount(self):
        """
        Return the total number of hosts for all blocks defined in the Networks
        instance.

        >>> blocks = ['172.16.0.0/16', '172.29.13.0/24', '10.1.24.0/26']
        >>> nets = Networks([CIDR(x) for x in blocks])
        >>> obtained = nets.getHostCount()
        >>> obtained
        65856
        >>> counts = [CIDR(x).getHostCount() for x in blocks]
        >>> counts
        [65536, 256, 64]
        >>> obtained == sum(counts)
        True
        """
        return sum([ x.getHostCount() for x in self ])

    def iterIPs(self):
        """
        Iterate through the IP addresses for each block in the collection.

        >>> ips = ['192.168.4.44/31', '172.16.5.5/32', '10.2.1.1/30']
        >>> nets = Networks([CIDR(x) for x in ips])
        >>> for host in nets.iterIPs():
        ...   print host
        192.168.4.44
        192.168.4.45
        172.16.5.5
        10.2.1.0
        10.2.1.1
        10.2.1.2
        10.2.1.3
        """
        return itertools.chain(*[ x.iterIPs() for x in self ])

    def assembleBlocks(self, startIP, endIP):
        """
        Build a collection of network, the sum of which exactly span
        (inclusively) the hosts from startIP through endIP.

        >>> start = '172.31.0.0'
        >>> end = '172.31.0.10'
        >>> nets = Networks()
        >>> nets.assembleBlocks(start, end)
        >>> for net in nets:
        ...   net, net.getHostRange()
        (172.31.0.0/29, (172.31.0.0, 172.31.0.7))
        (172.31.0.8/31, (172.31.0.8, 172.31.0.9))
        (172.31.0.10, (172.31.0.10, 172.31.0.10))

        >>> start = '10.0.7.0'
        >>> end = '10.0.10.1'
        >>> nets = Networks()
        >>> nets.assembleBlocks(start, end)
        >>> for net in nets:
        ...   net, net.getHostRange()
        (10.0.7.0/24, (10.0.7.0, 10.0.7.255))
        (10.0.8.0/23, (10.0.8.0, 10.0.9.255))
        (10.0.10.0/31, (10.0.10.0, 10.0.10.1))

        >>> start = '192.168.4.4'
        >>> end = '192.168.4.53'
        >>> nets = Networks()
        >>> nets.assembleBlocks(start, end)
        >>> for net in nets:
        ...   net, net.getHostRange()
        (192.168.4.4/30, (192.168.4.4, 192.168.4.7))
        (192.168.4.8/29, (192.168.4.8, 192.168.4.15))
        (192.168.4.16/28, (192.168.4.16, 192.168.4.31))
        (192.168.4.32/28, (192.168.4.32, 192.168.4.47))
        (192.168.4.48/30, (192.168.4.48, 192.168.4.51))
        (192.168.4.52/31, (192.168.4.52, 192.168.4.53))
        """
        blocks = getSpanningBlocks(startIP, endIP)
        self.extend(blocks)

    def withoutIPs(self, startIP, endIP, listOfIPs):
        """
        Build a collection of networks begining with startIP but that do not
        include the given IP addresses.

        >>> startIP = '192.168.4.0'
        >>> endIP = '192.168.4.255'
        >>> exclude = ['192.168.4.111']
        >>> nets = Networks()
        >>> nets.withoutIPs(startIP, endIP, exclude)
        >>> for net in nets:
        ...   print net
        192.168.4.0/26
        192.168.4.64/27
        192.168.4.96/29
        192.168.4.104/30
        192.168.4.108/31
        192.168.4.110
        192.168.4.112/28
        192.168.4.128/25

        # let's limit things even more:
        >>> startIP = '192.168.4.0'
        >>> endIP = '192.168.4.255'
        >>> exclude = ['192.168.4.10', '192.168.4.11', '192.168.4.111',
        ...   '192.168.4.255']
        >>> nets = Networks()
        >>> nets.withoutIPs(startIP, endIP, exclude)
        >>> for net in nets:
        ...   print net
        192.168.4.0/29
        192.168.4.8/31
        192.168.4.12/30
        192.168.4.16/28
        192.168.4.32/27
        192.168.4.64/27
        192.168.4.96/29
        192.168.4.104/30
        192.168.4.108/31
        192.168.4.110
        192.168.4.112/28
        192.168.4.128/26
        192.168.4.192/27
        192.168.4.224/28
        192.168.4.240/29
        192.168.4.248/30
        192.168.4.252/31
        192.168.4.254

        # and one more time...
        >>> startIP = '192.168.4.0'
        >>> endIP = '192.168.5.255'
        >>> exclude = ['192.168.4.10', '192.168.4.11', '192.168.4.111',
        ...   '192.168.4.255', '192.168.5.5']
        >>> nets = Networks()
        >>> nets.withoutIPs(startIP, endIP, exclude)
        >>> for net in nets:
        ...   print net
        192.168.4.0/29
        192.168.4.8/31
        192.168.4.12/30
        192.168.4.16/28
        192.168.4.32/27
        192.168.4.64/27
        192.168.4.96/29
        192.168.4.104/30
        192.168.4.108/31
        192.168.4.110
        192.168.4.112/28
        192.168.4.128/26
        192.168.4.192/27
        192.168.4.224/28
        192.168.4.240/29
        192.168.4.248/30
        192.168.4.252/31
        192.168.4.254
        192.168.5.0/30
        192.168.5.4
        192.168.5.6/31
        192.168.5.8/29
        192.168.5.16/28
        192.168.5.32/27
        192.168.5.64/26
        192.168.5.128/25

        # let's use sets for checking the results
        >>> all = set(utils.getIPs(startIP, endIP))
        >>> expected = all.difference(exclude)
        >>> obtained = []
        >>> for net in nets:
        ...   obtained.extend(net.getIPs())

        # if these aren't equal, then we have overlapping IP addresses, and
        # that's bad
        >>> len(obtained) == len(set(obtained))
        True

        # now let's check our result
        >>> set(obtained) == expected
        True
        >>> expected.symmetric_difference(obtained)
        set([])
        """
        current = startIP
        while ipmath.octets2int(current) < ipmath.octets2int(endIP):
            if current in listOfIPs:
                current = ipmath.incrementIP(current)
                continue
            cidr = getLargestBlock(current, listOfIPs)
            if cidr:
                self.append(cidr)
                ip = cidr.getHostRange()[(-1)].getIP()
                current = ipmath.incrementIP(ip)
            else:
                self.assembleBlocks(current, endIP)
                current = endIP

    def fromIPs(self, listOfIPs):
        """
        Build a collection of networks that include only the IP addresses that
        are given.

        >>> ips = ['192.168.4.%s' % x for x in xrange(0,256) if x != 111]
        >>> len(ips)
        255
        >>> nets = Networks()
        >>> nets.fromIPs(ips)
        >>> for net in nets:
        ...   print net
        192.168.4.0/26
        192.168.4.64/27
        192.168.4.96/29
        192.168.4.104/30
        192.168.4.108/31
        192.168.4.110
        192.168.4.112/28
        192.168.4.128/25
        """
        startIP = listOfIPs[0]
        endIP = listOfIPs[(-1)]
        all = set(utils.getIPs(startIP, endIP))
        excluded = list(all.symmetric_difference(listOfIPs))
        self.withoutIPs(startIP, endIP, excluded)


def getDirection(srcCIDRObj, dstCIDRObj, insideNets):
    """
    This is a utility function for determining whether the communication
    between two given IPs is "out-bound" or "in-bound". The idea is that
    we are viewing this from the perspective of a router and one or more
    intneral networks. If the traffic crosses the router, we look at it
    and will get a string value of either "inbound" or "outbound". If
    the traffic doesn't cross our "router" (i.e., if the source and
    destination IPs are either both in the internet networks or both
    not in the internal networks) then we get nothing returned.

    # Setup some networks
    >>> inside_block1 = CIDR('192.168.4.0/24')
    >>> inside_block2 = CIDR('172.16.0.0/16')
    >>> inside_block3 = CIDR('10.0.0.0/8')
    >>> insideNets = Networks([inside_block1, inside_block2, inside_block3])

    # Define some hosts
    >>> laptop = CIDR('192.168.4.100')
    >>> laptop in insideNets
    True
    >>> webserver = CIDR('10.2.5.10')
    >>> webserver in insideNets
    True
    >>> fileserver = CIDR('172.16.9.50')
    >>> fileserver in insideNets
    True
    >>> googleWWW = CIDR('64.233.167.147')
    >>> googleWWW in insideNets
    False
    >>> yahooMail = CIDR('216.136.224.155')
    >>> yahooMail in insideNets
    False

    >>> getDirection(laptop, webserver, insideNets)
    >>> getDirection(fileserver, webserver, insideNets)
    >>> getDirection(laptop, yahooMail, insideNets)
    'outbound'
    >>> getDirection(fileserver, googleWWW, insideNets)
    'outbound'
    >>> getDirection(webserver, googleWWW, insideNets)
    'outbound'
    >>> getDirection(googleWWW, webserver, insideNets)
    'inbound'
    >>> getDirection(yahooMail, laptop, insideNets)
    'inbound'
    """
    if dstCIDRObj in insideNets and srcCIDRObj not in insideNets:
        return 'inbound'
    elif srcCIDRObj in insideNets and dstCIDRObj not in insideNets:
        return 'outbound'


def _test():
    import sys, doctest
    if len(sys.argv) > 1:
        possibleObject = sys.argv[(-1)]
        if possibleObject.split('.')[0] in globals().keys():
            return doctest.run_docstring_examples(eval(possibleObject), globals(), name=possibleObject)
    return doctest.testmod()


if __name__ == '__main__':
    _test()