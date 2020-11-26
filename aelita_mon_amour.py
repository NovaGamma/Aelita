from init import*
from talk import*

def Message(message,text):
    return True if message.content.startswith(text) else False

def Admin(author):
    return author.guild_permissions.administrator

async def get_guilds():
    async for guild in client.fetch_guilds():
        if guild.name == "Poutine lovers":
            Putin = client.get_guild(guild.id)
        elif guild.name == "Muffin Sect":
            Muffin = client.get_guild(guild.id)
        elif guild.name == "Stock Market":
            Stock = client.get_guild(guild.id)
    return [Putin,Muffin,Stock]

@client.event
async def on_ready():
    talk.guilds = await get_guilds()
    global Guild
    Guild = talk.guilds[1]
    print("Hi Elvin i'm here")
    activity = discord.CustomActivity("AHHHHH")
    await client.change_presence(activity = activity)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.author.id == Elvin and message.content.startswith('$Voice'):
        voice_channel = message.author.voice.channel
        if voice_channel != None:
            channel = voice_channel.name
            vc = await voice_channel.connect()
            with open('test.mp3','rb') as data:
                vc.send_audio_packet(data,encode = False)
            #player = vc.create_ffmpeg_player('test.mp3')
            #player.start()
            #while not player.is_done():
            #    await asyncio.sleep(1)
            # disconnect after the player has finished
            #player.stop()
            #await vc.disconnect()


    if len(message.mentions) > 0 and message.mentions[0] == client.user:
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

    if len(message.content) == 1 and message.content in al:
        index = al.index(message.content) + 1
        if index != len(al):
            character = al[index]
            await message.channel.send('```' + character + '```')

    if message.content.isdigit():
        number = int(message.content)
        if number == 69:
            text = "```Nice !```"
        else:
            text = "```" +str(number + 1) + "```"
        if len(text) < 2000:
            await message.channel.send(text)
        else:
            await message.channel.send("```Tu es trop gourmand```")

    if message.author in Muted and not(message.channel.name == "diplomatie" or message.channel.name == "musique") and not(message.author.id == 281432668196044800):
        await message.delete()
        return

    if 'talk' in globals() and len(talk.connected) != 0 and talk.sending(message): #message.channel.id == talk.log_channel.id:
        await talk.send(message)
        return

    if 'talk' in globals() and len(talk.connected) != 0 and talk.receiving(message): #message.channel.id == talk.channel.id:
        await talk.log(message)

    if Message(message,'$'):
        if Message(message,'$M'):
            await motus(message)
        else:
            await Command(message)
        return

    if Message(message,'&'):
        await talk.connect(message)
        return

    for game in Games:#part that will check if the received message belong to a message sent in a game to be treated by a dedicated function
        if message.channel.category.id == game.gameCategory.id:
            await gameMessage(message,game)

    if message.content == ("Create Game") and message.channel.name == "games":
        if not inGame(message.author):
            await createGame(message,Guild)
            await message.delete()
        else:
            await message.channel.send(message.author.mention + " You're already in a game, you can't create one",delete_after = 30)
            await message.delete()
        return

    if message.content == "delete game":
        if message.author.guild_permissions.administrator:
            categoryId = message.channel.category_id
            for category in Guild.categories:
                if categoryId == category.id and "Game" in category.name:
                    for channel in category.channels:
                        await channel.delete()
                    await category.delete()
                    return

    if message.channel.guild.name in Motus.keys():
        await motus(message)

@client.event
async def on_reaction_add(reaction,user):
    if reaction.count == 1 and reaction.emoji == "‼️":
        if reaction.message.author.voice != None:
            await reaction.message.add_reaction("‼️")
            await reaction.message.author.move_to([channel for channel in reaction.message.guild.voice_channels if channel.name == "A fait une blague de merde" or channel.name == "blague de merde"][0])
            return

    if reaction.count == 1 and reaction.emoji == "🤡":
        if reaction.message.author.voice != None and (reaction.message.author.id == (530726932216807437 or 362644900535074816)):
            await reaction.message.add_reaction("🤡")
            await reaction.message.author.move_to([channel for channel in reaction.message.guild.voice_channels if channel.name == "Avis Biaisé"][0])
            return


#embed=discord.Embed(title="Title", url="https://url", description="description", color=0x0e15d8)
#embed.set_author(name="author name", url="httpauthor link",, icon_url="http icon" member.avatar_url )
#embed.set_thumbnail(url="httpicon")
#embed.add_field(name="field name", value="field value", inline=True)
#embed.set_footer(text="footer text")
#await ctx.send(embed=embed)



#id hugo = 530726932216807437
#-------------------- ‼️
with open('Id/id.txt','r') as IdFile:
    id = IdFile.read()
client.run(id)
