# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jraviles/Projects/src/prometheus_speedtest/prometheus_speedtest/prometheus_speedtest.py
# Compiled at: 2020-02-21 12:52:27
# Size of source mod 2**32: 4689 bytes
__doc__ = 'Instrument speedtest.net speedtests from Prometheus.'
from http import server
from urllib.parse import urlparse
import os
from absl import app
from absl import flags
from absl import logging
from prometheus_client import core
import prometheus_client, speedtest
from prometheus_speedtest import version
flags.DEFINE_string('address', '0.0.0.0', 'address to listen on')
flags.DEFINE_integer('port', 9516, 'port to listen on')
flags.DEFINE_boolean('version', False, 'show version')
FLAGS = flags.FLAGS

class PrometheusSpeedtest:
    """PrometheusSpeedtest"""

    def __init__(self, source_address=None, timeout=10):
        """Instantiates a PrometheusSpeedtest object.

        Args:
            source_address: str - optional network address to bind to.
                e.g. 192.168.1.1.
            timeout: int - optional timeout for speedtest in seconds.
        """
        self._source_address = source_address
        self._timeout = timeout

    def test(self):
        """Performs speedtest, returns results.

        Returns:
            speedtest.SpeedtestResults object.
        """
        logging.info('Performing Speedtest')
        client = speedtest.Speedtest(source_address=(self._source_address), timeout=(self._timeout))
        client.get_best_server()
        client.download()
        client.upload()
        logging.info(client.results)
        return client.results


class SpeedtestCollector:
    """SpeedtestCollector"""

    def __init__(self, tester=None):
        """Instantiates a SpeedtestCollector object.

        Args:
            tester: An instantiated PrometheusSpeedtest object for testing.
        """
        self._tester = tester if tester else PrometheusSpeedtest()

    def collect(self):
        """Performs a Speedtests and yields metrics.

        Yields:
            core.Metric objects.
        """
        results = self._tester.test()
        download_speed = core.GaugeMetricFamily('download_speed_bps', 'Download speed (bit/s)')
        download_speed.add_metric(labels=[], value=(results.download))
        yield download_speed
        upload_speed = core.GaugeMetricFamily('upload_speed_bps', 'Upload speed (bit/s)')
        upload_speed.add_metric(labels=[], value=(results.upload))
        yield upload_speed
        ping = core.GaugeMetricFamily('ping_ms', 'Latency (ms)')
        ping.add_metric(labels=[], value=(results.ping))
        yield ping
        bytes_received = core.GaugeMetricFamily('bytes_received', 'Bytes received during test')
        bytes_received.add_metric(labels=[], value=(results.bytes_received))
        yield bytes_received
        bytes_sent = core.GaugeMetricFamily('bytes_sent', 'Bytes sent during test')
        bytes_sent.add_metric(labels=[], value=(results.bytes_sent))
        yield bytes_sent


class SpeedtestMetricsHandler(server.SimpleHTTPRequestHandler, prometheus_client.MetricsHandler):
    """SpeedtestMetricsHandler"""

    def __init__(self, *args, **kwargs):
        static_directory = os.path.join(os.path.dirname(__file__), 'static')
        (super(SpeedtestMetricsHandler, self).__init__)(args, directory=static_directory, **kwargs)

    def do_GET(self):
        """Handles HTTP GET requests.

        Requests to '/probe' are handled by prometheus_client.MetricsHandler,
        other requests serve static HTML.
        """
        path = urlparse(self.path).path
        if path == '/probe':
            prometheus_client.MetricsHandler.do_GET(self)
        else:
            server.SimpleHTTPRequestHandler.do_GET(self)


def main(argv):
    """Entry point for prometheus_speedtest.py."""
    del argv
    if FLAGS.version:
        print('prometheus_speedtest v%s' % version.VERSION)
        return
    registry = core.CollectorRegistry(auto_describe=False)
    registry.register(SpeedtestCollector())
    metrics_handler = SpeedtestMetricsHandler.factory(registry)
    http = server.ThreadingHTTPServer((FLAGS.address, FLAGS.port), metrics_handler)
    logging.info('Starting HTTP server listening on %s:%s', FLAGS.address, FLAGS.port)
    http.serve_forever()


def init():
    """Initializes the prometheus_speedtest cli."""
    app.run(main)


if __name__ == '__main__':
    init()