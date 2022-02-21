from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from init import*  # Replace "my_module" here with the module name.
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
                    if os.path.exists(guild_name+'/Motus.json'):
                        with open(guild_name+"/Motus.json",'r') as MotusFile:
                            Motus[guild_name]['motus'] = json.load(MotusFile)
                    if os.path.exists(guild_name+'/players.json'):
                        with open(guild_name+'/players.json','r') as PlayersFile:
                            Motus[guild_name]['players'] = json.load(PlayersFile)
        if guild=='all':
            return Motus
        else:
            return Motus[guild]
    return {}

def save_motus(guild):
    try:
        with open(guild+'/Motus.json','w') as MotusFile:
            json.dump(Motus[guild]['motus'], MotusFile)
        with open(guild+'/players.json','w') as PlayersFile:
            json.dump(Motus[guild]['players'], PlayersFile)
    except:
        time.sleep(2)
        save_motus(guild)

def check_word(given_word,word):#given_word=word word=Motus[name]['motus']['word']
    state = []#0=:x: 1=:large_orange_diamond: 2= the corresponding letter 3= dash
    word_list = list(word)
    for i in range(len(given_word)):
        state.append(0)
    for i in range(len(given_word)):
        if word[i] == '-':
            word_list[i] = '!'
            state[i] = 3
        elif given_word[i] == word[i]:
            word_list[i] = '!'
            state[i] = 2
    for i in range(len(given_word)):
        if given_word[i] in word_list and state[i] < 2:
            index = word_list.index(given_word[i])
            word_list[index] = '!'
            state[i] = 1
        elif state[i] < 2:
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
        if state[i] == 3:
            good += 1
            text += ':heavy_minus_sign:'
    return [text,good]

async def updateStatus(state,guild,message = None):
    word = Motus[guild]['motus']['word']
    change = False
    if not('status' in Motus[guild]['motus'].keys()) or len(Motus[guild]['motus']['status']) != len(word):
        Motus[guild]['motus']['status'] = []
        for i in range(len(word)):
            Motus[guild]['motus']['status'].append('0')
    status = Motus[guild]['motus']['status']
    count = 0
    for i in range(len(word)):
        if status[i] == '0':
            if state[i] == 2:
                status[i] = '2'
                count += 1
                change = True
            if state[i] == 3:
                status[i] = '3'
    Motus[guild]['motus']['status'] = status
    return count

async def displayStatus(guild,message):
    text = ''
    if 'status' in Motus[guild]['motus'].keys():
        status = Motus[guild]['motus']['status']
    else:
        await message.channel.send("```There is no status yet```")
        return
    word = Motus[guild]['motus']['word']
    for i in range(len(status)):
        if status[i] == '2':
            text += ':regional_indicator_' + word[i].lower() + ':'
        elif status[i] == '3':
            text += ':heavy_minus_sign:'
        else:
            text += ':x:'
    await message.channel.send("```Le status actuel du mot est :```")
    await message.channel.send(text)


async def motus(message):
    global Motus

def get_guild(id):
    name = None
    if os.path.exists("Guilds.txt"):
        with open("Guilds.txt",'r') as GuildFile:
            for line in GuildFile:
                temp_guild = line.split(':')
                if int(temp_guild[1]) == id:
                    name = temp_guild[0]
    return name

@bot.command(name = 'Motus')
async def fMotus(ctx,*args):
    temp = args
    if len(temp) >= 1:
        ID = int(temp[0])
        word = temp[1]
        name = get_guild(ID)
        if name is None:
            await ctx.send("```Motus n'a pas encore été activé```")
            return
    else:
        await ctx.send("```Tu dois d'abord donner l'id du serveur```")
        return
    if len(temp) == 2:
        for letter in word:
            if letter not in al:
                await ctx.send("```Tu ne dois donner que des lettres```")
                return
        if dico.check(word):
            if not('word' in Motus[name]['motus'].keys()):
                if 'winner' in Motus[name]['motus'].keys() and (Motus[name]['motus']['winner'] == ctx.author.id or Motus[name]['motus']['winner'] == -1):
                    if len(word)>=2 and len(word)<=17:
                        Motus[name]['motus']['word'] = word
                        Motus[name]['motus']['author'] = ctx.author.id
                        Motus[name]['motus']['players'] = {}
                        Motus[name]['motus']['counter'] = 0
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
    await ctx.send(
    """```$Mactiver : pour que les administrateurs activent Motus dans un canal \n
    $Passe : pour que les administrateurs sautent un mot s'il est trop compliqué \n
    $Mot : pour voir quels sont les conseils du mot actuel \n
    $Mchannel : pour voir dans quels canaux Motus a été activé \n
    $Mid : pour obtenir l'identifiant du serveur  \n
    $Mstatus : pour obtenir l'état du mot rechercher (quelles lettres on déjà été trouvées) \n
    $Mleaderboard : pour obtenir le classement des gens qui ont jouer depuis la mise en place du système de point \n
    $Motus : à faire en message privé au bot pour donner le mot à trouver, ne fonctionne que si Motus vient d'être activé ou si vous trouvez le dernier mot```""")
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
        with open(str(guild.name)+'/Motus.json','a+') as MotusFile:#used to create the motus.txt file used to avoid bugs after
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
        name = ctx.channel.guild.name
        await ctx.send("```Le mot a été passé, n'importe qui peut en remettre un```")
        del Motus[name]['motus']['word']
        del Motus[name]['motus']['author']
        del Motus[name]['motus']['status']
        del Motus[name]['motus']['players']
        del Motus[name]['motus']['counter']
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

