import discord
from datetime import datetime
import os

def load():
    if os.path.exists('Stats.txt'):
        with open("Stats.txt",'r') as StatsFile:
            Stats={}
            for line in StatsFile:
                temp=line.split(':')
                if temp[0]=='time':
                    Stats['time']=datetime.fromisoformat(temp[1])
                elif temp[0]=='total':
                    Stats['total']=int(temp[1])
                else:
                    Stats[int(temp[0])]=int(temp[1])
        return Stats
    return {}

def save():
    with open("Stats.txt",'w+') as StatsFile:
        for key in Stats.keys():
            StatsFile.write(str(key)+':'+str(Stats[key])+'\n')

async def count(message,channel=None):
    if channel==None:
        channel=message.channel
    if not('time' in Stats.keys()):
        Stats['time']=None
    if 'total' in Stats.keys():
        first=Stats['total']
        total_messages=first
    else:
        total_messages=0
        first=0
    async for Message in channel.history(limit=10000,after=Stats['time']):
        if Message.content.isdecimal():
            if not(Message.author.id in Stats.keys()):
                Stats[Message.author.id]=1
                total_messages+=1
            else:
                Stats[Message.author.id]+=1
                total_messages+=1
            print(Message.created_at)
            Stats['time']=message.created_at
    await message.channel.send("```Found : "+str(total_messages-first)+" messages```")
    Stats['total']=total_messages
    print(Stats)
    save()

def load_motus(guild='all'):
    Motus={}
    if os.path.exists('Guilds.txt'):
        with open("Guilds.txt",'r') as GuildFile:
            for line in GuildFile:
                temp=line.split(':')
                guild_name=temp[0]
                if guild_name==guild or guild=='all':
                    with open(guild_name+'/channel.txt','r') as ChannelFile:
                        Channels=[]
                        for line in ChannelFile:
                            temp=line.rstrip('\n')
                            Channels.append(temp)
                    Motus[guild_name]={}
                    Motus[guild_name]['channels']=Channels
                    if os.path.exists(guild_name+'/Motus.txt'):
                        with open(guild_name+"/Motus.txt",'r') as MotusFile:
                            Motus[guild_name]['motus']={}
                            for line in MotusFile:
                                temp=line.split(':')
                                temp[1]=temp[1].rstrip('\n')
                                Motus[guild_name]['motus'][temp[0]]=temp[1]
        if guild=='all':
            return Motus
        else:
            return Motus[guild]
    return {}

def save_motus(guild):
    with open(guild+'/Motus.txt','w+') as MotusFile:
        for key in Motus[guild]['motus'].keys():
            MotusFile.write(key+':'+str(Motus[guild]['motus'][key])+'\n')

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    global Motus

    if message.author == client.user:
        return

    if message.content.startswith('£id'):
        print(message.author.id)
    
    if message.content.startswith('£Motus'):
        m_temp=message
        temp=m_temp.content.split(' ')
        print(len(temp))
        print(temp)
        if len(temp)==3:
            try:
                ID=int(temp[1])
            except:
                await message.channel.send("You have to give the id of the server in first parameters")
                return
            word=temp[2]
            if os.path.exists("Guilds.txt"):
                with open("Guilds.txt",'r') as GuildFile:
                    for line in GuildFile:
                        temp_guild=line.split(':')
                        if int(temp_guild[1])==ID:
                            name=temp_guild[0]
            else:
                await message.channel.send("Motus hasn't been activated anywhere")
                return
        print(len(temp))
        print(temp)
        if len(temp)==3:
            try:
                word.encode(encoding="ascii")
            except:
                await message.channel.send("No special characters please")
                return
            if word.isupper() and word.isalpha():
                print(Motus.keys())
                if not('word' in Motus[name]['motus'].keys()):
                    print(m_temp.author.id)
                    if (not('winner' in Motus[name]['motus'].keys()) or (('winner' in Motus[name]['motus'].keys()) and Motus[name]['motus']['winner']==str(m_temp.author.id))):
                        if len(word)>=5 and len(word)<=15:
                            Motus[name]['motus']['word']=word
                            Motus[name]['motus']['author']=m_temp.author.id
                            save_motus(name)
                            await m_temp.channel.send("```Your word has been taken```")
                        else:
                            await m_temp.channel.send("```The word must be at least 5 letters long and at max 10 letters long```")
                    else:
                        await m_temp.channel.send("```You aren't the last winner```")
                else:
                    await m_temp.channel.send("```There is already a word, you have to find it before you can ask another one```")
            else:
                await m_temp.channel.send("```You must give the word in uppercase or in letters```")
        else:
            await m_temp.channel.send("```You must give only one word```")
        return

    if message.content=='£reload':
        if message.author.id==281432668196044800:
            await message.channel.send("```Reloaded```")
            global Stats
            Stats={}
            Stats=load()

    if message.content=='£Mreload':
        if message.author.id==281432668196044800:
            await message.channel.send("```Reloaded```")
            Motus={}
            Motus=load_motus()

    if message.content=='£Mclean':
        if message.author.id==281432668196044800:
            with open("Motus.txt",'w+') as MotusFile:
                MotusFile.write('')
            await message.channel.send("```Cleaned```")

    if message.content=='£clean':
        if message.author.id==281432668196044800:
            with open("Stats.txt",'w+') as StatsFile:
                StatsFile.write('')
            await message.channel.send("```Cleaned```")

    if message.content=='£Mlist':
        if os.path.exists('Guilds.txt'):
            with open('Guilds.txt','r') as GuildFile:
                text='```'
                nServer=0
                for line in GuildFile:
                    nServer+=1
                    temp=line.split(':')
                    text+='Name : '+temp[0]+'   Id : '+temp[1]
                if nServer==1:
                    t=' Server found\n'
                else:
                    t=' Servers found\n'
                await message.channel.send(str(nServer)+t+text+'```')
        else:
            await message.channel.send("No server registered yet")
