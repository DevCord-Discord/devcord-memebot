import os
import praw
import discord
from random import randint, choice
from discord.ext import commands

client = commands.Bot(command_prefix="!")

reddit = praw.Reddit(client_id = os.environ["CLIENT_ID"],
                     client_secret = os.environ['CLIENT_SECRET'],
                     user_agent="Mozilla/5.0 (Windows NT 6.2; rv:20.0) Gecko/20121202 Firefox/20.0")

class Client(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def clear(self, ctx, amount = 10000000):
        await ctx.channel.purge(limit=amount)

    @commands.command
    async def help(self, ctx):
        embed = discord.Embed(title="dude for the resque", description="Some useful commands to use")
        embed.add_field(name="help", value="shows the commands to my guy")
        await ctx.send(content=None, embed=embed)

    @commands.command()
    async def meme(self, ctx):
        rnd = randint(0,5)
        subreddit = choice(["memes", "dankmemes", "linuxmemes", "programmerhumour", "masterhacker"])
        memes = reddit.subreddit(subreddit).new(limit=7)
        post = [p for p in memes if not p.stickied][rnd]
        embed = discord.Embed(description=post.title , color=randint(0, 0xFFFFFF), title=f"Memes for my guy")
        embed.set_author(name=f"{subreddit}",icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSj-m3NbE4PZ6TA1U53cIDr1fIjkT2OCzYvBA&usqp=CAU")
        embed.set_image(url=str(post.url))
        await ctx.send(embed=embed)

    @commands.command(aliases=['coder-scanner', 'skill_scanner'])
    async def skills(self, ctx,* ,user: discord.Member=None):
        """skills sensor to identify skilled programmers"""
        if not user:
            user = ctx.author.name
        techsavy = randint(0,100)
        if techsavy <= 33:
            skillsStatus = choice(["Noob",
                                       "Stackoverflow copypasta guy",
                                       "git push -force",
                                       "script kiddie",
                                       "the scammer guy",
                                       "try: *entire code* except : print('oopsie')",
                                       "Hella noob"])
            skillsColor = 0xFFC0CB
        elif 33 < techsavy < 66:
            skillsStatus = choice(["Hard worker",
                                       "Senior developer promotion incoming",
                                       "moderate",
                                       "the edgelord of programming",
                                       "r/programmerhumour",
                                       "half noob",
                                       "masterhaxor"])
            skillsColor = 0xFF69B4
        else:
            skillsStatus = choice(["Pro",
                                       "phD in C.S",
                                       "Senior developer",
                                       "Facebook intern",
                                       "Works in FANG",])
            skillsColor = 0xFF00FF
        emb = discord.Embed(description=f"Skills for **{user}**", color=skillsColor)
        emb.add_field(name="Skills:", value=f"{techsavy}% techsavy")
        emb.add_field(name="Comment:", value=f"{skillsStatus}")
        emb.set_author(name="Skills Tester™", icon_url="https://techcrunch.com/wp-content/uploads/2015/04/codecode.jpg?w=1390&crop=1")
        emb.set_image(url="https://media.giphy.com/media/hrRJ41JB2zlgZiYcCw/giphy.gif")
        await ctx.send(embed=emb)

def setup(client):
    client.add_cog(Client(client))
