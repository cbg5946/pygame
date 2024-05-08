from math import floor
from random import randint
import pygame
from pygame import QUIT, MOUSEBUTTONDOWN

WIDTH = 20
HEIGHT = 15
SIZE = 50
NUM_OF_BOMBS = 20
EMPTY = 0
BOMB = 1
OPENED = 2
OPEN_COUNT = 0
CHECKED = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

pygame.init()
SURFACE = pygame.display.set_mode([WIDTH*SIZE, HEIGHT*SIZE])
FPSCLOCK = pygame.time.Clock()

def num_of_bomb(field, x_pos, y_pos):
    count = 0 # 0개
    for yoffset in range(-1, 2):
        for xoffset in range(-1, 2):
            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == BOMB: # 범위 내에서 (-1, 0, 1)칸에 폭탄이 있으면
                count += 1
    return count

def open_tile(field, x_pos, y_pos):
    # 타일 오픈
    global OPEN_COUNT
    if CHECKED[y_pos][x_pos]: # 이미 타일을 확인 했다면
        return # 함수 종료
    
    CHECKED[y_pos][x_pos] = True # 타일 확인(True)
    
    for yoffset in range(-1, 2):
        for xoffset in range(-1, 2):
            xpos, ypos = (x_pos + xoffset, y_pos + yoffset)
            if 0 <= xpos < WIDTH and 0 <= ypos < HEIGHT and field[ypos][xpos] == EMPTY:
                field[ypos][xpos] = OPENED
                OPEN_COUNT += 1
                count = num_of_bomb(field, xpos, ypos)
                if count == 0 and not (xpos == x_pos and ypos == y_pos):
                    open_tile(field, xpos, ypos)

def main():
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_clear = largefont.render("!!CLEARED!!", True, (0, 255, 225))
    message_over = largefont.render("GAME OVER!!", True, (0, 255, 225))
    message_rect = message_clear.get_rect()
    message_rect.center = (WIDTH*SIZE/2, HEIGHT*SIZE/2)
    game_over = False
    
    field = [[EMPTY for xpos in range(WIDTH)] for ypos in range(HEIGHT)]
    count = 0 # 폭탄 0개
    while count < NUM_OF_BOMBS: 
        xpos, ypos = randint(0, WIDTH-1), randint(0, HEIGHT-1) 
        if field[ypos][xpos] == EMPTY: # 만약 칸이 비어있다면
            field[ypos][xpos] = BOMB # 폭탄 랜덤 배치
            count += 1

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1: # 1 : 왼쪽, 2 : 오른쪽
                xpos, ypos = floor(event.pos[0] / SIZE), floor(event.pos[1]/SIZE) # 칸 어디를 찍던 xpos, ypos를 정수화(floor 사용)
                if field[ypos][xpos] == BOMB:
                    game_over = True
                else:
                    open_tile(field, xpos, ypos)
        
        # 그리기
        SURFACE.fill((0, 0, 0))
        for ypos in range(HEIGHT):
            for xpos in range(WIDTH):
                tile = field[ypos][xpos]
                rect = (xpos*SIZE, ypos*SIZE, SIZE, SIZE) # 정사각형 격자로 이루어진 타일 생성
                
                if tile == EMPTY or tile == BOMB:
                    pygame.draw.rect(SURFACE, (192, 192, 192), rect) # 빈 칸 또는 폭탄 칸은 회색
                    if game_over and tile == BOMB: # 게임오버 됐을 때(폭탄 클릭)
                        pygame.draw.ellipse(SURFACE, (225, 225, 0), rect) # 폭탄 칸 노란색 원
                elif tile == OPENED:
                    count = num_of_bomb(field, xpos, ypos)
                    if count > 0:
                        num_image = smallfont.render("{}".format(count), True, (255, 255, 0))
                        SURFACE.blit(num_image, (xpos*SIZE+10, ypos*SIZE+10))
        
        # 선 그리기
        for idx in range(0, WIDTH*SIZE, SIZE):
            pygame.draw.line(SURFACE, (96, 96, 96), (idx, 0), (idx, HEIGHT*SIZE))
            for idx in range(0, HEIGHT*SIZE, SIZE):
                pygame.draw.line(SURFACE, (96, 96, 96), (0, idx), (WIDTH*SIZE, idx))
        
        # 메시지 나타내기
        if OPEN_COUNT == WIDTH*HEIGHT - NUM_OF_BOMBS:
            SURFACE.blit(message_clear, message_rect.topleft)
        elif game_over:
            SURFACE.blit(message_over, message_rect.topleft)
            
        
        pygame.display.update()
        FPSCLOCK.tick(15)

main()