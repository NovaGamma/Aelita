import discord
from discord.ext import commands
import os
import random
import time
#from talk import Talk
from datetime import datetime
import enchant
from PIL import Image, ImageDraw, ImageFont
from strMath import*
from discord.utils import get
import youtube_dl
import pyttsx3
import subprocess
import importlib

engine = pyttsx3.init()

BOT_PREFIX = '$'
bot = commands.Bot(command_prefix=(BOT_PREFIX,'&'))
MutedVoice = []
Muted = []
MuteRole = 809786088075821116
Elvin = 281432668196044800

number_list = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

al = ["%c"%char for char in range(65,91)]
mention = ['Oui ?','Oui ??','Stop','Vraiment Stop','STOP !!']
count = 0
#talk = Talk(bot)
ctime = 0

Motus = {}
Games = []

import TicTacToe.tictactoe as tictactoe
dico = enchant.Dict("fr_FR")
from command import*
from Motus.motus import load_motus
#from voice import*

Motus = load_motus()


Guild = None

from Motus.motus import motus
