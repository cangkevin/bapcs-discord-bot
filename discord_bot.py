import discord
import praw_client

import logging
import multiprocessing as mp
import asyncio

from decouple import config

logging.basicConfig(level=logging.INFO)

client = discord.Client()

async def check_queue(q):
    await client.wait_until_ready()
    channel = discord.Object(id=config('CHANNEL_ID'))
    while not client.is_closed:
        if not q.empty():
            try:
                submission = q.get_nowait()
                em = discord.Embed(title=submission['title'],
                                    url=submission['url'],
                                    description=submission['reddit_url'])
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