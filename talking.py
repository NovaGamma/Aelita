from init import*


def Message(message,text):
    return True if message.content.startswith(text) else False


def Admin(author):
    return author.guild_permissions.administrator


class Connection:
    def __init__(self,guild,category):
        self.guild = guild
        self.category = category
        self.channels = []


class Talk:
    def __init__(self,client):
        self.guilds = client.guilds
        self.channels = None
        self.choosing = None
        self.guild = None
        self.connected = []
        self.channel = None
        self.log_channel = None

    def sending(self,message):
        for i in range(len(self.connected[0].channels)):
            if self.connected[0].channels[i][1].id == message.channel.id:
                return True
        return False

    def receiving(self,message):
        for i in range(len(self.connected[0].channels)):
            if self.connected[0].channels[i][0].id == message.channel.id:
                return True
        return False

    async def disconnect(self,ctx):
        if this.sending(ctx.message):
            return

    async def choose(self,temp,Guild):
        self.guild = self.guilds[int(temp[1])]
        if len(self.connected) == 0:
            category = await Guild.create_category(name = self.guild.name, position = 2)
            channel = self.guild.text_channels[int(temp[2])]
            self.connected = [Connection(self.guild,category)]
            log_channel = await Guild.create_text_channel(name = channel.name,category = category)
            self.connected[0].channels = [[channel,log_channel]]
        else:
            channel = self.connected[0].guild.text_channels[int(temp[2])]
            log_channel = await Guild.create_text_channel(name = channel.name,category = self.connected[0].category)
            self.connected[0].channels.append([channel, log_channel])

    async def send(self,message):
        embed = discord.Embed(description = message.content, color = 0x0e15d8)
        if len(message.attachments) != 0:
            url = message.attachments[0].url
            embed.set_image(url = url)
        for i in range(len(self.connected[0].channels)):
            channel = self.connected[0].channels[i][1]
            other = self.connected[0].channels[i][0]
            if channel.id == message.channel.id:
                await other.send(embed = embed)

    async def log(self,message):
        embed = discord.Embed(description = message.content, color = 0x0e15d8)
        embed.set_author(name = message.author.display_name, icon_url = message.author.avatar_url)
        if len(message.attachments) != 0:
            url = message.attachments[0].url
            embed.set_image(url = url)
        for i in range(len(self.connected[0].channels)):
            channel = self.connected[0].channels[i][0]
            other = self.connected[0].channels[i][1]
            if channel.id == message.channel.id:
                await other.send(embed = embed)

    async def connect(self,message):
        if message.author.id == 281432668196044800 and message.guild.name == "Stock Market":
            temp = message.content.split(" ")
            if len(temp) == 3:
                print("choosing")
                await self.choose(temp,message.guild)
