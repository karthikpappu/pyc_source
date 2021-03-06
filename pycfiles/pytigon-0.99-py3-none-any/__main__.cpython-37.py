# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-76h68wr6/websockets/websockets/__main__.py
# Compiled at: 2020-04-19 04:11:09
# Size of source mod 2**32: 6420 bytes
import argparse, asyncio, os, signal, sys, threading
from typing import Any, Set
from .client import connect
from .exceptions import ConnectionClosed, format_close
if sys.platform == 'win32':

    def win_enable_vt100() -> None:
        """
        Enable VT-100 for console output on Windows.

        See also https://bugs.python.org/issue29059.

        """
        import ctypes
        STD_OUTPUT_HANDLE = ctypes.c_uint(-11)
        INVALID_HANDLE_VALUE = ctypes.c_uint(-1)
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 4
        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        if handle == INVALID_HANDLE_VALUE:
            raise RuntimeError('unable to obtain stdout handle')
        cur_mode = ctypes.c_uint()
        if ctypes.windll.kernel32.GetConsoleMode(handle, ctypes.byref(cur_mode)) == 0:
            raise RuntimeError('unable to query current console mode')
        py_int_mode = int.from_bytes(cur_mode, sys.byteorder)
        new_mode = ctypes.c_uint(py_int_mode | ENABLE_VIRTUAL_TERMINAL_PROCESSING)
        if ctypes.windll.kernel32.SetConsoleMode(handle, new_mode) == 0:
            raise RuntimeError('unable to set console mode')


def exit_from_event_loop_thread(loop: asyncio.AbstractEventLoop, stop: 'asyncio.Future[None]') -> None:
    loop.stop()
    if not stop.done():
        try:
            ctrl_c = signal.CTRL_C_EVENT
        except AttributeError:
            ctrl_c = signal.SIGINT

        os.kill(os.getpid(), ctrl_c)


def print_during_input(string: str) -> None:
    sys.stdout.write(f"\x1b7\n\x1b[A\x1b[L{string}\n\x1b8\x1b[B")
    sys.stdout.flush()


def print_over_input(string: str) -> None:
    sys.stdout.write(f"\r\x1b[K{string}\n")
    sys.stdout.flush()


async def run_client(uri: str, loop: asyncio.AbstractEventLoop, inputs: 'asyncio.Queue[str]', stop: 'asyncio.Future[None]') -> None:
    try:
        websocket = await connect(uri)
    except Exception as exc:
        try:
            print_over_input(f"Failed to connect to {uri}: {exc}.")
            exit_from_event_loop_thread(loop, stop)
            return
        finally:
            exc = None
            del exc

    else:
        print_during_input(f"Connected to {uri}.")
    try:
        while 1:
            incoming = asyncio.ensure_future(websocket.recv())
            outgoing = asyncio.ensure_future(inputs.get())
            done, pending = await asyncio.wait([
             incoming, outgoing, stop],
              return_when=(asyncio.FIRST_COMPLETED))
            if incoming in pending:
                incoming.cancel()
            if outgoing in pending:
                outgoing.cancel()
            if incoming in done:
                try:
                    message = incoming.result()
                except ConnectionClosed:
                    break
                else:
                    if isinstance(message, str):
                        print_during_input('< ' + message)
                    else:
                        print_during_input('< (binary) ' + message.hex())
            if outgoing in done:
                message = outgoing.result()
                await websocket.send(message)
            if stop in done:
                break

    finally:
        await websocket.close()
        close_status = format_close(websocket.close_code, websocket.close_reason)
        print_over_input(f"Connection closed: {close_status}.")
        exit_from_event_loop_thread(loop, stop)


def main() -> None:
    if sys.platform == 'win32':
        try:
            win_enable_vt100()
        except RuntimeError as exc:
            try:
                sys.stderr.write(f"Unable to set terminal to VT100 mode. This is only supported since Win10 anniversary update. Expect weird symbols on the terminal.\nError: {exc}\n")
                sys.stderr.flush()
            finally:
                exc = None
                del exc

    try:
        import readline
    except ImportError:
        pass

    parser = argparse.ArgumentParser(prog='python -m websockets',
      description='Interactive WebSocket client.',
      add_help=False)
    parser.add_argument('uri', metavar='<uri>')
    args = parser.parse_args()
    loop = asyncio.new_event_loop()
    inputs = asyncio.Queue(loop=loop)
    stop = loop.create_future()
    asyncio.ensure_future((run_client(args.uri, loop, inputs, stop)), loop=loop)
    thread = threading.Thread(target=(loop.run_forever))
    thread.start()
    try:
        while True:
            message = input('> ')
            loop.call_soon_threadsafe(inputs.put_nowait, message)

    except (KeyboardInterrupt, EOFError):
        loop.call_soon_threadsafe(stop.set_result, None)

    thread.join()


if __name__ == '__main__':
    main()