async def send_points(message,name):
    guild = message.channel.guild
    text = ""
    list_players = [[player, points] for player, points in Motus[name]['motus']['players'].items()]
    list_players.sort(key = lambda x: x[1])
    list_players.append([Motus[name]['motus']['author'],Motus[name]['motus']['counter']])
    for player in list_players:
        text += f"{guild.get_member(int(player[0])).nick} gagne {player[1]} point{'s' if player[1] > 1 else ''}\n"
    await message.channel.send(f"```{text}```")

def add_points(name):
    list_players = Motus[name]['motus']['players'].items()
    for player, points in list_players:
        if player in Motus[name]['players'].keys():
            Motus[name]['players'][player] += points
        else:
            Motus[name]['players'][player] = points
    author_id = str(Motus[name]['motus']['author'])
    if author_id in Motus[name]['players'].keys():
        Motus[name]['players'][author_id] += Motus[name]['motus']['counter']
    else:
        Motus[name]['players'][author_id] = Motus[name]['motus']['counter']


@bot.command()
async def Mleaderboard(ctx):
    if ctx.channel.guild.name in Motus.keys():
        name=ctx.channel.guild.name
        guild = ctx.channel.guild
        text = ""
        list_players = [[id, points] for id, points in Motus[name]['players'].items()]
        list_players.sort(key = lambda x: x[1])
        for index,player in enumerate(list_players[::-1]):
            text += f"#{index+1} {guild.get_member(int(player[0])).nick} a {player[1]} points\n"
        await ctx.channel.send(f"```{text}```")

async def motus(message):
    if message.channel.guild.name in Motus.keys():
        name=message.channel.guild.name
        if message.channel.id in Motus[name]['channels']:
            word = message.content
            if '-' in word:
                temp = ''.join(word.split('-'))
            else:
                temp = word
            if temp.isupper():
                for letter in word:
                    if letter not in al:
                        await message.delete(delay=20)
                        await message.channel.send("```Tu ne dois donner que des lettres```",delete_after = 20)
                        return
            else:
                return
            if 'word' in Motus[name]['motus'].keys():
                print(message.channel.guild.name+'  '+str(message.author.display_name)+'  '+message.content)
                if not(str(message.author.id)==Motus[name]['motus']['author']) or message.author.id == Elvin:
                    word=message.content#here word is the word given by a person that's trying to find the real word
                    if len(word)==len(Motus[name]['motus']['word']):
                        if word[0]==Motus[name]['motus']['word'][0]:
                            if dico.check(word):
                                Motus[name]['motus']['counter'] += 1
                                state = check_word(word,Motus[name]['motus']['word'])
                                count = await updateStatus(state,name,message = message)
                                if str(message.author.id) in Motus[name]['motus']['players'].keys():
                                    Motus[name]['motus']['players'][str(message.author.id)] += count
                                else:
                                    Motus[name]['motus']['players'][str(message.author.id)] = count
                                save_motus(name)
                                temp = convert(state,word)
                                good = temp[1]
                                text = temp[0]
                                await message.channel.send(text)
                                if good == len(Motus[name]['motus']['word']):
                                    if str(message.author.id) in Motus[name]['motus']['players'].keys():
                                        Motus[name]['motus']['players'][str(message.author.id)] += int(len(Motus[name]['motus']['word'])/2)
                                    else:
                                        Motus[name]['motus']['players'][str(message.author.id)] = int(len(Motus[name]['motus']['word'])/2)
                                    await message.channel.send(f"Bravo,{message.author.mention}!\n le mot a été trouvé en {Motus[name]['motus']['counter']} essais")
                                    await send_points(message,name)
                                    add_points(name)
                                    try:
                                        await message.author.send(f"Tu as gagné, il te faut maintenant me renvoyer cette commande\n$Motus {message.guild.id} TONMOT")
                                    except:
                                        await message.channel.send(f"{message.author.mention} il semblerait que je ne puisse pas t'envoyer de message, il faut que tu me débloque pour que tu puisse mettre un mot en utilisant la commande \n$Motus {message.guild.id} TONMOT")
                                    del Motus[name]['motus']['word']
                                    del Motus[name]['motus']['author']
                                    del Motus[name]['motus']['status']
                                    del Motus[name]['motus']['players']
                                    del Motus[name]['motus']['counter']
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
