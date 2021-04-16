from init import*

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
        await ctx.channel.send("```{}```".format("\n".join([role.name for role in ctx.guild.roles])))

@bot.command()
async def give_role(ctx,number):
    if ctx.author.id == Elvin:
        number = int(number)
        await ctx.author.add_roles(ctx.guild.roles[number])

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
