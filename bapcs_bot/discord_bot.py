import discord
# HACK: use absolute import when running this script, relative for testing
if __name__ == '__main__':
    import praw_client
else:
    from . import praw_client
import logging
import multiprocessing as mp
import asyncio
from simple_settings import settings

logging.basicConfig(level=logging.INFO)

class BAPCSWatcher:
    def __init__(self):
        self._queue = mp.Queue()
        self._client = discord.Client()
        self._color = {
            'BLUE': discord.Color(0x0066ff),
            'RED': discord.Color(0xcc0000),
            'ORANGE': discord.Color(0xffcc66),
            'GREEN': discord.Color(0x00ff33),
            'WHITE': discord.Color(0xffffff),
            'MAGENTA': discord.Color(0x9966ff),
            'YELLOW': discord.Color(0xffff66)
        }
        self._reddit_stream = mp.Process(target=praw_client.start,args=(self._queue,))
        self._client.loop.create_task(self._check_queue(self._queue))

    def run(self):
        self._reddit_stream.start()
        self._client.run(settings.BOT_TOKEN)

    def _embed_color(self, flair):
        if flair is None:
            return self._color['MAGENTA']

        flair_text = flair.lower()
        return {
            'case': self._color['BLUE'],
            'cooler': self._color['BLUE'],
            'fan': self._color['ORANGE'],
            'hdd': self._color['BLUE'],
            'keyboard': self._color['GREEN'],
            'mouse': self._color['GREEN'],
            'ram': self._color['BLUE'],
            'mobo': self._color['BLUE'],
            'prebuilt': self._color['WHITE'],
            'controller': self._color['GREEN'],
            'cpu': self._color['BLUE'],
            'gpu': self._color['BLUE'],
            'headphones': self._color['GREEN'],
            'monitor': self._color['RED'],
            'psu': self._color['BLUE'],
            'ssd': self._color['BLUE'],
            'meta': self._color['YELLOW'],
        }.get(flair_text, self._color['MAGENTA'])

    async def _check_queue(self, q):
        await self._client.wait_until_ready()
        channel = discord.Object(id=settings.CHANNEL_ID)
        while not self._client.is_closed:
            await asyncio.sleep(5) # check every 5 seconds
            if q.empty():
                continue
            submission = q.get()
            em = discord.Embed(title=submission['title'],
                                url=submission['url'],
                                description=submission['reddit_url'],
                                colour=self._embed_color(submission['type']))
            await self._client.send_message(channel,embed=em)

bot = BAPCSWatcher()

@bot._client.event
async def on_ready():
    print('Logged in as ', bot._client.user.name)
    print('------')

@bot._client.event
async def on_message(message):
    if message.author == bot._client.user:
        return

    if message.content.startswith('!hello'):
        msg = 'Hello {0.author.mention}'.format(message)
        await bot._client.send_message(message.channel, msg)

if __name__ == '__main__':
    bot.run()
