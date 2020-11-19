from inspect import getsourcefile
import os.path as path, sys
current_dir = path.dirname(path.abspath(getsourcefile(lambda:0)))
sys.path.insert(0, current_dir[:current_dir.rfind(path.sep)])
from init import*  # Replace "my_module" here with the module name.
sys.path.pop(0)

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
								Motus[guild_name]['motus'][temp[0]]=temp[1]
		if guild=='all':
			return Motus
		else:
			return Motus[guild]
	return {}

def save_motus(guild):
	print('before')
	with open(guild + '/Motus.txt','w+') as MotusFile:
		print(Motus)
		for key in Motus[guild]['motus'].keys():
			MotusFile.write(key + ':' + str(Motus[guild]['motus'][key]) + '\n')
			print(key + ':' + str(Motus[guild]['motus'][key]) + '\n')

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

def convert(state):
	good = 0
	text = ''
	for i in range(len(state)):
		if state[i] == 0:
			text += ':x:'
		if state[i] == 1:
			text += ':large_orange_diamond:'
		if state[i] == 2:
			good += 1
			text += ':red_circle:'
	return [text,good]

async def motus(message):
	global Motus
	#print(globals().keys())
	#print(Motus)

	if message.content.startswith('$Motus'):
		m_temp=message
		temp=m_temp.content.split(' ')
		if len(temp)==3:
			try:
				ID=int(temp[1])
			except:
				await message.channel.send("```Tu dois d'abord donner l'id du serveur```")
				return
			word=temp[2]
			if os.path.exists("Guilds.txt"):
				with open("Guilds.txt",'r') as GuildFile:
					for line in GuildFile:
						temp_guild=line.split(':')
						if int(temp_guild[1])==ID:
							name=temp_guild[0]
			else:
				await message.channel.send("```Motus n'a pas encore été activé```")
				return
		if len(temp)==3:
			if word.isupper() and word.isalpha():
				if dico.check(word):
					if not('word' in Motus[name]['motus'].keys()):
						print(m_temp.author.id)
						if (not('winner' in Motus[name]['motus'].keys()) or (('winner' in Motus[name]['motus'].keys()) and Motus[name]['motus']['winner']==str(m_temp.author.id))):
							if len(word)>=5 and len(word)<=15:
								Motus[name]['motus']['word']=word
								Motus[name]['motus']['author']=str(m_temp.author.id)
								save_motus(name)
								await m_temp.channel.send("```Ton mot est enregistré```")
							else:
								await m_temp.channel.send("```Le mot doit avoir une longueur comprise entre 5 lettres et 15 lettres```")
						else:
							await m_temp.channel.send("```Tu n'es pas le dernier vainqueur```")
					else:
						await m_temp.channel.send("```Il y a déjà un mot, tu dois le trouver avant de pouvoir en proposer un```")
				else:
					await m_temp.channel.send("```Ce mot n'existe pas ou n'est pas dans le dictionnaire```")
			else:
				await m_temp.channel.send("```Tu dois donner le mot en majuscules```")
		else:
			await m_temp.channel.send("```Tu ne dois donner que des lettres```")
		return


	elif message.content=='$Mrecharge':
		if message.author.id==281432668196044800:
			await message.channel.send("```Rechargé```")
			Motus = {}
			Motus = load_motus()

	elif message.content=='$Msupprime':
		if message.author.id==281432668196044800:
			with open("Motus.txt",'w+') as MotusFile:
				MotusFile.write('')
			await message.channel.send("```Supprimé```")

	elif message.content=='$Mliste':
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
				await message.channel.send(str(nServer)+t+text)
		else:
			await message.channel.send("```Aucun serveur enregistré```")
#----------------------------------------------------------------------------------------------------------------------------------
	try:
		message.channel.name
	except:
		print("exit")
		return
#----------------------------------------------------------------------------------------------------------------------------------
	if message.content=='$Maide':
		await message.channel.send("```$Mactiver : pour que les administrateurs activent Motus dans un canal \n\n$Passe : pour que les administrateurs sautent un mot s'il est trop compliqué \n\n$Mot : pour voir quels sont les conseils du mot actuel \n\n$Mchannel : pour voir dans quels canaux Motus a été activé \n\n$Mid : pour obtenir l'identifiant du serveur  \n\n$Motus : à faire en message privé au bot pour donner le mot à trouver, ne fonctionne que si Motus vient d'être activé ou si vous trouvez le dernier mot```")
		return

	elif message.content=='$Mid':
		if message.channel.guild.name in Motus.keys():
			await message.channel.send("```L'id du serveur est : "+str(message.channel.guild.id)+"```")
		else:
			await message.channel.send("```Motus n'a pas encore été activé sur ce serveur```")
		return

	elif message.content=='$Mactiver':
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
					await message.channel.send("```Motus a été activé correctement```")
				else:
					await message.channel.send("```Motus est déjà activé sur ce channel```")
					return
			with open(str(guild.name)+'/Motus.txt','a+') as MotusFile:#used to create the motus.txt file used to avoid bugs after
				pass
			Motus[guild.name]=load_motus(guild.name)
		else:
			await message.channel.send("```Tu n'as pas la permission pour cette commande```",delete_after=20)
		return

	elif message.content=='$Mpasse':
		if message.author.guild_permissions.administrator:
			if 'word' in Motus[message.channel.guild.name]['motus'].keys():
				await message.channel.send("W.I.P")
		return

	elif message.content=='$Mot':
		if 'word' in Motus[message.channel.guild.name]['motus'].keys():
			await message.channel.send("```Le mot actuel contient "+str(len(Motus[message.channel.guild.name]['motus']['word']))+" lettres et commence par un "+str(Motus[message.channel.guild.name]['motus']['word'][0])+"```")
		else:
			await message.channel.send("```Il n'y a pas de mot actuellement```")
		return

	elif message.content.startswith('$quit'):
		if message.author.guild_permissions.administrator:
			await message.channel.send('Déconnection...')
			await client.logout()
		return

	if message.channel.guild.name in Motus.keys():
		name=message.channel.guild.name
		if message.channel.id in Motus[name]['channels']:
			if message.content.isupper():
				if 'word' in Motus[name]['motus'].keys():
					print(message.channel.guild.name+'  '+str(message.author.display_name)+'  '+message.content)
					if not(str(message.author.id)==Motus[name]['motus']['author']):
						word=message.content#here word is the word given by a person that's trying to find the real word
						if len(word)==len(Motus[name]['motus']['word']):
							if word[0]==Motus[name]['motus']['word'][0]:
								if dico.check(word):
									state = check_word(word,Motus[name]['motus']['word'])
									temp = convert(state)
									good = temp[1]
									text = temp[0]
									await message.channel.send(text)
									if good==len(Motus[name]['motus']['word']):
										await message.channel.send('before message')
										await message.channel.send("Bravo," + message.author.mention+"!")
										await message.channel.send('before del 1')
										del Motus[name]['motus']['word']
										await message.channel.send('before del 2')
										del Motus[name]['motus']['author']
										await message.channel.send("before author id")
										Motus[name]['motus']['winner'] = message.author.id
										await message.channel.send("before save")
										save_motus(name)
										Motus[name] = load_motus(name)
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
