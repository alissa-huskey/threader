"""Discord bot"""

import asyncio
import os
from sys import stderr
from datetime import datetime

import discord
from discord.enums import ChannelType
import pytz

VERBOSE = True

def info(*args, div=False):
    """Print an info message."""
    if not VERBOSE:
        return

    print(*args, file=stderr)

    if div:
        print("-"*40, file=stderr)


def error(*args):
    """Print an info message."""
    if not VERBOSE:
        return

    info("Error:", *args, div=True)
    quit(1)


class Client(discord.Client):
    """Discord API Client"""

    envvar = "BOT_TOKEN"

    def __init__(self, *args, **kwargs):
        self.token = os.environ.get(self.envvar)
        self.tz = pytz.timezone("US/Mountain")

        if not self.token:
            error(f"{envvar} environment variable missing.", file=stderr)

        super().__init__(*args, **kwargs)

    async def on_ready(self):
        """Print debug info when client starts up."""
        info(f"Application ({self.user.id}) {self.user.name}")
        info("Ready.", div=True)

    async def on_message(self, message):
        """Create a thread if "!thread" message is received"""
        info("Received message:", message.channel, message.content, div=True)

        content = message.content.strip()

        if content.startswith("!thread"):
            await self.make_thread(message.channel, "(Testing) Live Share Links", ":robot: :link:")

    async def make_thread(self, channel, title, message=None):
        """Create a public thread on channel that archives after 1 hour named
           with the current date and title. If message is present, post first
           as first message to thread.

           Parameters
           -----------
           channel: (int, discord.channels.Channel)
                Channel or channel id
           title: (str)
                Title of thread
           message: (str, default=None)
                Text of message to post.
           """
        if isinstance(channel, int):
            channel = self.get_channel(channel)

        now = datetime.now(self.tz)
        nice_date = now.strftime("%m-%d-%Y (%s)")
        date = now.strftime("%F")

        # requires discord.py version >1.7.3
        # (master as of 10/10/2021)
        await channel.create_thread(
            name=f"{nice_date} {title}",
            type=ChannelType.public_thread,
            auto_archive_duration=60,
        )

        if message:
            thread = channel.threads[-1]
            await thread.send(message)


def main():
    """Start the API client."""
    api = Client()
    api.run(api.token)

if __name__ == "__main__":
    main()

