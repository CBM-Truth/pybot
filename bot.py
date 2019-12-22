import discord
from discord.ext import commands
from scraper import DiscordRedditScraper
from token import TOKEN

bot = commands.Bot(command_prefix='!')

@bot.command()
async def test(ctx, arg):
    print('processing command...')
    print(arg)
    await ctx.send('Received command argument: {}'.format(arg))

    if not arg:
        await ctx.send('You must supply an argument to the "test" command')

    print('Called test command')
    print(arg, type(arg))

@bot.command()
async def scrape(ctx, subreddit, _max):
    scraper_client = DiscordRedditScraper(
        ctx,
        client_id='TB0-ZpHZQF6Qog',
        client_secret='Rz4XNGcDBZVMQE45IpB0EBl-p3s',
        user_agent='windows:cbm.projects.redditscraper:v2.0 (by /u/PTTruTH)',
    )
    await scraper_client.scrape(subreddit, _max)

bot.run(TOKEN)
