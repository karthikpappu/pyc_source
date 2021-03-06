# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/websockets/websockets/extensions/permessage_deflate.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 21730 bytes
"""
:mod:`websockets.extensions.permessage_deflate` implements the Compression
Extensions for WebSocket as specified in :rfc:`7692`.

"""
import zlib
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union
from ..exceptions import DuplicateParameter, InvalidParameterName, InvalidParameterValue, NegotiationError, PayloadTooBig
from ..framing import CTRL_OPCODES, OP_CONT, Frame
from ..typing import ExtensionName, ExtensionParameter
from .base import ClientExtensionFactory, Extension, ServerExtensionFactory
__all__ = [
 'PerMessageDeflate',
 'ClientPerMessageDeflateFactory',
 'ServerPerMessageDeflateFactory']
_EMPTY_UNCOMPRESSED_BLOCK = b'\x00\x00\xff\xff'
_MAX_WINDOW_BITS_VALUES = [str(bits) for bits in range(8, 16)]

class PerMessageDeflate(Extension):
    __doc__ = '\n    Per-Message Deflate extension.\n\n    '
    name = ExtensionName('permessage-deflate')

    def __init__(self, remote_no_context_takeover: bool, local_no_context_takeover: bool, remote_max_window_bits: int, local_max_window_bits: int, compress_settings: Optional[Dict[(Any, Any)]]=None) -> None:
        """
        Configure the Per-Message Deflate extension.

        """
        if compress_settings is None:
            compress_settings = {}
        else:
            if not remote_no_context_takeover in (False, True):
                raise AssertionError
            else:
                if not local_no_context_takeover in (False, True):
                    raise AssertionError
                else:
                    assert 8 <= remote_max_window_bits <= 15
                    assert 8 <= local_max_window_bits <= 15
                assert 'wbits' not in compress_settings
                self.remote_no_context_takeover = remote_no_context_takeover
                self.local_no_context_takeover = local_no_context_takeover
                self.remote_max_window_bits = remote_max_window_bits
                self.local_max_window_bits = local_max_window_bits
                self.compress_settings = compress_settings
                self.decoder = self.remote_no_context_takeover or zlib.decompressobj(wbits=(-self.remote_max_window_bits))
            self.encoder = self.local_no_context_takeover or (zlib.compressobj)(wbits=-self.local_max_window_bits, **self.compress_settings)
        self.decode_cont_data = False

    def __repr__(self) -> str:
        return f"PerMessageDeflate(remote_no_context_takeover={self.remote_no_context_takeover}, local_no_context_takeover={self.local_no_context_takeover}, remote_max_window_bits={self.remote_max_window_bits}, local_max_window_bits={self.local_max_window_bits})"

    def decode(self, frame: Frame, *, max_size: Optional[int]=None) -> Frame:
        """
        Decode an incoming frame.

        """
        if frame.opcode in CTRL_OPCODES:
            return frame
        elif frame.opcode == OP_CONT and not self.decode_cont_data:
            return frame
            if frame.fin:
                self.decode_cont_data = False
            else:
                if not frame.rsv1:
                    return frame
                if not frame.fin:
                    self.decode_cont_data = True
                if self.remote_no_context_takeover:
                    self.decoder = zlib.decompressobj(wbits=(-self.remote_max_window_bits))
            data = frame.data
            if frame.fin:
                data += _EMPTY_UNCOMPRESSED_BLOCK
            max_length = 0 if max_size is None else max_size
            data = self.decoder.decompress(data, max_length)
            if self.decoder.unconsumed_tail:
                raise PayloadTooBig(f"Uncompressed payload length exceeds size limit (? > {max_size} bytes)")
            if frame.fin and self.remote_no_context_takeover:
                del self.decoder
        return frame._replace(data=data, rsv1=False)

    def encode(self, frame: Frame) -> Frame:
        """
        Encode an outgoing frame.

        """
        if frame.opcode in CTRL_OPCODES:
            return frame
            if frame.opcode != OP_CONT:
                if self.local_no_context_takeover:
                    self.encoder = (zlib.compressobj)(wbits=-self.local_max_window_bits, **self.compress_settings)
        else:
            data = self.encoder.compress(frame.data) + self.encoder.flush(zlib.Z_SYNC_FLUSH)
            if frame.fin:
                if data.endswith(_EMPTY_UNCOMPRESSED_BLOCK):
                    data = data[:-4]
            if frame.fin and self.local_no_context_takeover:
                del self.encoder
        return frame._replace(data=data, rsv1=True)


