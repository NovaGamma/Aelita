from init import*

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
            text = f"{self.players[player].mention}'s Turn 🟡"
            if player == 1:
                self.players.insert(0,self.players[player])
                self.players.pop(2)
            await self.turn_message.edit(content = text)

    def createBoardT(self):
        board = []
        temp = []
        for i in range(0,9):
            temp.append(number_list[i])
            if (i+1)%3 == 0:
                board.append(temp)
                temp = []
        self.board = board

    def createBoard4(self):
        board = []
        for i in range(6):
            temp = []
            for j in range(7):
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

def checkRowsT(board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return 0

def checkDiagonalsT(board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return 0

def checkWinT(board):
    import numpy as np
    #transposition to check rows, then columns
    for newBoard in [board, np.transpose(board)]:
        result = checkRowsT(newBoard)
        if result:
            return result
    return checkDiagonalsT(board)

def checkDiagonals4(board,sign):
    import numpy as np
    for i in range(3,6):
        for j in range(0,4):
            if board[i][j]==sign and board[i-1][j+1]==sign and board[i-2][j+2]==sign and board[i-3][j+3]==sign:
                return 1
    for i in range(len(board)):
        board[i] = np.flip(board[i])
    for i in range(3,6):
        for j in range(0,4):
            if board[i][j]==sign and board[i-1][j+1]==sign and board[i-2][j+2]==sign and board[i-3][j+3]==sign:
                return 1
    return 0

def checkRows4(board,sign):
    for i in range(len(board)):
        for j in range(len(board[i])-3):
            if board[i][j]==sign and board[i][j+1]==sign and board[i][j+2]==sign and board[i][j+3]==sign:
                return 1
    return 0

def checkWin4(board,sign):
    import numpy as np
    from copy import deepcopy
    for newBoard in [board, np.transpose(board)]:
        result = checkRows4(newBoard,sign)
        if result:
            return result
    return checkDiagonals4(deepcopy(board),sign)

async def PlaceT(ctx,user):
    number = number_list.index(ctx.emoji)
    game = False
    for i in Games:
        if user in i.players:
            game = i
    if not game:
        return
    if user in game.players:
        player_index = game.players.index(user)
    else:
        print('User not found')
        return
    if player_index == game.nMove%2:
        if game.type == "tictactoe":
            if game.board[(number)//3][number%3] in number_list:
                game.board[(number)//3][number%3] = '❌' if player_index == 0 else '⭕'
            else:
                await ctx.message.channel.send("You can't play here",delete_after = 10)
                return
            text = str(game)
            await game.message[0].edit(content = text)
            if checkWinT(game.board):
                await ctx.message.channel.send(f"{game.players[player_index].mention} won")
                Games.remove(game)
            elif game.nMove == 9 and game.type == "tictactoe":
                await ctx.message.channel.send("It's a draw !")
                Games.remove(game)

        elif game.type == "4x4":
            placed = False
            pos = 0
            if game.board[0][number] == '⬛':
                for i in range(5):
                    if game.board[i+1][number] != '⬛' and not placed:
                        game.board[i][number] = '🟡' if player_index == 0 else '🔴'
                        placed = True
                        pos = i
                if not placed:
                    if game.board[i+1][number] == '⬛':
                        game.board[5][number] = '🟡' if player_index == 0 else '🔴'
                        pos = 5
                    else:
                        await ctx.message.channel.send("You can't play here",delete_after = 10)
                        return
            else:
                await ctx.message.channel.send("You can't play here",delete_after = 10)
                return
            await game.edit(pos)
            if checkWin4(game.board,'🟡' if player_index == 0 else '🔴'):
                await ctx.message.channel.send(f"{game.players[player_index].mention} won")
                Games.remove(game)
                return
        game.nMove += 1
        if player_index == 0:
            text = f"{game.players[1].mention}'s Turn  🔴"
        else:
            text = f"{game.players[0].mention}'s Turn  🟡"
        await game.turn_message.edit(content = text)
    else:
        await ctx.message.channel.send("Sorry not your turn to play",delete_after = 10)

def reset():
    Games = []

async def InitBoardT(ctx,author):
    game = Board(author,'tictactoe')
    Games.append(game)
    text = f"{author.mention}'s game"
    game.turn_message = await ctx.send(text)
    text = str(game)
    game.message = [await ctx.send(text)]
    await game.message[0].add_reaction("✅")

async def InitBoard4(ctx,author):
    game = Board(author,'4x4')
    Games.append(game)
    text = f"{author.mention}'s game"
    game.turn_message = await ctx.send(text)
    text = str(game).split("\n")
    text.pop(len(text)-1)
    game.message = []
    await ctx.send("".join(number_list[:7]))
    for line in text:
        temp = await ctx.send(line)
        game.message.append(temp)
    await game.message[-1].add_reaction("✅")

@bot.command()
async def Tic(ctx):
    await tictactoe.InitBoardT(ctx,ctx.message.author)

@bot.command()
async def P4(ctx):
    await tictactoe.InitBoard4(ctx,ctx.message.author)
