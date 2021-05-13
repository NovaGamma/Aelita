class Board():
    def __init__(self,player,type = ""):
        self.board = []
        self.players = [player]
        self.type = type
        if type == "tictactoe":
            self.createBoardT()
        elif type == "4x4":
            self.createBoard4()
        self.nMove = 0

    async def addPlayer(self,member):
        if len(self.players) < 2:
            self.players.append(member)
        if len(self.players) == 2:
            await self.message[-1].remove_reaction("✅",bot.user)
            if self.type == "4x4":
                n = 7
            elif self.type == "tictactoe":
                n = 9
            for i in range(n):
                emoji = number_list[i]
                await self.message[-1].add_reaction(emoji)
            player = random.randint(0,1)
            text = f"{self.players[player].mention}'s Turn"
            if player == 1:
                self.players.insert(0,self.players[player])
                self.players.pop(2)
            await self.turn_message.edit(content = text)

    def createBoard(self,sizeX,sizeY):
        board = []
        for i in range(sizeY):
            temp = []
            for j in range(sizeX):
                temp.append('⬛')
            board.append(temp)
        self.board = board

    def __repr__(self):
        text = ''
        for i in (self.board):
            for j in i:
                text += j
            text += '\n'
        text.lstrip('\n')
        return text

    async def edit(self,placed):
        text = self.board[placed]
        text = ''.join(text)
        await self.message[placed].edit(content = text)