def _build_parameters(server_no_context_takeover: bool, client_no_context_takeover: bool, server_max_window_bits: Optional[int], client_max_window_bits: Optional[Union[(int, bool)]]) -> List[ExtensionParameter]:
    """
    Build a list of ``(name, value)`` pairs for some compression parameters.

    """
    params = []
    if server_no_context_takeover:
        params.append(('server_no_context_takeover', None))
    else:
        if client_no_context_takeover:
            params.append(('client_no_context_takeover', None))
        if server_max_window_bits:
            params.append(('server_max_window_bits', str(server_max_window_bits)))
        if client_max_window_bits is True:
            params.append(('client_max_window_bits', None))
        else:
            if client_max_window_bits:
                params.append(('client_max_window_bits', str(client_max_window_bits)))
    return params


def _extract_parameters(params: Sequence[ExtensionParameter], *, is_server: bool) -> Tuple[(bool, bool, Optional[int], Optional[Union[(int, bool)]])]:
    """
    Extract compression parameters from a list of ``(name, value)`` pairs.

    If ``is_server`` is ``True``, ``client_max_window_bits`` may be provided
    without a value. This is only allow in handshake requests.

    """
    server_no_context_takeover = False
    client_no_context_takeover = False
    server_max_window_bits = None
    client_max_window_bits = None
    for name, value in params:
        if name == 'server_no_context_takeover':
            if server_no_context_takeover:
                raise DuplicateParameter(name)
            elif value is None:
                server_no_context_takeover = True
            else:
                raise InvalidParameterValue(name, value)
        elif name == 'client_no_context_takeover':
            if client_no_context_takeover:
                raise DuplicateParameter(name)
            elif value is None:
                client_no_context_takeover = True
            else:
                raise InvalidParameterValue(name, value)
        elif name == 'server_max_window_bits':
            if server_max_window_bits is not None:
                raise DuplicateParameter(name)
            elif value in _MAX_WINDOW_BITS_VALUES:
                server_max_window_bits = int(value)
            else:
                raise InvalidParameterValue(name, value)
        elif name == 'client_max_window_bits':
            if client_max_window_bits is not None:
                raise DuplicateParameter(name)
            if is_server and value is None:
                client_max_window_bits = True
            else:
                if value in _MAX_WINDOW_BITS_VALUES:
                    client_max_window_bits = int(value)
                else:
                    raise InvalidParameterValue(name, value)
        else:
            raise InvalidParameterName(name)

    return (server_no_context_takeover,
     client_no_context_takeover,
     server_max_window_bits,
     client_max_window_bits)


class ClientPerMessageDeflateFactory(ClientExtensionFactory):
    __doc__ = '\n    Client-side extension factory for the Per-Message Deflate extension.\n\n    Parameters behave as described in `section 7.1 of RFC 7692`_. Set them to\n    ``True`` to include them in the negotiation offer without a value or to an\n    integer value to include them with this value.\n\n    .. _section 7.1 of RFC 7692: https://tools.ietf.org/html/rfc7692#section-7.1\n\n    :param server_no_context_takeover: defaults to ``False``\n    :param client_no_context_takeover: defaults to ``False``\n    :param server_max_window_bits: optional, defaults to ``None``\n    :param client_max_window_bits: optional, defaults to ``None``\n    :param compress_settings: optional, keyword arguments for\n        :func:`zlib.compressobj`, excluding ``wbits``\n\n    '
    name = ExtensionName('permessage-deflate')

    def __init__(self, server_no_context_takeover: bool=False, client_no_context_takeover: bool=False, server_max_window_bits: Optional[int]=None, client_max_window_bits: Optional[Union[(int, bool)]]=None, compress_settings: Optional[Dict[(str, Any)]]=None) -> None:
        """
        Configure the Per-Message Deflate extension factory.

        """
        if not server_max_window_bits is None:
            if not 8 <= server_max_window_bits <= 15:
                raise ValueError('server_max_window_bits must be between 8 and 15')
        else:
            if not client_max_window_bits is None:
                if not client_max_window_bits is True:
                    if not 8 <= client_max_window_bits <= 15:
                        raise ValueError('client_max_window_bits must be between 8 and 15')
            if compress_settings is not None and 'wbits' in compress_settings:
                raise ValueError('compress_settings must not include wbits, set client_max_window_bits instead')
        self.server_no_context_takeover = server_no_context_takeover
        self.client_no_context_takeover = client_no_context_takeover
        self.server_max_window_bits = server_max_window_bits
        self.client_max_window_bits = client_max_window_bits
        self.compress_settings = compress_settings

    def get_request_params(self) -> List[ExtensionParameter]:
        """
        Build request parameters.

        """
        return _build_parameters(self.server_no_context_takeover, self.client_no_context_takeover, self.server_max_window_bits, self.client_max_window_bits)

    def process_response_params(self, params: Sequence[ExtensionParameter], accepted_extensions: Sequence['Extension']) -> PerMessageDeflate:
        """
        Process response parameters.

        Return an extension instance.

        """
        if any((other.name == self.name for other in accepted_extensions)):
            raise NegotiationError(f"received duplicate {self.name}")
        else:
            server_no_context_takeover, client_no_context_takeover, server_max_window_bits, client_max_window_bits = _extract_parameters(params, is_server=False)
            if self.server_no_context_takeover:
                if not server_no_context_takeover:
                    raise NegotiationError('expected server_no_context_takeover')
            if self.client_no_context_takeover:
                client_no_context_takeover = client_no_context_takeover or True
        if self.server_max_window_bits is None:
            pass
        elif server_max_window_bits is None:
            raise NegotiationError('expected server_max_window_bits')
        else:
            if server_max_window_bits > self.server_max_window_bits:
                raise NegotiationError('unsupported server_max_window_bits')
            elif self.client_max_window_bits is None:
                if client_max_window_bits is not None:
                    raise NegotiationError('unexpected client_max_window_bits')
            elif self.client_max_window_bits is True:
                pass
            elif client_max_window_bits is None:
                client_max_window_bits = self.client_max_window_bits
            else:
                if client_max_window_bits > self.client_max_window_bits:
                    raise NegotiationError('unsupported client_max_window_bits')
            return PerMessageDeflate(server_no_context_takeover, client_no_context_takeover, server_max_window_bits or 15, client_max_window_bits or 15, self.compress_settings)


