import discord
import praw_client

import logging
import multiprocessing as mp
import asyncio

from decouple import config

logging.basicConfig(level=logging.INFO)

client = discord.Client()
colors = {
    'BLUE': discord.Color(0x0066ff),
    'RED': discord.Color(0xcc0000),
    'ORANGE': discord.Color(0xffcc66),
    'GREEN': discord.Color(0x00ff33),
    'WHITE': discord.Color(0xffffff),
    'MAGENTA': discord.Color(0x9966ff),
    'YELLOW': discord.Color(0xffff66)
}

def embed_color(flair):
    if flair is None:
        return colors['MAGENTA']

    flair_text = flair.lower()
    return {
        'case': colors['BLUE'],
        'cooler': colors['BLUE'],
        'fan': colors['ORANGE'],
        'hdd': colors['BLUE'],
        'keyboard': colors['GREEN'],
        'mouse': colors['GREEN'],
        'ram': colors['BLUE'],
        'mobo': colors['BLUE'],
        'prebuilt': colors['WHITE'],
        'controller': colors['GREEN'],
        'cpu': colors['BLUE'],
        'gpu': colors['BLUE'],
        'headphones': colors['GREEN'],
        'monitor': colors['RED'],
        'psu': colors['BLUE'],
        'ssd': colors['BLUE'],
        'meta': colors['YELLOW'],
    }.get(flair_text, colors['MAGENTA'])


async def check_queue(q):
    await client.wait_until_ready()
    channel = discord.Object(id=config('CHANNEL_ID'))
    while not client.is_closed:
        if not q.empty():
            try:
                submission = q.get_nowait()
                em = discord.Embed(title=submission['title'],
                                    url=submission['url'],
                                    description=submission['reddit_url'],
                                    colour=embed_color(submission['type']))
                await client.send_message(channel, embed=em)
            except Exception as e: # if queue is empty
                pass
        await asyncio.sleep(10) # check every 10 seconds


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # TODO: implement filtering functionality for submission flairs


@client.event
async def on_ready():
    print('Logged in as ', client.user.name)
    print('------')


if __name__ == '__main__':
    mp.set_start_method('spawn')
    q = mp.Queue()
    p =  mp.Process(target=praw_client.start, args=(q,))
    p.start()
    
    client.loop.create_task(check_queue(q))
    client.run(config('BOT_TOKEN'))