#----------------------------------------------------------------------------------------------------------------------------------
    try:
        message.channel.name
    except:
        return
#----------------------------------------------------------------------------------------------------------------------------------
    if message.content=='£Mhelp':
        await message.channel.send("```£Mactivate : for administrators to activate Motus in a channel\n\n£Skip : for administrators to skip a word if it is too complicated\n\n£Mword : to see what the current word hints are\n\n£Mchannel : to see in which channels Motus has been activated\n\n£Mid : to get the id of the server\n\n£Motus : to do in private message to the bot to give the word to find, works only if Motus just have been activated or if you find the last word```")
        return

    if message.content=='£Mid':
        if message.channel.guild.name in Motus.keys():
            await message.channel.send("The id of the server is : "+str(message.channel.guild.id))
        else:
            await message.channel.send("Motus hasn't been activated anywhere in this server")
        return

    if message.content=='£Mactivate':
        if message.author.guild_permissions.administrator:
            iD=message.channel.id
            guild=message.channel.guild
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
                    await message.channel.send("Motus has been correctly activated")
                else:
                    await message.channel.send("Motus has already been activated in this channel")
                    return
            with open(str(guild.name)+'/Motus.txt','a+') as MotusFile:#used to create the motus.txt file used to avoid bugs after
                pass
            print(id,guild)
        else:
            await message.channel.send("```You don't have the permission to run this command```",delete_after=20)
        return

    if message.content=='£Mskip':
        if message.author.guild_permissions.administrator:
            if 'word' in Motus[message.channel.guild.name]['motus'].keys():
                await message.channel.send("W.I.P")
        return

    if message.content.startswith('£delete'):
        if message.author.guild_permissions.administrator:
            if message.content.startswith('£delete bot'):
                temp=message.content.split(' ')
                number=int(temp[2])
                messages = await message.channel.history(limit=number+1).flatten()
                for m in messages:
                    if m.author==client.user:
                        await m.delete()
                await message.delete()
            else:
                temp=message.content.split(' ')
                number=int(temp[1])
                messages = await message.channel.history(limit=number+1).flatten()
                for m in messages:
                    await m.delete()
        else:
            await message.delete()
        return
    #10000 part

    if message.channel.name=='1000':
        channel=message.channel
        if not(message.content.isdecimal()):
            author=message.author
            mention=author.mention
            if len(message.content)==1:
                await message.delete()
            else:
                await message.channel.send(message.content+'\n'+mention+" You must follow the rules don't write other messages than numbers in this channel\n This message will auto-destruct in 1 minute```",delete_after=60)
                await message.delete()
        else:
            number=int(message.content)
            author=message.author
            mention=author.mention
            messages = await channel.history(limit=10).flatten()
            m=0
            while messages[1].author==client.user and m<8:
                m+=1
                del messages[1]
            if m==8:
                messages = await channel.history(limit=100).flatten()
                m=0
                while messages[1].author==client.user and m<98:
                    m+=1
                    del messages[1]
            if messages[1].author!=client.user:
                message_number=int(messages[1].content)
                if not(messages[1]==message):
                    if message_number==number or len(messages[1].content)!=len(message.content):
                        await message.delete()
                        await message.channel.send(mention+"``` This number has already been wrotten, your too late\n This message will auto-destruct in 1 minute```",delete_after=60)
                    elif not(number-1==message_number):
                        await message.delete()
                        await message.channel.send(mention+"``` You must write the next number not another number\n This message will auto-destruct in 1 minute```",delete_after=60)
                    elif author==messages[1].author:
                        await message.delete()
                        await message.channel.send(mention+"``` You can't wrote a number two times in a row\n This message will auto-destruct in 1 minute```",delete_after=60)
        return

    if message.content=='£Mword':
        if 'word' in Motus[message.channel.guild.name]['motus'].keys():
            await message.channel.send("```The current word contains "+str(len(Motus[message.channel.guild.name]['motus']['word']))+" letters and start with a "+str(Motus[message.channel.guild.name]['motus']['word'][0])+"```")
        return

    if message.content.startswith('£channel'):
        await message.channel.send('```the current channel is : '+message.channel.name+"```")
        return
    
    if message.content.startswith('£hello'):
        await message.channel.send('Hello!')
        return

    if message.content.startswith('£quit'):
        if message.author.guild_permissions.administrator:
            await message.channel.send('Disconnecting...')
            await client.logout()
        return

    if message.content.startswith('£count'):
        if len(message.channel_mentions)>0:
            if len(message.channel_mentions)>1:
                await message.channel.send('```You can count only in one channel at a time```')
            else:
                await message.channel.send('```Counting...```')
                await count(message,message.channel_mentions[0])
        else:
            await message.channel.send('```Counting...```')
            await count(message)
        await message.channel.send('```Finished !```')
        return
        
    if message.content.startswith('£display'):
        if message.content=='£display all':
            text='```'
            text+='the total number of messages is : '+str(Stats['total'])+'\n'
            for name in Stats.keys():
                if name!='time' and name!='total':
                    text+=str(message.channel.guild.get_member(name).nick)+' has sent '+str(Stats[name])+' messages '+str(float(int((Stats[name]/Stats['total'])*1000))/10)+'%\n'
            await message.channel.send(text+"```")

        elif message.content=='£display me':
            if message.author.id in Stats.keys():
                 await message.channel.send('You have sent '+str(Stats[message.author.id])+' messages')
            else:
                await message.channel.send("```You haven't send any messages before the last count, if you think that you have send messages then do a count before retrying```")
        elif len(message.mentions)>0:
            if len(message.mentions)>1:
                await message.channel.send('```You have to mention only one user```')
            else:
                print(message.mentions[0],message.mentions[0].name)
                if message.mentions[0].id in Stats.keys():
                    await message.channel.send('```This user has sent : '+str(Stats[message.mentions[0].id])+' messages```')
                else:
                    await message.channel.send("```This user hasn't send any messages before the last count, if you think that he has send messages then do a count before retrying```")
        else:
            await message.channel.send("```You have to mention a User or write 'me' instead of the mention, you can also check the help funcion : £help to see all other functions```") 
        return

    #motus part

    if message.channel.guild.name in Motus.keys():
        name=message.channel.guild.name
        print("channel")
        if message.channel.id in Motus[name]['channels']:
            print("channel exist")
            if message.content.isupper():
                if 'word' in Motus[name].keys():
                    print(str(message.author.id))
                    print(Motus[name]['motus']['author'])
                    if not(str(message.author.id)==Motus[name]['motus']['author']):
                        word=message.content#here word is the word given by a person that's trying to find the real word
                        if len(word)==len(Motus[name]['motus']['word']):
                            text=''
                            good=0
                            for i in range(len(Motus[name]['motus']['word'])):
                                if word[i]==Motus[name]['motus']['word'][i]:
                                    text+=':red_circle:'
                                    good+=1
                                else:
                                    if word[i] in Motus[name]['motus']['word']:
                                        text+=':large_orange_diamond:'
                                    else:
                                        text+=':black_circle:'
                            await message.channel.send(text)
                            if good==len(Motus[name]['motus']['word']):
                                await message.channel.send("Congratulation,"+message.author.mention)
                                del Motus[name]['motus']['word']
                                del Motus[name]['motus']['author']
                                Motus[name]['motus']['winner']=message.author.id
                                save_motus(name)
                                Motus[name]=load_motus(name)
                        else:
                            await message.delete(delay=20)
                            await message.channel.send("```The lenght of the given word ("+str(len(word))+") isn't the same as the word to find, as a remainder the word to find is a word in "+str(len(Motus['word']))+" letters and starting with a "+str(Motus['word'][0])+"```",delete_after=20)
                    else:
                        await message.delete(delay=20)
                        await message.channel.send("```The current word to find is yours, you can't try to find it, but you can skip it if you want using the £Mskip command```",delete_after=10)
                else:
                    await message.delete(delay=20)
                    await message.channel.send("```There is no word to find yet, please give a word to find before other people can try to find it```",delete_after=10)
        else:
            return

Stats=load()
Motus=load_motus()
print(Motus.keys())
print('bot test')
client.run('NjkxNTc4MTI0OTE1MTc5NTcw.XniAiQ.4fhrOFIBQOo2DihPBXCX33NvVn0')