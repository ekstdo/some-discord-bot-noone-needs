import _thread
pi = 3.1415926535897932384626433832795028841971693993751058209749445923078164062862089986280348253421170679

sqrt = lambda x: x ** 0.5
sq = lambda x: x ** 2

import sqlite3, discord, asyncio, logging, bs4 
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
from discord import PermissionOverwrite, Permissions
from discord import Game, Server, Member, Embed
from io import StringIO
import time, datetime, calendar, random, math, sys, contextlib, json, os
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
link = "https://discordapp.com/oauth2/authorize?client_id=397678986953752576"
class GET_DATA:
    def __init__(self, url): 
        self.url = url 
        opened = urlopen(url)
        self.inner = opened.read()
        opened.close()
        self.page = bs(self.inner , "html.parser")
def DUDEN(word):
    inner = GET_DATA("https://www.duden.de/rechtschreibung/"+word)
    return inner.page.find("ol")
def get_duden(word):
    try:
        a = DUDEN(word)
        definitions = [i.text for i in a.findAll("li")]
        return definitions
    except:
        return ["404 Error occured, something went wrong"]
bot_token = os.environ["bot_token"]
prefix = None 
with open('prefix.txt', 'r') as prefixfile:
    prefixread = prefixfile.read()
    prefix = prefixread.split('\n')[0]
print(prefix)
prefix_len = len(prefix)
sql_connection = sqlite3.connect('example.db')
sql_cursor = sql_connection.cursor()

class SomeBot(discord.Client):
    async def on_ready(self):
        print("Discord Bot Test is there!")
        a = open("setup.json", "r")
        self.dictionary = json.loads(a.read())
        a.close()
        self.repl_channel = get(self.get_all_channels(), name = self.dictionary["repl_channel"])
        self.logging_channel = get(self.get_all_channels(), name = self.dictionary["logging_channel"])
        self.main_server = self.dictionary["main_server"]
    async def on_message(self, message):
        if message.content.startswith(prefix):
            self.command(message)
        elif message.channel.name == self.repl_channel.name and message.server.name == self.main_server: 
            if not self.repl_channel: self.repl_channel = message.channel
            print("[repl]: ", message.content)
            await self.repl(message)
        else:
            print(f'[msg| {message.author}, {message.server}.{message.channel}]: {message.content}')
    async def send_error(self, msg, channel):
        await self.send_message(channel, f"Some thing went wrong... [{msg}]")
    async def save(self):
        a = open("setup.json", "w")
        a.close()
        await self.send_message("saved", logging_channel)
    async def repl(self, message):
        master = False 
        content = message.content
        split_msg = message.content.split(" ")
        if message.content.startswith("sudo"):
            split_msg.pop(0)
            content = content[5:]
            if message.author.server_permissions:
                master = True
        if content.startswith("def."):
            defs = get_duden(split_msg[1])
            n_defs = [str(i) + ".:" + j for i, j in enumerate(defs)]
            await self.send_message(message.channel, "```" +  "\n".join(n_defs) + "```")
        elif split_msg[0] == "len":
            await self.send_message(message.channel, len(content[4:]))
        elif split_msg[0] == "rev":
            await self.send_message(message.channel, content[4:][::-1])
        elif split_msg[0] == "echo":
            await self.send_message(message.channel, content[5:])
        elif split_msg[0] == "invite":
            await self.send_message(message.channel, link)
        # elif split_msg[0] == "purge":
        #     await
        elif split_msg[0] == "avatar":
            if len(split_msg) == 1: 
                a = discord.Embed()
                a.set_image(url = message.author.avatar_url)
                await self.send_message(message.channel, "", embed = a)
            else: 
                mem_id = int(split_msg[1].replace("<", '').replace('!', '').replace('>', '').replace('@', ''))
                member = message.server.get_member(mem_id)
                if member:
                    a = discord.Embed()
                    a.set_image(url = member.avatar_url)
                    await self.send_message(message.channel, "", embed = a)
                else:
                    await self.send_error("Member not there", message.channel)
        elif split_msg[0] == "avatar_link": 
            if len(split_msg) == 1:
                await self.send_message(message.channel, message.author.avatar_url)
            else:
                mem_id = int(split_msg[1][2:-1])
                member = get(self.get_all_members())
                await self.send_message(message.channel, member.avatar_url)
        if master: 
            if content.startswith("setchannel"):
                try:
                    ids = int(split_msg[1][2:-1])
                    self.logging_channel = self.get_channel(ids)
                except:
                    await self.send_error("channel not found", message.channel)
        

logging.basicConfig(level=logging.INFO)

client = SomeBot()


client.run(bot_token)

