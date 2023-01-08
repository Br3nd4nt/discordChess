from PIL import Image, ImageDraw, ImageFont

class ChessBoard:
    def __init__(self, name, size=8):
        self.names = {
            1: 'pawn',
            2: 'knight',
            3: 'bishop',
            4: 'rook',
            5: 'queen',
            6: 'king'
        }
        self.size = size
        self.name = name
        self.board = [[0 for x in range(size)] for y in range(size)]
        # 1 - pawn
        # 2 - knight
        # 3 - bishop
        # 4 - rook
        # 5 - queen
        # 6 - king
        for i in range(8):
            self.board[1][i] = 1
            self.board[6][i] = -1
        self.board[0][0] = 4
        self.board[0][1] = 2
        self.board[0][2] = 3
        self.board[0][3] = 5
        self.board[0][4] = 6
        self.board[0][5] = 3
        self.board[0][6] = 2
        self.board[0][7] = 4
        self.board[7][0] = -4
        self.board[7][1] = -2
        self.board[7][2] = -3
        self.board[7][3] = -5
        self.board[7][4] = -6
        self.board[7][5] = -3
        self.board[7][6] = -2
        self.board[7][7] = -4
        self.drawBoard()

    def drawBoard(self):
        image = Image.new("RGB", (64 + self.size*128, 64 + self.size*128), (240, 200, 150))
        drawBoard = ImageDraw.Draw(image)
        for x in range(self.size):
            for y in range(self.size):

                color = (240, 200, 150)
                if (x+y) % 2 == 0:
                    drawBoard.rectangle((64+x*128, 64+y*128, 64+x*128+128, 64+y*128+128), fill=(200, 150, 100))
                    color = (200, 150, 100)
                
                if self.board[y][x] != 0:
                    tmp = Image.open(f"pieces/{self.board[y][x]}.png")
                    tmp = Image.composite(tmp, Image.new('RGB', tmp.size, color), tmp)
                    image.paste(tmp, (64+x*128, 64+y*128))

        for i in range(self.size):
            drawBoard.text((64-32, 64+i*128+64), str(i+1), fill=(0, 0, 0), anchor="mm", font=ImageFont.truetype("CozetteVector.dfont", 32))
            drawBoard.text((64+i*128+64, 64-32), chr(ord('a')+i), fill=(0, 0, 0), anchor="mm", font=ImageFont.truetype("CozetteVector.dfont", 32))
        image.save(f"boards/{self.name}.png")
    
    
    def makeMove(self, move):
        figure, place = move.split(' ')
        y1, x1 = int(figure[1])-1, ord(figure[0])-ord('a')
        y2, x2 = int(place[1])-1, ord(place[0])-ord('a')
        # print(self.board[y1][x1], self.board[y2][x2])
        if self.checkMove((x1, y1), (x2, y2)):
            self.board[y2][x2] = self.board[y1][x1]
            self.board[y1][x1] = 0
            self.drawBoard()
            return f"Move made: ({self.names[abs(self.board[y2][x2])]}) {move}"
        else:
            return "invalid move!"

    def checkMove(self, figure, place):
        piece = self.board[figure[1]][figure[0]]
        if figure[0] == place[0] and figure[1] == place[1]:
            return -1
        if figure == 0:
            return -1
        #white pawn
        if piece == 1:
            if figure[1] == 1 and place[1] == 3 and figure[0] == place[0]:
                return 1
            if figure[1] == place[1]-1 and figure[0] == place[0]:
                return 1
            if figure[1] == place[1]-1 and abs(figure[0]-place[0]) == 1 and self.board[place[1]][place[0]] < 0:
                return 1
            return -1
        #black pawn
        if piece == -1:
            if figure[1] == 6 and place[1] == 4 and figure[0] == place[0]:
                return 1
            if figure[1] == place[1]+1 and figure[0] == place[0]:
                return 1
            if figure[1] == place[1]+1 and abs(figure[0]-place[0]) == 1 and self.board[place[1]][place[0]] > 0:
                return 1
            return -1
        #knight
        if piece == 2 or piece == -2:
            if abs(figure[0]-place[0]) == 2 and abs(figure[1]-place[1]) == 1:
                return 1
            if abs(figure[0]-place[0]) == 1 and abs(figure[1]-place[1]) == 2:
                return 1
            return -1
        #bishop
        if piece == 3 or piece == -3:
            if abs(figure[0]-place[0]) != abs(figure[1]-place[1]):
                return -1
            if figure[0] < place[0]:
                if figure[1] < place[1]:
                    for i in range(1, abs(figure[0]-place[0])):
                        if self.board[figure[1]+i][figure[0]+i] != 0:
                            return -1
                else:
                    for i in range(1, abs(figure[0]-place[0])):
                        if self.board[figure[1]-i][figure[0]+i] != 0:
                            return -1
            else:
                if figure[1] < place[1]:
                    for i in range(1, abs(figure[0]-place[0])):
                        if self.board[figure[1]+i][figure[0]-i] != 0:
                            return -1
                else:
                    for i in range(1, abs(figure[0]-place[0])):
                        if self.board[figure[1]-i][figure[0]-i] != 0:
                            return -1
            return 1
        #rook
        if piece == 4 or piece == -4:
            if figure[0] != place[0] and figure[1] != place[1]:
                return -1
            if figure[0] == place[0]:
                if figure[1] < place[1]:
                    for i in range(figure[1]+1, place[1]):
                        if self.board[i][figure[0]] != 0:
                            return -1
                else:
                    for i in range(place[1]+1, figure[1]):
                        if self.board[i][figure[0]] != 0:
                            return -1
            else:
                if figure[0] < place[0]:
                    for i in range(figure[0]+1, place[0]):
                        if self.board[figure[1]][i] != 0:
                            return -1
                else:
                    for i in range(place[0]+1, figure[0]):
                        if self.board[figure[1]][i] != 0:
                            return -1
            return 1
        #queen
        if piece == 5 or piece == -5:
            if figure[0] != place[0] and figure[1] != place[1]:
                if abs(figure[0]-place[0]) != abs(figure[1]-place[1]):
                    return -1
                if figure[0] < place[0]:
                    if figure[1] < place[1]:
                        for i in range(1, abs(figure[0]-place[0])):
                            if self.board[figure[1]+i][figure[0]+i] != 0:
                                return -1
                    else:
                        for i in range(1, abs(figure[0]-place[0])):
                            if self.board[figure[1]-i][figure[0]+i] != 0:
                                return -1
                else:
                    if figure[1] < place[1]:
                        for i in range(1, abs(figure[0]-place[0])):
                            if self.board[figure[1]+i][figure[0]-i] != 0:
                                return -1
                    else:
                        for i in range(1, abs(figure[0]-place[0])):
                            if self.board[figure[1]-i][figure[0]-i] != 0:
                                return -1
            else:
                if figure[0] == place[0]:
                    if figure[1] < place[1]:
                        for i in range(figure[1]+1, place[1]):
                            if self.board[i][figure[0]] != 0:
                                return -1
                    else:
                        for i in range(place[1]+1, figure[1]):
                            if self.board[i][figure[0]] != 0:
                                return -1
                else:
                    if figure[0] < place[0]:
                        for i in range(figure[0]+1, place[0]):
                            if self.board[figure[1]][i] != 0:
                                return -1
                    else:
                        for i in range(place[0]+1, figure[0]):
                            if self.board[figure[1]][i] != 0:
                                return -1
            return 1
        #king
        if piece == 6 or piece == -6:
            if abs(figure[0]-place[0]) > 1 or abs(figure[1]-place[1]) > 1:
                return -1
            return 1
        #castling
        if piece == 7 or piece == -7:
            if figure[1] != place[1]:
                return -1
            if figure[0] == 4 and place[0] == 6:
                if self.board[figure[1]][7] != 4*piece:
                    return -1
                for i in range(5, 7):
                    if self.board[figure[1]][i] != 0:
                        return -1
                return 2
            if figure[0] == 4 and place[0] == 2:
                if self.board[figure[1]][0] != 4*piece:
                    return -1
                for i in range(1, 4):
                    if self.board[figure[1]][i] != 0:
                        return -1
                return 2
            return -1
        
if __name__ == "__main__":
    chess = ChessBoard('test')
    chess.makeMove('e2 e4')
    # chess.drawBoard()
    # chess.image.show()