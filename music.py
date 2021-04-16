from init import*

def paste():
    keyboard.press(Key.ctrl)
    keyboard.press('v')
    keyboard.release(Key.ctrl)
    keyboard.release('v')
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

def getMusic(path):
    path = path
    dirs = os.listdir(path)
    dirs.remove('desktop.ini')
    dirs.remove('Playlists')
    dirs.remove('Coldplay')
    total = []
    for dir in dirs:
        albums = os.listdir(path+'/'+dir)
        for album in albums:
            musics = [i.rstrip('.mp3') for i in os.listdir(path+'/'+dir+'/'+album) if i.endswith('.mp3')]
            for music in musics:
                if music[:2].isdigit():
                    music = music[2:].lstrip()
                if music[:2].isdigit():
                    music = music[2:].lstrip()
                total.append(dir + ' ' + music)
    return total

def get(number,total):
    choosed = []
    for i in range(number):
        choosed.append('-p '+random.choice(total))
    return choosed

@bot.command()
async def get_history(ctx):
    import json
    list = []
    i = 0
    async for message in ctx.channel.history(limit = 10000):
        print(i)
        i+=1
        if message.content.startswith('-p'):
            content = message.content.lstrip('-p')
            list.append(content)
    with open('data.json','w') as file:
        json.dump(list,file)

@bot.command()
async def music(ctx,number):
    if ctx.author.id == Elvin:
        path = "C:/Users/NovaGamma/Music"
        music = getMusic(path)
        list = get(int(number),music)
        print(list)
        for i in list:
            print(i)
            pyperclip.copy(i)
            pyperclip.paste()
            paste()
            time.sleep(0.5)

@bot.command()
async def randomMusic(ctx,number = 1):

    with open('cleaned4.json','r') as file:
        data = json.load(file)
    list = []
    for i in range(int(number)):
        list.append(random.choice(data))
    if ctx.author.id == Elvin:
        for i in list:
            pyperclip.copy(f"-p {i}")
            pyperclip.paste()
            paste()
            time.sleep(0.5)
    else:
        await ctx.channel.send(f"```-p {list[0]}```")
