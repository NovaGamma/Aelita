import discord
import os
import random
import time
from talk import Talk
from datetime import datetime
import enchant


MutedVoice = []
Muted = []
client = discord.Client()
Elvin = 281432668196044800

talk = Talk(client)

Motus = {}
dico = enchant.Dict("fr_FR")

from Motus.motus import load_motus

Motus = load_motus()

Games = []
Guild = None

from Motus.motus import motus
from command import Command
from TheWolf.wolf import gameMessage,inGame,createGame
