from Board import Board
import random

class AI:
    # depth: độ sâu của thuật toán minimax
    # turn: lượt đánh của AI (1(X) hoặc 2(O))
    # winScore: ngưỡng chiến thắng
    def __init__(self, depth, turn) -> None:
        self.depth = depth
        self.turn = turn
        self.winScore = 100000000

    # Nếu AI đánh nước đánh đầu tiên thì ta random nước đánh đầu tiên
    def getFirstMove(self) -> list:
        return [int(random.random() * 5 + 3), int(random.random() * 5 + 3)]
    
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

            if self.getScore(board, self.turn, self.turn) >= self.winScore:# Phát hiện ra nước đánh chiến thắng luôn
                board.cell[move[0]][move[1]] = 0
                return [0, move[0], move[1]]

            board.cell[move[0]][move[1]] = 0

        return None
    
    # Thuật toán minimax kết hợp cắt tỉa alpha - beta
    def minimax(self, depth_, board: Board, isMax, alpha: float, beta: float) -> list:
        if depth_ == 0:
            return [self.calculate(board, 1 if isMax else 2), None, None]

        possibleMove = self.getPossibleMove(board)

        if len(possibleMove) == 0:# Không còn ô có thể đánh
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

    # Tính số điểm của trạng thái bảng xét tới
    # board: bảng cần tính điểm
    # turn: lượt tiếp theo là 1(X) hay 2(O)
    def calculate(self, board: Board, turn) -> float:
        myScore = self.getScore(board, self.turn, turn)# ĐIểm AI giành được
        oppoScore = self.getScore(board, 3 - self.turn, turn)# ĐIểm đối thủ giành được

        if oppoScore == 0:
            oppoScore = 1

        return float(myScore) / float(oppoScore)
    
    # Tính điểm tương ứng cho 1(X) hoặc 2(O) 
    # XO: xác định sẽ tính điểm cho 1(X) hay 2(O)
    # turn_: lượt tiếp theo là 1(X) hay 2(O) 
    def getScore(self, board: Board, XO, turn_) -> int:
        cell = list(board.cell)

        return self.calHorizontal(cell, XO, turn_) + self.calVertical(cell, XO, turn_) + self.calDiagonal(cell, XO, turn_)
    
    # Tính điểm trên hàng ngang
    # XO, turn_ tương ứng với getScore
    def calHorizontal(self, cell, XO, turn_) -> int:
        consecutive = 0 # Biến đếm số lượng ô liên tiếp cùng giá trị XO
        blocks = 2 # Kiểm soát 2 đầu (bắt đầu và kết thúc) của dãy liên tiếp có bị chặn hay còn trống
                   # Đặt = 2 do giả sử 2 đầu đều bị chặn (đầu bắt đầu chắc chắn bị chặn bởi không thể đánh ra ngoài biên)
        score = 0 # Tổng điểm đạt được
        # Với mỗi dãy liên tiếp độ dài nhất định kết hợp cùng kiểm tra block 2 đầu sẽ cho thấy được tiềm năng có nước chiến thẳng (Xem ở hàm getConsecutiveScore)

        for i in range(len(cell)):
            for j in range(len(cell[0])):
                if cell[i][j] == XO:
                    consecutive += 1 # Nếu ô (i,j) có giá trị XO đang xét độ dài dãy liên tiếp tăng 1
                elif cell[i][j] == 0: # Nếu ô (i,j) trống
                    if consecutive > 0: # Nếu tồn tại dãy liên tiếp ngay trước ô (i,j)
                        blocks -= 1 # vì ô (i,j) trống nên đầu kết thúc của dãy liên tiếp không bị chặn
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_) # Tính điểm
                        consecutive = 0 # ô (i,j) kết thúc dãy liên tiếp => dãy liên tiếp mới sẽ có độ dài = 0 (chưa có gì)
                    blocks = 1 # do ô (i,j) trống nên đầu bắt đầu của dãy liên tiếp tiếp theo không bị chặn
                               # đặt = 1 do giả sử đầu kết thúc của dãy liên tiếp tiếp theo bị chặn
                else: # Nếu ô (i,j) có giá trị khác XO đang xét
                    # Tương tự ở trên
                    if consecutive > 0: 
                        score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
                        consecutive = 0
                    blocks = 2

            if consecutive > 0:
                score += self.getConsecutiveScore(consecutive, blocks, XO == turn_)
            
            # Đặt lại giá trị để chuyển sang tính hàng tiếp theo
            consecutive = 0
            blocks = 2

        return score
    
    # Tương tự Horizontal nhưng là chiều dọc
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
    
    # Tương tự Horizontal nhưng là chiều chéo
    def calDiagonal(self, cell, XO, turn_) -> int:
        consecutive = 0
        blocks = 2
        score = 0

        # Chiều chéo từ trái trên xuống phải dưới
        [dx,dy] = [1, 1]
        calCell = []
        for i in range(len(cell)):
            calCell.append([i, 0])
        for j in range(1, len(cell[0])):
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

        # Chiều chéo từ trái dưới lên phải trên
        [dx,dy] = [-1, 1]
        calCell = []
        for i in range(len(cell)):
            calCell.append([i, 0])
        for j in range(1, len(cell[0])):
            calCell.append([len(cell) - 1, j])

        for [di, dj] in calCell:
            [i, j] = [di, dj]
            while(True):
                if i < 0 or j >= len(cell):break

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

    # Tính điểm cho mỗi trường hợp độ dài liên tiếp
    # isTurn: kiểm tra xem lượt tiếp theo có phải mình đánh hay không
    def getConsecutiveScore(self, consecutive, blocks, isTurn) -> int:
        if blocks == 2 and consecutive < 5: # Bị chặn 2 đầu và độ dài < 5 thì không có giá trị vì không thể chiến thắng
            return 0
        
        if consecutive >= 5: # Tạo được dãy có độ dài >=5 thì chắc chắn thắng
            return self.winScore * 2
        
        # Các dãy khi này có blocks < 2
        if consecutive == 4: # dãy có độ dài 4
            if isTurn: # Lượt tiếp theo mình đánh 
                return 1000000 # cơ hội thắng cao
            else: # Lượt tiếp theo của đối thủ
                if blocks == 0: # không bị block 2 đầu
                    return 250000 # cơ hội thắng cao nhưng đối thủ có thể có nước cờ chiến thắng trong lượt đi tiếp theo
                # bị block 1 đầu
                return 200 # cơ hội thắng thấp do đối thủ có thể chặn
        
        # Tương tự 
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