from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE

pygame.init() # pygame 초기화
pygame.key.set_repeat(5, 5) # key 반복

SURFACE = pygame.display.set_mode((800, 600)) # 창 크기 설정
FPSCLOCK = pygame.time.Clock() # FPS 설정

def main():
    walls = 80 # 동굴 구성하는 직사각형 수
    ship_y = 250 # 케릭터 y좌표
    velocity = 0 # 케릭터 속도
    score = 0 # 점수
    slope = randint(1, 6) # 동굴 기울기
    sysfont = pygame.font.SysFont(None, 36)
    ship_image = pygame.image.load(r"games\cave\ship.png")
    bang_image = pygame.image.load(r"games\cave\bang.png")
    holes = []
    for xpos in range(walls):
        holes.append(Rect(xpos*10, 100, 10, 400)) #(x좌표, y좌표, 폭, 높이)
    game_over = False
    
    while True:
        is_space_down = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    is_space_down = True
        
        # 내 케릭터 이동
        if not game_over:
            score += 10
            velocity += -3 if is_space_down else 3 # space 누르면 위로 3 아니면 아래로 3
            ship_y += velocity # 케릭터 위치 조절
            
            #동굴 스크롤
            edge = holes[-1].copy()
            test = edge.move(0, slope) # 비변환 함수(edge는 그대로)
            if test.top <= 0 or test.bottom >= 600:
                slope = randint(1, 6)*(-1 if slope > 0 else 1)
                edge.inflate_ip(0, -20) # 직사각형 높이 축소(동굴 좁아지게)
            edge.move_ip(10, slope) # 변환 함수(edge 변화)
            holes.append(edge) # 맨 끝에 추가
            del holes[0] # 처음 직사각형 삭제
            holes = [x.move(-10, 0) for x in holes] #전체를 왼쪽으로 10만큼 이동
            
            # 충돌(벽에 부딛힌다면)
            if holes[0].top > ship_y or holes[0].bottom < ship_y + 80:
                game_over = True
             
        # 그리기
        SURFACE.fill((0, 255, 0))
        for hole in holes:
            pygame.draw.rect(SURFACE, (0, 0, 0), hole)
        SURFACE.blit(ship_image, (0, ship_y)) # 케릭터 나타내기
        score_image = sysfont.render("score is {}".format(score), True, (0, 0, 225))
        SURFACE.blit(score_image, (600, 20)) # 스코어 나타내기
        
        if game_over:
            SURFACE.blit(bang_image, (0, ship_y-40)) # 죽으면 bang이미지 나타내기
        pygame.display.update()
        FPSCLOCK.tick(15)
main()