class ServerPerMessageDeflateFactory(ServerExtensionFactory):
    __doc__ = '\n    Server-side extension factory for the Per-Message Deflate extension.\n\n    Parameters behave as described in `section 7.1 of RFC 7692`_. Set them to\n    ``True`` to include them in the negotiation offer without a value or to an\n    integer value to include them with this value.\n\n    .. _section 7.1 of RFC 7692: https://tools.ietf.org/html/rfc7692#section-7.1\n\n    :param server_no_context_takeover: defaults to ``False``\n    :param client_no_context_takeover: defaults to ``False``\n    :param server_max_window_bits: optional, defaults to ``None``\n    :param client_max_window_bits: optional, defaults to ``None``\n    :param compress_settings: optional, keyword arguments for\n        :func:`zlib.compressobj`, excluding ``wbits``\n\n    '
    name = ExtensionName('permessage-deflate')

    def __init__(self, server_no_context_takeover: bool=False, client_no_context_takeover: bool=False, server_max_window_bits: Optional[int]=None, client_max_window_bits: Optional[int]=None, compress_settings: Optional[Dict[(str, Any)]]=None) -> None:
        """
        Configure the Per-Message Deflate extension factory.

        """
        if not server_max_window_bits is None:
            if not 8 <= server_max_window_bits <= 15:
                raise ValueError('server_max_window_bits must be between 8 and 15')
        else:
            if not client_max_window_bits is None:
                if not 8 <= client_max_window_bits <= 15:
                    raise ValueError('client_max_window_bits must be between 8 and 15')
            if compress_settings is not None and 'wbits' in compress_settings:
                raise ValueError('compress_settings must not include wbits, set server_max_window_bits instead')
        self.server_no_context_takeover = server_no_context_takeover
        self.client_no_context_takeover = client_no_context_takeover
        self.server_max_window_bits = server_max_window_bits
        self.client_max_window_bits = client_max_window_bits
        self.compress_settings = compress_settings

    def process_request_params(self, params: Sequence[ExtensionParameter], accepted_extensions: Sequence['Extension']) -> Tuple[(List[ExtensionParameter], PerMessageDeflate)]:
        """
        Process request parameters.

        Return response params and an extension instance.

        """
        if any((other.name == self.name for other in accepted_extensions)):
            raise NegotiationError(f"skipped duplicate {self.name}")
        else:
            server_no_context_takeover, client_no_context_takeover, server_max_window_bits, client_max_window_bits = _extract_parameters(params, is_server=True)
            if self.server_no_context_takeover:
                if not server_no_context_takeover:
                    server_no_context_takeover = True
            if self.client_no_context_takeover:
                client_no_context_takeover = client_no_context_takeover or True
        if self.server_max_window_bits is None:
            pass
        elif server_max_window_bits is None:
            server_max_window_bits = self.server_max_window_bits
        else:
            if server_max_window_bits > self.server_max_window_bits:
                server_max_window_bits = self.server_max_window_bits
            elif self.client_max_window_bits is None:
                if client_max_window_bits is True:
                    client_max_window_bits = self.client_max_window_bits
            elif client_max_window_bits is None:
                raise NegotiationError('required client_max_window_bits')
            else:
                if client_max_window_bits is True:
                    client_max_window_bits = self.client_max_window_bits
                else:
                    if self.client_max_window_bits < client_max_window_bits:
                        client_max_window_bits = self.client_max_window_bits
            return (
             _build_parameters(server_no_context_takeover, client_no_context_takeover, server_max_window_bits, client_max_window_bits),
             PerMessageDeflate(client_no_context_takeover, server_no_context_takeover, client_max_window_bits or 15, server_max_window_bits or 15, self.compress_settings))