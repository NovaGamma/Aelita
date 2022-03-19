import discord
from discord.ext import commands
import os
import random
import time
from datetime import datetime
import enchant
from strMath import*
from discord.utils import get
import subprocess
import importlib
import requests
import json


library_path = os.environ.get("TEST")
print(os.path.exists(library_path))

intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True
intents.emojis = True
intents.reactions = True

BOT_PREFIX = '$'
bot = commands.Bot(command_prefix = BOT_PREFIX, intents = intents)
MutedVoice = []
Muted = []
MuteRole = 809786088075821116
Elvin = 281432668196044800

number_list = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

al = ["%c"%char for char in range(65,91)]
al.append('-')
count = 0
ctime = 0

Motus = {}
Games = []

import TicTacToe.tictactoe as tictactoe
print(enchant.list_languages())
dico = enchant.Dict("fr_FR")
from command import*
from music import*
from Motus.motus import load_motus
import dev_command as dev
from talking import*
#from voice import*

Motus = load_motus()


Guild = None

from Motus.motus import motus
