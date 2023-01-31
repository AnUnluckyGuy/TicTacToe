from AI import AI
from Board import Board
import sys
import pygame
import time

pygame.init()
game_font = pygame.font.Font(pygame.font.get_default_font(), 50)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTBLUE = (0, 128, 255)
GREEN = (0, 255, 0)
RED = (255, 0 , 0)
YELLOW = (255, 255, 0)
status = ["", "X turn", "O turn", "Winner Found", "Draw"]
adjust_to_write_status = 50
turn = 1
start = False
just_play = []
cell_size = 60
size = 10
board_length = size * cell_size + adjust_to_write_status
board_width = size * cell_size
screen = pygame.display.set_mode((board_width, board_length))

def display(board: Board) -> None:
    screen.fill(WHITE)
    if turn == 1 or turn == 2:
        screen.blit(game_font.render(status[turn], True, BLACK, WHITE), (230, 0))
    elif turn == 3:
        screen.blit(game_font.render(status[turn], True, BLACK, WHITE), (125, 0))
    else :
        screen.blit(game_font.render(status[turn], True, BLACK, WHITE), (250, 0))
    for i in range(size):
        for j in range(size):
            bcolor = LIGHTBLUE
            if len(just_play) and i == just_play[0] and j == just_play[1]:
                bcolor = YELLOW
            cell_posX = j * cell_size
            cell_posY = i * cell_size + adjust_to_write_status
            pygame.draw.rect(surface=screen, rect = pygame.Rect(cell_posX, cell_posY, cell_size, cell_size), color=bcolor)
            pygame.draw.rect(surface=screen, rect = pygame.Rect(cell_posX + 2, cell_posY + 2, cell_size - 4, cell_size - 4), color=WHITE)
            if board.cell[i][j] == 1:
                screen.blit(game_font.render("X", True, RED, WHITE), (cell_posX + 13, cell_posY + 8))
            elif board.cell[i][j] == 2:
                screen.blit(game_font.render("O", True, GREEN, WHITE), (cell_posX + 10, cell_posY + 8))
    pygame.display.flip()

if __name__ == "__main__":
    ai = [0, AI(3, 1), AI(3, 2)]
    board = Board()
    playerTurn = 2

    while(True):
        mouseX = -1
        mouseY = -1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseY, mouseX = pygame.mouse.get_pos()
                break
        
        if board.checkWin(): 
            turn = 3
        
        if board.checkDraw():
            turn  = 4
        
        if turn >= 3:
            display(board)
            continue

        if turn == playerTurn:
            if mouseX != -1:
                px = (mouseX - adjust_to_write_status) // cell_size
                py = mouseY // cell_size
                if board.cell[px][py] == 0:
                    board.cell[px][py] = turn
                    just_play = [px, py]
                    turn = 3 - turn
                    start = True
        else:
            if not start:
                n_move = ai[turn].getFirstMove()
                start = True
            else:
                n_move = ai[turn].getNextMove(board)
            board.cell[n_move[0]][n_move[1]] = turn
            just_play = [n_move[0], n_move[1]]
            turn = 3 - turn

        '''
        if turn < 3:
            if not start:
                n_move = ai[turn].getFirstMove()
                start = True
            else:
                n_move = ai[turn].getNextMove(board)
            board.cell[n_move[0]][n_move[1]] = turn
            just_play = [n_move[0], n_move[1]]
            turn = 3 - turn
        '''

        display(board)
        #time.sleep(5)