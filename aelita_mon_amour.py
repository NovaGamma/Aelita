from init import*
#from talk import*

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

@bot.listen('on_message')
async def process(message):
    if message.author == bot.user:
        return

    if len(message.mentions) > 0 and message.mentions[0] == bot.user:
        if message.content[0] == '<' and message.content[len(message.content)-1] == '>':
            global count
            global ctime
            if count == 5:
                count = 0
            if count != 0:
                factor = (time.time() - ctime)%10
                if factor > count:
                    count = 0
                else:
                    count -= factor
            await message.channel.send("```" + mention[count] + "```")
            count += 1
            ctime = time.time()
        elif len(message.content.lstrip('<@!772507835225210900>').split(' ')) == 2:
            word = message.content.lstrip('<@!772507835225210900>').lstrip().split(' ')[0]
            await message.channel.send('https://fr.wikipedia.org/wiki/' + word)

    #if len(message.content) == 1 and message.content in al:
    #    index = al.index(message.content) + 1
    #    if index != len(al):
    #        character = al[index]
    #        await message.channel.send('```' + character + '```')

    #if message.content.isdigit():
    #    number = int(message.content)
    #    if number == 69:
    #        text = "```Nice !```"
    #    else:
    #        text = "```" +str(number + 1) + "```"
    #    if len(text) < 2000:
    #        await message.channel.send(text)
    #    else:
    #        await message.channel.send("```Tu es trop gourmand```")

    if message.author in Muted and not(message.channel.name == "diplomatie" or message.channel.name == "musique") and not(message.author.id == 281432668196044800):
        await message.delete()
        return

    #if 'talk' in globals() and len(talk.connected) != 0 and talk.sending(message): #message.channel.id == talk.log_channel.id:
        #await talk.send(message)
        #return

    #if 'talk' in globals() and len(talk.connected) != 0 and talk.receiving(message): #message.channel.id == talk.channel.id:
        #await talk.log(message)

    #if Message(message,'&'):
    #    await talk.connect(message)
    #    return

    if isinstance(message.channel, discord.abc.PrivateChannel):
        return

    if message.channel.guild.name in Motus.keys():
        await motus(message)

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
#with open('Id/id.txt','r') as IdFile:
#    id = IdFile.read()
token = os.getenv("BOT_TOKEN")
bot.run(token)
