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
    print("Hi Elvin i'm here")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

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

client.run("NzcyNTA3ODM1MjI1MjEwOTAw.X57r_A.50E4BKDU_pLs21vsZwDlvO0iYT4")
