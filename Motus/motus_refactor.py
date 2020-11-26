from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from init_refactor import*  # Replace "my_module" here with the module name.
sys.path.pop(0)

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

def load_motus(guild='all'):
    #Motus = {}
    if os.path.exists('Guilds.txt'):
        with open("Guilds.txt",'r') as GuildFile:
            for line in GuildFile:
                temp=line.split(':')
                guild_name=temp[0]
                if guild_name==guild or guild=='all':
                    with open(guild_name+'/channel.txt','r') as ChannelFile:
                        Channels=[]
                        for line in ChannelFile:
                            Channels.append(int(line))
                    Motus[guild_name]={}
                    Motus[guild_name]['channels']=Channels
                    if os.path.exists(guild_name+'/Motus.txt'):
                        with open(guild_name+"/Motus.txt",'r') as MotusFile:
                            Motus[guild_name]['motus']={}
                            for line in MotusFile:
                                temp=line.split(':')
                                temp[1]=temp[1].rstrip('\n')
                                if temp[0] == 'status':
                                    Motus[guild_name]['motus']['status'] = temp[1].split(',')
                                else:
                                    Motus[guild_name]['motus'][temp[0]]=temp[1]
        if guild=='all':
            return Motus
        else:
            return Motus[guild]
    return {}

def save_motus(guild):
    try:
        with open(guild+'/Motus.txt','w+') as MotusFile:
            for key in Motus[guild]['motus'].keys():
                if key == 'status':
                    a = ','
                    MotusFile.write(key + ':' + a.join(Motus[guild]['motus'][key]) + '\n')
                else:
                    MotusFile.write(key + ':' + str(Motus[guild]['motus'][key]) + '\n')
    except:
        time.sleep(2)
        save_motus(guild)

def check_word(given_word,word):#given_word=word word=Motus[name]['motus']['word']
    state = []#0=:x: 1=:large_orange_diamond: 2=:red_circle:
    word_list = list(word)
    for i in range(len(given_word)):
        state.append(0)
    for i in range(len(given_word)):
        if given_word[i] == word[i]:
            word_list[i] = '!'
            state[i] = 2
    for i in range(len(given_word)):
        if given_word[i] in word_list and state[i] != 2:
            index = word_list.index(given_word[i])
            word_list[index] = '!'
            state[i] = 1
        elif state[i] != 2:
            state[i] = 0
    return state

def convert(state,word):
    good = 0
    text = ''
    for i in range(len(state)):
        if state[i] == 0:
            text += ':x:'
        if state[i] == 1:
            text += ':large_orange_diamond:'
        if state[i] == 2:
            good += 1
            text += ':regional_indicator_' + word[i].lower() + ':'
    return [text,good]

async def updateStatus(state,guild,message = None):
    word = Motus[guild]['motus']['word']
    change = False
    if not('status' in Motus[guild]['motus'].keys()) or len(Motus[guild]['motus']['status']) != len(word):
        Motus[guild]['motus']['status'] = []
        for i in range(len(word)):
            Motus[guild]['motus']['status'].append('0')
    status = Motus[guild]['motus']['status']
    for i in range(len(word)):
        if status[i] == '0':
            if state[i] == 2:
                status[i] = '2'
                change = True
    if change:
        save_motus(guild)
    Motus[guild]['motus']['status'] = status

async def displayStatus(guild,message):
    text = ''
    if 'status' in Motus[guild]['motus'].keys():
        status = Motus[guild]['motus']['status']
    else:
        await message.channel.send("```There is no status yet```")
    word = Motus[guild]['motus']['word']
    for i in range(len(status)):
        if status[i] == '2':
            text += ':regional_indicator_' + word[i].lower() + ':'
        else:
            text += ':x:'
    await message.channel.send(text)


async def motus(message):
    global Motus

