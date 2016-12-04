#!/usr/bin/env python3.5
import asyncio
import logging

from client import Client
from core.settings import LOGGING_CONFIG


logging.config.dictConfig(LOGGING_CONFIG)


if __name__ == "__main__":
    client = Client(asyncio.get_event_loop())
    client.run()
