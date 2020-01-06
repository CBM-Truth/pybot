import discord
from discord.ext import commands
from scraper import DiscordRedditScraper
from bot_token import TOKEN

bot = commands.Bot(command_prefix='!')

@bot.command()
async def scrape(ctx, subreddit, _max):
    scraper_client = DiscordRedditScraper(
        ctx,
        client_id='TB0-ZpHZQF6Qog',
        client_secret='Rz4XNGcDBZVMQE45IpB0EBl-p3s',
        user_agent='windows:cbm.projects.redditscraper:v2.0 (by /u/PTTruTH)',
    )
    await scraper_client.scrape(subreddit, _max)

@bot.command()
async def log(ctx, message):
    print('logging...')
    await ctx.send_message(message.author, message)


@bot.command()
async def 

bot.run(TOKEN)
