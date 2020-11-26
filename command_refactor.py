from init_refactor import*

def getFont(im,top,middle,bottom):
    fontPath = r'c:\windows\fonts\arial.ttf'
    size = 90
    font = ImageFont.truetype(fontPath, size)
    sizeTop = font.getlength(top)
    sizeMiddle = font.getlength(middle)
    sizeBottom = font.getlength(bottom)
    if sizeTop >= sizeMiddle:
        if sizeTop >= sizeBottom:
            text = top
        else:
            text = bottom
    elif sizeMiddle >= sizeBottom:
        text = middle
    else:
        text = bottom
    temp = font.getlength(text)
    while temp > im.width:
        size -= 2
        font = ImageFont.truetype(fontPath, size)
        temp = font.getlength(text)
    font = ImageFont.truetype(fontPath, size)
    return [font,size]

def draw(image,top = '', middle = '', bottom = ''):
    temp = getFont(image,top,middle,bottom)
    font = temp[0]
    fontSize = temp[1]
    draw = ImageDraw.Draw(image)
    if top != '':
        draw.text((0,0),top,font = font)
    if middle != '':
        draw.text((0,(image.height-fontSize)/2),middle,font = font)
    if bottom != '':
        draw.text((0, image.height-fontSize),bottom,font = font)

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


def Admin(author):
    return author.guild_permissions.administrator

@bot.command()
async def hello(ctx):
    await ctx.send('Hello')

@bot.command()
async def get_emoji(ctx):
    if ctx.author.id == Elvin:
        emojis = await ctx.guild.fetch_emojis()
        urls = [[emoji.url,emoji.name] for emoji in emojis]
        for url in urls:
            await url[0].save('Emoji/' + url[1] + '.png')
        return

@bot.command()
async def save_emoji(ctx):
    if ctx.author.id == Elvin:
        for name in os.listdir("Emoji/"):
            with open("Emoji/" + name,'rb') as image:
                await ctx.guild.create_custom_emoji(name = name.rstrip('.png'), image = image.read())
        return

@bot.command()
async def emoji(ctx,Name):
    emojis = await message.guild.fetch_emojis()
    temp = Name.split(':')
    name = temp[1] if len(temp) > 1 else ''
    for emoji in emojis:
        if name == emoji.name:
            await ctx.send(emoji.url)
            break

@bot.command()
async def meme(ctx,top='',middle='',bottom=''):
    if len(ctx.message.attachments) == 1:
        async with ctx.message.channel.typing():
            attachment = ctx.message.attachments[0]
            await attachment.save('Temp/'+attachment.filename)
            im = Image.open('Temp/'+attachment.filename)
            draw(im,top,middle,bottom)
            im.save('Temp/'+attachment.filename)
            with open('Temp/'+attachment.filename,'rb') as file:
                await ctx.send(file = discord.File(file))
            os.remove('Temp/'+attachment.filename)
    await ctx.message.delete()

@bot.command()
async def bigemoji(ctx,Name):
    emojis = await ctx.guild.fetch_emojis()
    content = Name.lstrip('<')
    name = content.split(':')[1]
    factor = float(content.split('>')[1].strip()) if content.split('>')[1] != '' else 2
    if factor > 5:
        await ctx.message.delete()
        await ctx.send("```Le facteur max est 5 (c'est pour toi seb)```")
        return
    for emoji in emojis:
        if name == emoji.name:
            url = emoji.url
            break
    async with ctx.typing():
        await url.save('Temp/' + emoji.name + '.png')
        path = 'Temp/' + emoji.name + '.png'
        im = Image.open(path)
        size = (int(im.width * factor),int(im.height * factor))
        new = im.resize(size)
        new.save(path)
        await ctx.send(file = discord.File(path))
        os.remove(path)

@bot.command()
async def calc(ctx):
    content = ctx.message.content[5:].lstrip()
    if len(content) > 0:
        converted = convert(content)
        result = str(math(converted))
        if len(result) > (2000-6):
            await ctx.send("```The result is too long to be displayed```")
        else:
            await ctx.send("```"+result+"```")
    else:
        await ctx.send("```Vous n'avez rien donné a calculer```")

async def dele(message):
    await message.delete()

