import urllib.request as web
import ctypes as c 
import praw
import os
import shutil
import os.path
import sys
import time
import discord
import io
import aiohttp

class DiscordRedditScraper:
    """
    Reddit Scraper Object
    """

    def __init__(self, ctx, height=c.windll.user32.GetSystemMetrics(1),
                            width=c.windll.user32.GetSystemMetrics(0),
                            client_id='', client_secret='', user_agent=''):
        self.ctx = ctx
        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height
        self.MAX_FILENAME_LENGTH = 170
        self.MIN_FILE_SIZE = 300
        self.__reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

    @staticmethod
    def __is_digit(s):
        """
        Returns true if argument is of the float class, false otherwise
        :return: true if argument can be casted to a float, false otherwise
        """
        try:
            float(s)
            return True
        except ValueError:
            return False

    def __get_resolution(self, title):
        """
        Returns the resolution embedded in a reddit post title of the form: (width, height)
        :param title: Title string of the reddit post
        :return: Resolution of the image in the post as specified by the OP
        """
        res = ''
        for char in filter(lambda char: char in title, ['[', ']', '(', ')']):
            title = title.replace(char, '')
        title = list(title)

        for char in title:
            if self.__is_digit(char):
                res += 'x' + char if len(res) == 4 else char
        res = res.split('x')
        if len(res) < 2:
            return 0, 0

        width, height = res[0], res[1]
        if len(width) < 4 or len(height) < 4:
            width, height = 0, 0
        return int(width), int(height)

    def __compatible(self, post):
        """
        Returns true if the resolution in the post title is at least 1920x1080 and if width > height
        returns false otherwise
        :param post:
        :return:
        """
        width, height = self.__get_resolution(post.title)
        good_domain = "i.redd.it" in post.domain or "imgur" in post.domain
        correct_dimensions = width >= self.SCREEN_WIDTH and width > height >= self.SCREEN_HEIGHT
        return correct_dimensions and good_domain

    @staticmethod
    def __cleanup_title(string):
        """
        Removes bad characters from and appends '.jpg' to end of string
        :param string: string to be modified
        :return: modified string
        """
        chars = ['/', '\\', ':', '*', '?', '<', '>', '"', '|']
        for char in filter(lambda char: char in string, chars):
            string = string.replace(char, '')
        return string + '.jpg'

    @staticmethod
    def __cleanup_url(url):
        """
        Appends '.jpg' the image url if it isn't already present, returns a new string
        :param url: url to modify
        :return: modified url
        """
        ret_str = url
        url = url.split('.')
        if url[-1] != 'jpg':
            ret_str += '.jpg'
        return ret_str

    async def scrape(self, subreddits, _max):
        """
        Scraping routine
        """
        subs = [sub + 'porn' if 'porn' not in sub else sub
                for sub in subreddits.replace(' ', '').split(',')]

        await self.ctx.send('Reading reddit...')
        compatible_posts = [post for sub in subs for post in self.__reddit.subreddit(sub).hot(limit=int(_max))
                            if self.__compatible(post)]

        if len(compatible_posts) == 0:
            await self.ctx.send('No compatible images found')
        else:
            await self.ctx.send('{} compatible images detected'.format(str(len(compatible_posts))))
            await self.ctx.send('Collecting images...\n')

            async with aiohttp.ClientSession() as session:
                for idx, post in enumerate(compatible_posts):
                    async with session.get(self.__cleanup_url(post.url)) as resp:
                        if resp.status == 200:
                            data = io.BytesIO(await resp.read())
                            await self.ctx.send(file=discord.File(data, self.__cleanup_url(str(idx+1))))
                                


