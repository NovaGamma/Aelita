from init import*

async def get_guilds():
    async for guild in client.fetch_guilds():
        if guild.name == "Poutine lovers":
            Putin = client.get_guild(guild.id)
        elif guild.name == "Muffin Sect":
            Muffin = client.get_guild(guild.id)
        elif guild.name == "Stock Market":
            Stock = client.get_guild(guild.id)
    return [Putin,Muffin,Stock]

def Message(message,text):
    return True if message.content.startswith(text) else False

def Admin(author):
    return author.guild_permissions.administrator

async def Command(message):
    if Message(message,'$get_emoji') and message.author.id == Elvin:
        emojis = await message.guild.fetch_emojis()
        urls = [[emoji.url,emoji.name] for emoji in emojis]
        for url in urls:
            await url[0].save('Emoji/' + url[1] + '.png')
        return

    elif Message(message,'$save_emoji') and message.author.id == Elvin:
        for name in os.listdir("Emoji/"):
            with open("Emoji/" + name,'rb') as image:
                await message.guild.create_custom_emoji(name = name.rstrip('.png'), image = image.read())
        return

    elif Message(message,'$delete'):
        if Admin(message.author):
            if Message(message,'$delete bot'):
                temp=message.content.split(' ')
                if temp[2].isdigit():
                    number=int(temp[2])
                    messages = await message.channel.history(limit=number+1).flatten()
                    for m in messages:
                        if m.author==client.user:
                            await m.delete()
                await message.delete()
            else:
                temp=message.content.split(' ')
                if temp[1].isdigit():
                    number=int(temp[1])
                    messages = await message.channel.history(limit=number+1).flatten()
                    for m in messages:
                        await m.delete()
        else:
            await message.delete()
        return

    elif Message(message,"$A"):
        await message.channel.send(":regional_indicator_a:")

    elif Message(message,"$Flavien"):
        if message.author.id != 362644900535074816:
            await message.channel.send("``` Cher Flavien,\n rapelle toi que tu n'auras jamais de pouvoir sur ce serveur\n Avec les compliments de la direction  ```")
            #await message.channel.send("```   ```")

    elif Message(message,"$id"):
        if message.author.id == 281432668196044800:
            if len(message.channel_mentions) == 1:
                channel = message.channel_mentions[0]
                print(channel.id)
            elif len(message.mentions) == 1:
                user = message.mentions[0]
                print(user.name + ' id ' + str(user.id))
        return

    elif Message(message,"$bdm"):
        if len(message.mentions) == 1 or len(message.mentions) == 2:
            mention = message.mentions
            for user in mention:
                if user.voice != None:
                    await user.move_to([channel for channel in message.guild.voice_channels if channel.name == "A fait une blague de merde" or channel.name == "blague de merde"][0])
            await message.delete()
        return

    elif Message(message,"$avis"):
        if len(message.mentions) == 1 or len(message.mentions) == 2:
            mention = message.mentions
            for user in mention:
                if user.channel != None and (user.id == 530726932216807437 or user.id == 362644900535074816):
                    await user.move_to([channel for channel in message.guild.voice_channels if channel.name == "Avis Biaisé"][0])
            await message.delete()
        return

    elif Message(message,"$embed"):
        embed = discord.Embed(description = "test Embed", color = 0x0e15d8)
        await message.channel.send(embed = embed)

    elif Message(message,'$mute'):
        if Admin(message.author) and not(message.channel.id == 772515947503943690):
            to_mute = message.mentions
            if "$mutevoice" in message.content:
                for m in to_mute:
                    if m.voice != None:
                        await m.edit(mute = True)
                        MutedVoice.append(m)
            else:
                for m in to_mute:
                    Muted.append(m)
            await message.delete()
        return

    elif Message(message,'$unmute'):
        if Admin(message.author) and not(message.channel.id == 772515947503943690):
            to_mute = message.mentions
            if "$unmutevoice" in message.content:
                for m in to_mute:
                    if m in MutedVoice and m.voice != None:
                        await m.edit(mute = False)
                        MutedVoice.remove(m)
            else:
                for m in to_mute:
                    if m in MutedVoice:
                        Muted.remove(m)
            await message.delete()
        return

    elif Message(message,'$list'):
        if len(Muted) == 0:
            embed = discord.Embed(description = "No one is mute !", color = 0x0e15d8)
            await message.channel.send(embed = embed)
        else:
            list = [user.mention for user in Muted]
            text = ''
            for mention in list:
                text += mention
            embed = discord.Embed(description = text, color = 0x0e15d8)
            await message.channel.send(embed = embed)

    elif Message(message,"$help") or Message(message,"$oscour") or Message(message,"$aled"):# == "$help": #or "$aled" or "$oscour":
        await message.channel.send("```$mute @quelqu'un  mute la personne\n$unmute @quelqu'un unmute la personne (voc aussi)\n$list déroule la liste des gens qui sont mutés sur ce serveur\n$mutevoice @quelqu'un mute la voix de la personne si sur vocal\n\n$delete x, x un nombre, supprime autant de messages que x\n$delete bot x comme la précédente mais que pour les messages du bot\n\n$bdm @quelqu'un bouge cette personne dans 'blague de merde', que si déjà en vocal\n$avis @quelqu'un bouge la personne dans 'avis biaisé' (seulement Hugo et Flavien(pour le moment j'éspère))\n\n$Flavien envoie un petit message mignon à Flavien alias Thimothé```")
        await message.delete()
