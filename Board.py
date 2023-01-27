
dx = [-1, 0, 1, 1]
dy = [1, 1, 1, 0]

class Board:
    def __init__(self) -> None:
        self.size = 10
        self.cell = [[0 for j in range(self.size)] for i in range(self.size)]
    
    def checkWin(self) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if self.cell[i][j] == 0: continue
                for dir in range(4):
                    check = True
                    for k in range(1, 5):
                        ni = i + k * dx[dir]
                        nj = j + k * dy[dir]
                        if ni < 0 or ni >= self.size or nj < 0 or nj >= self.size or self.cell[ni][nj] != self.cell[i][j]:
                            check = False
                            break
                    if check:
                        return True
        return False
    
    def checkDraw(self) -> bool:
        for i in range(self.size):
            for j in range(self.size):
                if self.cell[i][j] == 0:
                    return False
        return True
