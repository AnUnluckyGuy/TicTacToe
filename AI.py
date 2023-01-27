from Board import Board
import random

class AI:
    def __init__(self, depth = 3, turn = 1) -> None:
        self.depth = depth
        self.turn = turn
        self.winScore = 100000000

    def getFirstMove(self) -> list:
        return [int(random.random() * 7 + 1), int(random.random() * 7 + 1)]
    
    # Tìm kiếm nước đi tiếp theo
    def getNextMove(self, board: Board) -> list:
        # Tìm xem liệu có nước chiến thắng luôn không
        bestMove = self.searchWinningMove(board)

        if bestMove != None:# Nếu có
            return [bestMove[1], bestMove[2]]
        else:# Nếu không thực hiện Mininmax
            bestMove = self.minimax(self.depth, board, True, -self.winScore, self.winScore)
            return [bestMove[1], bestMove[2]]

    # Tìm các ô có thể đánh tiếp (ô còn trống và nằm cạnh 1 ô đã đánh)
    def getPossibleMove(self, board: Board) -> list:
        possibleMove = []
        
        for i in range(board.size):
            for j in range(board.size):
                if board.cell[i][j] == 0:
                    check = False
                    for k1 in range(-1,2):
                        for k2 in range(-1,2):
                            if k1 == 0 and k2 == 0: continue
                            ni = i + k1
                            nj = j + k2
                            if ni < 0 or ni >= board.size or nj < 0 or nj >= board.size:continue
                            if board.cell[ni][nj]:
                                check = True
                    if check:
                        possibleMove.append((i, j))
        
        return possibleMove

    # Tìm xem liệu có nước chiến thắng luôn không
    def searchWinningMove(self, board: Board) -> list:
        possibleMove = self.getPossibleMove(board)

        for move in possibleMove:
            board.cell[move[0]][move[1]] = self.turn

            if self.getScore(board, self.turn, self.turn) >= self.winScore:
                board.cell[move[0]][move[1]] = 0
                return [0, move[0], move[1]]

            board.cell[move[0]][move[1]] = 0

        return None
    
    def minimax(self, depth_, board: Board, isMax, alpha: float, beta: float) -> list:
        if depth_ == 0:
            return [self.calculate(board, 1 if isMax else 2), None, None]

        possibleMove = self.getPossibleMove(board)

        if len(possibleMove) == 0:
            return [self.calculate(board, 1 if isMax else 2), None, None]

        if isMax:
            bestMove = [float(-self.winScore), None, None]

            for move in possibleMove:
                board.cell[move[0]][move[1]] = self.turn

                tmp = self.minimax(depth_ - 1, board, False, alpha, beta)
                
                if float(tmp[0]) > bestMove[0]:
                    bestMove[0] = float(tmp[0])
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
                alpha = max(alpha, bestMove[0])

                board.cell[move[0]][move[1]] = 0
                if alpha >= beta:
                    break
            return bestMove
        else:
            bestMove = [float(self.winScore), None, None]

            for move in possibleMove:
                board.cell[move[0]][move[1]] = 3 - self.turn

                tmp = self.minimax(depth_ - 1, board, True, alpha, beta)
                
                if float(tmp[0]) < bestMove[0]:
                    bestMove[0] = float(tmp[0])
                    bestMove[1] = move[0]
                    bestMove[2] = move[1]
                beta = min(beta, bestMove[0])

                board.cell[move[0]][move[1]] = 0
                if alpha >= beta:
                    break
            return bestMove

    def calculate(self, board: Board, turn) -> float:
        Xscore = self.getScore(board, self.turn, turn)
        OScore = self.getScore(board, 3 - self.turn, turn)

        if OScore == 0:
            OScore = 1

        return float(Xscore) / float(OScore)
    
    def getScore(self, board: Board, XO, turn_) -> int:
        cell = list(board.cell)

        return self.calHorizontal(cell, XO, turn_) + self.calVertical(cell, XO, turn_) + self.calDiagonal(cell, XO, turn_)
    
    def calHorizontal(self, cell, XO, turn_) -> int:
        consecutive = 0
        blocks = 2
        score = 0

        for i in range(len(cell)):
            for j in range(len(cell[0])):
                if cell[i][j] == XO:
                    consecutive += 1
                elif cell[i][j] == 0:
                    if consecutive > 0:
                        blocks -= 1
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 1
                else:
                    if consecutive > 0:
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 2

            if consecutive > 0:
                score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
            
            consecutive = 0
            blocks = 2

        return score
    
    def calVertical(self, cell, XO, turn_) -> int:
        consecutive = 0
        blocks = 2
        score = 0

        for j in range(len(cell[0])):
            for i in range(len(cell)):
                if cell[i][j] == XO:
                    consecutive += 1
                elif cell[i][j] == 0:
                    if consecutive > 0:
                        blocks -= 1
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 1
                else:
                    if consecutive > 0:
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 2

            if consecutive > 0:
                score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
            
            consecutive = 0
            blocks = 2

        return score
    
    def calDiagonal(self, cell, XO, turn_) -> int:
        consecutive = 0
        blocks = 2
        score = 0

        [dx,dy] = [1, 1]
        calCell = []
        for i in range(len(cell)):
            calCell.append([i, 0])
        for j in range(len(cell[0])):
            calCell.append([0, j])

        for [di, dj] in calCell:
            [i, j] = [di, dj]
            while(True):
                if i >= len(cell) or j >= len(cell):break

                if cell[i][j] == XO:
                    consecutive += 1
                elif cell[i][j] == 0:
                    if consecutive > 0:
                        blocks -= 1
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 1
                else:
                    if consecutive > 0:
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 2
                
                i += dx
                j += dy

            if consecutive > 0:
                score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
            
            consecutive = 0
            blocks = 2

        [dx,dy] = [-1, 1]
        calCell = []
        for i in range(len(cell)):
            calCell.append([i, 0])
        for j in range(len(cell[0])):
            calCell.append([len(cell) - 1, j])

        for [di, dj] in calCell:
            [i, j] = [di, dj]
            while(True):
                if i >= len(cell) or j >= len(cell):break

                if cell[i][j] == XO:
                    consecutive += 1
                elif cell[i][j] == 0:
                    if consecutive > 0:
                        blocks -= 1
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 1
                else:
                    if consecutive > 0:
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 2
                
                i += dx
                j += dy

            if consecutive > 0:
                score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
            
            consecutive = 0
            blocks = 2
            
        return score

    def getConsecutiveScore(self, consecutive, blocks, isTurn) -> int:
        if blocks == 2 and consecutive < 5:
            return 0
        
        if consecutive >= 5:
            return self.winScore * 2
        
        if consecutive == 4:
            if isTurn:
                return 1000000
            else:
                if blocks == 0:
                    return 250000
                return 200
        
        if consecutive == 3:
            if blocks == 0:
                if isTurn:
                    return 50000
                return 200
            else:
                if isTurn:
                    return 10
                return 5
        
        if consecutive == 2:
            if blocks == 0:
                if isTurn:
                    return 7
                return 5
            else:
                return 3

        if consecutive == 1:
            return 1 