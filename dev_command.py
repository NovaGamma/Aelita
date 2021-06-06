from init import*

@bot.command()
async def getxD(ctx):
    if ctx.author.id == Elvin:
        sum = 0
        total_messages = 0
        for server in bot.guilds:
            await ctx.channel.send(f"Doing server : {server.name}")
            for channel in server.channels:
                if type(channel) is discord.TextChannel:
                    await ctx.channel.send(f"Doing channel : {channel.name}")
                    messages = await channel.history()
                    for message in messages:
                        if message.author.id == Elvin:
                            total_messages += 1
                            content = message.content
                            if "xD" in content:
                                sum += 1
        await ctx.channel.send(f"The total number of xD is {sum}")



@bot.command()
async def get_emoji(ctx):
    if ctx.author.id == Elvin:
        emojis = await ctx.guild.fetch_emojis()
        urls = [[emoji.url,emoji.name] for emoji in emojis]
        for url in urls:
            await url[0].save('Emoji/' + url[1] + '.png')
        return

@bot.command()
async def Hello(ctx):
    if ctx.author.id == Elvin:
        await ctx.channel.send(f"Hello u")

@bot.command()
async def e(ctx):
    if ctx.author.id == Elvin:
        txt = ctx.message.content.lstrip("$e ")
        with open('file.py','w') as file:
            file.write(txt)
        proc = subprocess.Popen('python file.py', stdin = subprocess.PIPE, stdout = subprocess.PIPE,stderr=subprocess.STDOUT)
        stdout, stderr = proc.communicate()
        with open('result.txt','w') as result:
            result.write(stdout.decode())

        with open('result.txt','r') as result:
            txt = [line for line in result if line != '\n']

        txt = ''.join(txt)
        await ctx.send(f"The result is :\n```{txt}```")

@bot.command()
async def save_emoji(ctx):
    if ctx.author.id == Elvin:
        for name in os.listdir("Emoji/"):
            with open("Emoji/" + name,'rb') as image:
                await ctx.guild.create_custom_emoji(name = name.rstrip('.png'), image = image.read())
        return

@bot.command()
async def emoji(ctx,Name):
    emojis = await ctx.guild.fetch_emojis()
    temp = Name.split(':')
    name = temp[1] if len(temp) > 1 else ''
    for emoji in emojis:
        if name == emoji.name:
            await ctx.send(emoji.url)
            break

@bot.command()
async def roles(ctx):
    if ctx.author.id == Elvin:
        string = "```"
        for i,v in enumerate(ctx.guild.roles):
            name = v.name
            string += f"{i} {name}\n"
        string += "```"
        await ctx.channel.send(string)

@bot.command()
async def people(ctx):
    if ctx.author.id == Elvin:
        print(ctx.guild)
        string = "```"
        for i,v in enumerate(ctx.guild.members):
            name = v.name
            string += f"{i} {name}\n"
        string += "```"
        await ctx.channel.send(string)

@bot.command()
async def give_role(ctx,number):
    if ctx.author.id == Elvin:
        number = int(number)
        await ctx.author.add_roles(ctx.guild.roles[number])

@bot.command()
async def remove_role(ctx,number):
    if ctx.author.id == Elvin:
        number = int(number)
        await ctx.author.remove_roles(ctx.guild.roles[number])

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
