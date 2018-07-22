import unittest
import time
from bapcs_bot import BAPCSWatcher

class TestDiscordBot(unittest.TestCase):
    def setUp(self):
        self.bot = BAPCSWatcher()

    def test_embed_color_with_no_flair(self):
        color = self.bot._embed_color(None)
        self.assertEqual(color, self.bot._color['MAGENTA'], 
                        'wrong embed color for flair: None')

    def test_embed_color_with_unknown_flair(self):
        color = self.bot._embed_color('mic')
        self.assertEqual(color, self.bot._color['MAGENTA'], 
                        'wrong embed color for unknown flair')

    def test_embed_color_with_known_flairs(self):
        color = self.bot._embed_color('gpu')
        self.assertEqual(color, self.bot._color['BLUE'], 
                        'wrong embed color for flair: gpu')

    def test_reddit_stream_in_seperate_process(self):
        self.assertEqual(self.bot._reddit_stream.is_alive(), False)
        self.bot._reddit_stream.start()
        self.assertEqual(self.bot._reddit_stream.is_alive(), True, 
                        'reddit client not running in a separate process')
        self.bot._reddit_stream.terminate()
        time.sleep(0.1)
        self.assertEqual(self.bot._reddit_stream.is_alive(), False)
