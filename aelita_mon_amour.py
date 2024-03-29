from init import*

def Message(message,text):
    return True if message.content.startswith(text) else False

def Admin(author):
    return author.guild_permissions.administrator

async def get_guilds():
    Putin = ''
    Muffin = ''
    Stock = ''
    async for guild in bot.fetch_guilds():
        if guild.name == "Poutine lovers":
            Putin = bot.get_guild(guild.id)
        elif guild.name == "Muffin Sect":
            Muffin = bot.get_guild(guild.id)
        elif guild.name == "Stock Market":
            Stock = bot.get_guild(guild.id)
    return [Putin,Muffin,Stock]

@bot.event
async def on_ready():
    print("Hi Elvin i'm here")
    global talk
    talk = Talk(bot)


@bot.event
async def on_member_join(member):
    await member.edit(nick = f"Muffin {member.display_name}")

@bot.listen('on_message')
async def process(message):
    if message.author == bot.user:
        return

    if message.author in Muted and not(message.channel.name == "diplomatie" or message.channel.name == "musique") and not(message.author.id == 281432668196044800):
        await message.delete()
        return

    if 'talk' in globals() and len(talk.connected) != 0 and talk.sending(message): #message.channel.id == talk.log_channel.id:
        await talk.send(message)
        return

    if 'talk' in globals() and len(talk.connected) != 0 and talk.receiving(message): #message.channel.id == talk.channel.id:
        await talk.log(message)

    if isinstance(message.channel, discord.abc.PrivateChannel):
        return

    if message.channel.guild.name in Motus.keys():
        await motus(message)

@bot.command()
async def connect(ctx):
    await talk.connect(ctx.message)

@bot.command()
async def disconnect(ctx):
    await talk.disconnect(ctx.message)

@bot.event
async def on_reaction_add(reaction,user):
    if user == bot.user:
        return
    if reaction.emoji in number_list or reaction.emoji == "✅":
        for game in Games:
            if reaction.message == game.message[-1]:
                if reaction.emoji == "✅":
                    await game.addPlayer(user)
                else:
                    await tictactoe.PlaceT(reaction,user)
                await reaction.remove(user)

@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return
    if payload.emoji.name == '🎉':
        print('yay')
    print(repr(payload.emoji.name))

@bot.command()
async def load(ctx,*args):
    if not ctx.author.id == Elvin:
        return
    if len(args) != 0:
        args[0] = name
    else:
        os.system("cls")
        os.system("python aelita_mon_amour.py")
        quit()
        return
    if name == 't':
        tictactoe.reset()
        os.system("cls")
        importlib.reload(tictactoe)
        return

#id hugo = 530726932216807437
#-------------------- ‼️
with open('Id/id.txt','r') as IdFile:
    token = IdFile.read()
#token = os.getenv("BOT_TOKEN")
bot.run(token)
