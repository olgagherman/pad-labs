#!/usr/bin/env python3.5
import asyncio
from client import Client


if __name__ == "__main__":
    client = Client(asyncio.get_event_loop())
    client.run()
