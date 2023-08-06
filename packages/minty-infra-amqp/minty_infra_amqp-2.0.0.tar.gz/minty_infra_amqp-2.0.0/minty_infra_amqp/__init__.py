# SPDX-FileCopyrightText: Mintlab B.V.
#
# SPDX-License-Identifier: EUPL-1.2

__version__ = "2.0.0"

import amqpstorm  # type: ignore
import threading
from amqpstorm import AMQPChannelError, AMQPConnectionError
from minty import Base
from typing import Any, Dict, Optional


class AMQPInfrastructure(Base):
    __slots__ = ["cache_lock", "connection", "channels"]

    def __init__(self) -> None:
        """Initialize the AMQP infrastructure"""
        self.cache_lock = threading.Lock()
        self.channels: Dict[str, amqpstorm.Channel] = {}
        self.connection: Optional[amqpstorm.Connection] = None

    def __call__(self, config: Dict[str, Any]) -> amqpstorm.Channel:
        """Create a new AMQP connection using the specified configuration

        :param config: Configuration to read amqp:// URL from
        :type config: dict
        :return: A handle for a channel on a connection to an AMQP server.
        :rtype: amqpstorm.Connection
        """

        rmq_url = config["amqp"]["url"]

        with self.cache_lock:
            try:
                channel = self.channels[rmq_url]
                channel.check_for_errors()
            except (KeyError, AMQPConnectionError):
                # No connection/channel has been made (yet)
                channel = self._create_connection_and_channel(rmq_url)
            except AMQPChannelError:
                # Still connected, but channel somehow invalid
                if not self.connection:  # pragma: no cover
                    # Should be impossible, given how amqpstorm works
                    raise
                channel = self.connection.channel()
                self.channels[rmq_url] = channel

        return channel

    def _create_connection_and_channel(
        self, rmq_url: str
    ) -> amqpstorm.Channel:
        """Create connection and channel.

        :param rmq_url:  amqp:// URL
        :type rmq_url: str
        :return: channel
        :rtype: amqpstorm.Channel
        """
        timer = self.statsd.get_timer("amqp_connect_duration")
        with timer.time():
            self.connection = amqpstorm.UriConnection(rmq_url)
        self.channels[rmq_url] = self.connection.channel()

        self.statsd.get_counter("amqp_connect_number")

        return self.channels[rmq_url]