@bot.command(name = 'Motus')
async def fMotus(ctx,*args):
    temp = args
    if len(temp) >= 1:
        ID = int(temp[0])
        word = temp[1]
        if os.path.exists("Guilds.txt"):
            with open("Guilds.txt",'r') as GuildFile:
                for line in GuildFile:
                    temp_guild = line.split(':')
                    if int(temp_guild[1]) == ID:
                        name = temp_guild[0]
        else:
            await ctx.send("```Motus n'a pas encore été activé```")
            return
    else:
        await ctx.send("```Tu dois d'abord donner l'id du serveur```")
        return
    if len(temp) == 2:
        if word.isupper() and word.isalpha():
            if dico.check(word):
                if not('word' in Motus[name]['motus'].keys()):
                    if ('winner' in Motus[name]['motus'].keys() and (Motus[name]['motus']['winner'] == str(ctx.author.id) or Motus[name]['motus']['winner'] == '-1')):
                        if len(word)>=2 and len(word)<=17:
                            Motus[name]['motus']['word'] = word
                            Motus[name]['motus']['author'] = str(ctx.author.id)
                            save_motus(name)
                            for guild in await get_guilds():
                                if guild.name == name:
                                    channel = guild.get_channel(Motus[name]['channels'][0])
                                    await channel.send("```Le mot actuel contient "+str(len(Motus[channel.guild.name]['motus']['word']))+" lettres et commence par un "+str(Motus[channel.guild.name]['motus']['word'][0])+"```")
                            await ctx.send("```Ton mot est enregistré```")
                        else:
                            await ctx.send("```Le mot doit avoir une longueur comprise entre 5 lettres et 15 lettres```")
                    else:
                        await ctx.send("```Tu n'es pas le dernier vainqueur```")
                else:
                    await ctx.send("```Il y a encore un mot a trouver```")
            else:
                await ctx.send("```Ce mot n'existe pas ou n'est pas dans le dictionnaire```")
        else:
            await ctx.send("```Tu dois donner le mot en majuscules```")
    else:
        await ctx.send("```Tu ne dois donner que des lettres```")
    return

@bot.command()
async def Mrecharge(ctx):
    if ctx.author.id==281432668196044800:
        await ctx.send("```Rechargé```")
        Motus = {}
        Motus = load_motus()

@bot.command()
async def Msupprime(ctx):
    if ctx.author.id==281432668196044800:
        with open("Motus.txt",'w+') as MotusFile:
            MotusFile.write('')
        await ctx.send("```Supprimé```")

@bot.command()
async def Mliste(ctx):
    if os.path.exists('Guilds.txt'):
        with open('Guilds.txt','r') as GuildFile:
            text='```'
            nServer=0
            for line in GuildFile:
                nServer+=1
                temp=line.split(':')
                text+='Nom : '+temp[0]+'   Id : '+temp[1]
            if nServer==1:
                t=' Serveur trouvé\n'
            else:
                t=' Serveurs trouvés\n'
            await ctx.send(str(nServer)+t+text)
    else:
        await ctx.send("```Aucun serveur enregistré```")

@bot.command()
async def Maide(ctx):
    await ctx.send("```$Mactiver : pour que les administrateurs activent Motus dans un canal \n\n$Passe : pour que les administrateurs sautent un mot s'il est trop compliqué \n\n$Mot : pour voir quels sont les conseils du mot actuel \n\n$Mchannel : pour voir dans quels canaux Motus a été activé \n\n$Mid : pour obtenir l'identifiant du serveur  \n\n$Motus : à faire en message privé au bot pour donner le mot à trouver, ne fonctionne que si Motus vient d'être activé ou si voustrouvez le dernier mot```")
    return

@bot.command()
async def Mid(ctx):
    if ctx.guild.name in Motus.keys():
        await ctx.send("```L'id du serveur est : "+str(ctx.guild.id)+"```")
    else:
        await ctx.send("```Motus n'a pas encore été activé sur ce serveur```")
    return

@bot.command()
async def Mactiver(ctx):
    if ctx.author.guild_permissions.administrator:
        iD=ctx.message.channel.id
        guild=ctx.guild
        with open("Guilds.txt",'a+') as GuildFile:
            already=0
            text=guild.name+':'+str(guild.id)+'\n'
            for line in GuildFile:
                if line==text:
                    already=1
            if already==0:
                GuildFile.write(guild.name+':'+str(guild.id)+'\n')
        if not(os.path.exists(guild.name)):
            os.mkdir(str(guild.name))
        with open(str(guild.name)+'/channel.txt','a+') as ChannelFile:
            exist=0
            for line in ChannelFile:
                line_channel=int(line)
                if line_channel==iD:
                    exist=1
            if not(exist):
                ChannelFile.write(str(iD)+'\n')
                await ctx.send("```Motus a été activé correctement```")
            else:
                await ctx.send("```Motus est déjà activé sur ce channel```")
                return
        with open(str(guild.name)+'/Motus.txt','a+') as MotusFile:#used to create the motus.txt file used to avoid bugs after
            pass
        Motus[guild.name]=load_motus(guild.name)
    else:
        await ctx.send("```Tu n'as pas la permission pour cette commande```",delete_after=20)
    return

