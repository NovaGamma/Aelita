import discord
import os
import random
import time
from talk import Talk
from datetime import datetime
import enchant
from PIL import Image, ImageDraw, ImageFont

MutedVoice = []
Muted = []
client = discord.Client()
Elvin = 281432668196044800
al = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
mention = ['Oui ?','Oui ??','Stop','Vraiment Stop','STOP !!']
count = 0
talk = Talk(client)
ctime = 0

Motus = {}
dico = enchant.Dict("fr_FR")

from Motus.motus import load_motus

Motus = load_motus()

Games = []
Guild = None

from Motus.motus import motus
from command import Command
from TheWolf.wolf import gameMessage,inGame,createGame
