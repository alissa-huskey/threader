"""Discord bot"""

import discord
import os
from sys import stderr
from datetime import datetime
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
        now = datetime.now(self.tz).strftime("%m-%d-%Y")

        if content.startswith("!thread"):
            # await message.channel.send(f":robot: :link: {now}")

            # requires discord.py version >1.7.3
            # (master as of 10/10/2021)
            await message.channel.create_thread(
                name=f"{now} Live Share Links",
                message=message,
            )
            return

def main():
    """Start the API client."""
    api = Client()
    api.run(api.token)

if __name__ == "__main__":
    main()

