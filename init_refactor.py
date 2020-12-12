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

engine = pyttsx3.init()

BOT_PREFIX = '$'
bot = commands.Bot(command_prefix=(BOT_PREFIX,'&'))
MutedVoice = []
Muted = []
Elvin = 281432668196044800
al = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
mention = ['Oui ?','Oui ??','Stop','Vraiment Stop','STOP !!']
count = 0
#talk = Talk(bot)
ctime = 0

Motus = {}
dico = enchant.Dict("fr_FR")

from command_refactor import*
from Motus.motus_refactor import load_motus
from voice import*

Motus = load_motus()

Games = []
Guild = None

from Motus.motus_refactor import motus