@bot.command()
async def delete(ctx,*args):
    if Admin(ctx.author) or ctx.author.id == Elvin:
        if len(args) > 1 and args[0] == 'bot':
            if args[1].isdigit():
                number=int(args[1])
                messages = await ctx.message.channel.history(limit=number+1).flatten()
                for m in messages:
                    if m.author==bot.user:
                        await m.delete()
            await message.delete()
        else:
            if args[0].isdigit():
                number=int(args[0])
                messages = await ctx.message.channel.history(limit=number+1).flatten()
                for m in messages:
                    await m.delete()
    else:
        await ctx.message.delete()
    return

@bot.command()
async def Flavien(ctx):
    if ctx.author.id != 362644900535074816:
        await ctx.send("``` Cher Flavien,\n rapelle toi que tu n'auras jamais de pouvoir sur ce serveur\n Avec les compliments de la direction  ```")

@bot.command()
async def id(ctx):
    if ctx.author.id == Elvin:
        if len(ctx.message.channel_mentions) == 1:
            channel = ctx.message.channel_mentions[0]
            print(channel.id)
        elif len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
            print(user.name + ' id ' + str(user.id))
    return

@bot.command()
async def bdm(ctx):
    if len(ctx.message.mentions) == 1 or len(ctx.message.mentions) == 2:
        mention = ctx.message.mentions
        for user in mention:
            if user.voice != None:
                await user.move_to([channel for channel in ctx.guild.voice_channels if channel.name == "A fait une blague de merde" or channel.name == "blague de merde"][0])
        await ctx.message.delete()
    return

@bot.command()
async def avis(ctx):
    if len(ctx.message.mentions) == 1 or len(ctx.message.mentions) == 2:
        mention = ctx.message.mentions
        for user in mention:
            if user.voice != None and (user.id == 530726932216807437 or user.id == 362644900535074816):
                await user.move_to([channel for channel in ctx.guild.voice_channels if channel.name == "Avis Biaisé"][0])
        await ctx.message.delete()
    return

@bot.command()
async def embed(ctx):
    embed = discord.Embed(description = "test Embed", color = 0x0e15d8)
    await ctx.send(embed = embed)

@bot.command()
async def mute(ctx):
    if Admin(ctx.author) and not(ctx.message.channel.id == 772515947503943690):
        to_mute = ctx.message.mentions
        if "$mutevoice" in ctx.message.content:
            for m in to_mute:
                if m.voice != None:
                    await m.edit(mute = True)
                    MutedVoice.append(m)
        else:
            for m in to_mute:
                Muted.append(m)
        await ctx.message.delete()
    return

@bot.command()
async def unmute(ctx):
    if Admin(ctx.author) and not(ctx.message.channel.id == 772515947503943690):
        to_mute = ctx.message.mentions
        if "$unmutevoice" in ctx.message.content:
            for m in to_mute:
                if m in MutedVoice and m.voice != None:
                    await m.edit(mute = False)
                    MutedVoice.remove(m)
        else:
            for m in to_mute:
                if m in MutedVoice:
                    Muted.remove(m)
        await ctx.message.delete()
    return

@bot.command()
async def mutelist(ctx):
    if len(Muted) == 0:
        embed = discord.Embed(description = "No one is mute !", color = 0x0e15d8)
        await ctx.send(embed = embed)
    else:
        list = [user.mention for user in Muted]
        text = ''
        for mention in list:
            text += mention
        embed = discord.Embed(description = text, color = 0x0e15d8)
        await ctx.send(embed = embed)

@bot.command(aliases=['oscour', 'aled'])
async def Help(ctx):
    await ctx.send("```$mute @quelqu'un  mute la personne\n$unmute @quelqu'un unmute la personne (voc aussi)\n$list déroule la liste des gens qui sont mutés sur ce serveur\n$mutevoice @quelqu'un mute la voix de la personne si sur vocal\n\n$delete x, x un nombre, supprime autant de messages que x\n$delete bot x comme la précédente mais que pour les messages du bot\n\n$bdm @quelqu'un bouge cette personne dans 'blague de merde', que si déjà en vocal\n$avis @quelqu'un bouge la personne dans'avis biaisé' (seulement Hugo et Flavien(pour le moment j'éspère))\n\n$Flavien envoie un petit message mignon à Flavien alias Thimothé\n$emoji :nomEmoji: renvoie l'emoji custom dans sa taille originale\n$bigemoji :nomEmoji: x  renvoie l'emoji custom aggrandie en taille 2 ou si précisé multiplié par un facteur x```")
    await ctx.message.delete()
