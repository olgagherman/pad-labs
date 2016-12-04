#!/usr/bin/env python3.5
import asyncio
import logging.config

from server import ServerNode
from core import settings


logging.config.dictConfig(settings.LOGGING_CONFIG)


if __name__ == "__main__":
    node = ServerNode(
        asyncio.get_event_loop(),
        udp_group_address=settings.UDP_GROUP_ADDRESS,
        udp_group_port=settings.UDP_GROUP_PORT,
        **settings.SERVER_CONFIG[1],
    )
    node.run()