@bot.command()
async def Mpasse(ctx):
    if ctx.author.guild_permissions.administrator or ctx.author.id == 281432668196044800:
        name = ctx.guild.name
        if not('word' in Motus[name]['motus'].keys()):
            await ctx.send("```L'ancien vainqueur a été enlevé, n'importe qui peut mettre un mot```")
            Motus[name]['motus']['winner'] = -1
            save_motus(name)
            Motus[name]=load_motus(name)
    return

@bot.command()
async def Mskip(ctx):
    if ctx.author.guild_permissions.administrator or ctx.author.id == Elvin:
        await ctx.send("```Le mot a été passé, n'importe qui peut en remettre un```")
        del Motus[name]['motus']['word']
        del Motus[name]['motus']['author']
        del Motus[name]['motus']['status']
        Motus[name]['motus']['winner'] = -1
        save_motus(name)
        Motus[name]=load_motus(name)
    else:
        await ctx.send("```Tu n'as pas les permissions pour passer le mot```",delete_after = 20)
        await ctx.message.delete()

@bot.command()
async def Mot(ctx):
    if 'word' in Motus[ctx.guild.name]['motus'].keys():
        await ctx.send("```Le mot actuel contient "+str(len(Motus[ctx.guild.name]['motus']['word']))+" lettres et commence par un "+str(Motus[ctx.guild.name]['motus']['word'][0])+"```")
    else:
        await ctx.send("```Il n'y a pas de mot actuellement```")
    return

@bot.command()
async def Mstatus(ctx):
    name = ctx.guild.name
    await displayStatus(name,ctx.message)
    await ctx.message.delete()

async def motus(message):
    if message.channel.guild.name in Motus.keys():
        name=message.channel.guild.name
        if message.channel.id in Motus[name]['channels']:
            if message.content.isupper():
                if 'word' in Motus[name]['motus'].keys():
                    print(message.channel.guild.name+'  '+str(message.author.display_name)+'  '+message.content)
                    if not(str(message.author.id)==Motus[name]['motus']['author']) or message.author.id == Elvin:
                        word=message.content#here word is the word given by a person that's trying to find the real word
                        if len(word)==len(Motus[name]['motus']['word']):
                            if word[0]==Motus[name]['motus']['word'][0]:
                                if dico.check(word):
                                    state = check_word(word,Motus[name]['motus']['word'])
                                    await updateStatus(state,name,message = message)
                                    temp = convert(state,word)
                                    good = temp[1]
                                    text = temp[0]
                                    await message.channel.send(text)
                                    if good == len(Motus[name]['motus']['word']):
                                        await message.channel.send("Bravo,"+message.author.mention+"!")
                                        del Motus[name]['motus']['word']
                                        del Motus[name]['motus']['author']
                                        del Motus[name]['motus']['status']
                                        Motus[name]['motus']['winner'] = message.author.id
                                        save_motus(name)
                                        Motus[name] = load_motus(name)
                                        channel = message.channel
                                else:
                                    await message.delete(delay=20)
                                    await message.channel.send("```Ce mot n'existe pas```",delete_after=20)
                            else:
                                await message.delete(delay=20)
                                await message.channel.send("```Tu dois donner un mot avec "+Motus[name]['motus']['word'][0]+" comme première lettre```",delete_after=20)
                        else:
                            await message.delete(delay=20)
                            await message.channel.send("```La taille de ton mot est ("+str(len(word))+") ce qui est différent de la taille du mot à trouver, pour rappel le mot actuel contient "+str(len(Motus[message.channel.guild.name]['motus']['word']))+" lettres et commence avec un "+str(Motus[message.channel.guild.name]['motus']['word'][0])+"```",delete_after=20)
                    else:
                        await message.delete(delay=20)
                        await message.channel.send("```Le mot à chercher est le tien, tu ne peux pas essayer de le trouver, cependant tu peux le passer avec la commande $Mpasse```",delete_after=20)
                else:
                    await message.delete(delay=20)
                    await message.channel.send("```Il n'y a pas de mot à trouver actuellement, merci de donner un mot afin que les autres puissent essayer de le trouver```",delete_after=20)
        else:
            return
