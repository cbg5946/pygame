from math import sin, cos, radians
from random import randint
import pygame

pygame.init()
pygame.key.set_repeat(5, 5)
SURFACE = pygame.display.set_mode((800, 800))
FPSCLOCK = pygame.time.Clock()

class Drawable:
    # 전체의 그리기 객체의 부모 클래스
    def __init__(self, rect):
        self.rect = rect
        self.step = [0, 0]
        
    def move(self):
        rect = self.rect.center
        xpos = (rect[0] + self.step[0]) % 800 # 화면 끝에 도달하면 반대편 화면으로 나옴
        ypos = (rect[1] + self.step[1]) % 800
        self.rect.center = (xpos, ypos)

class Rock(Drawable):
    # 운석 객체
    def __init__(self, pos, size):
        super().__init__(pygame.Rect(0, 0, size, size))
        self.rect.center = pos
        self.image = pygame.image.load(r"games\asteroid\rock.png")
        self.theta = randint(0, 360) # 운석이 이동하는 방향
        self.size = size
        self.power = 128/size # 운석의 이동 속도, 크기가 작을 수록 빠르게 이동
        self.step[0] = cos(radians(self.theta)) * self.power
        self.step[1] = sin(radians(self.theta)) * -self.power # 굳이 -를 붙일 필요는 없다
    
    def draw(self):
        # 운석 그리기
        rotated = pygame.transform.rotozoom(self.image, self.theta, self.size/64) # 운석이 갈라질 때 더 작은 운석이 생성될 수 있도록 배율 설정
        rect = rotated.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(rotated, rect)
        
    def tick(self):
        # 운석 이동
        self.theta += 3
        self.move()
        
class Shot(Drawable):
    # 총알 객체
    def __init__(self):
        super().__init__(pygame.Rect(0, 0, 6, 6))
        self.count = 0 # 총알 진행했는지 나타내는 카운터
        self.power = 10 # 총알 속도
        self.max_count = 40 #총알 도달 거리
    
    def draw(self):
        # 총알 그리기
        if self.count < self.max_count:
            pygame.draw.rect(SURFACE, (225, 225, 0), self.rect)
    
    def tick(self):
        # 총알 이동
        self.count += 1
        self.move()

class Ship(Drawable):
    # 캐릭터 객체
    def __init__(self):
        super().__init__(pygame.Rect(355, 370, 90, 60))
        self.theta = 0 # 캐릭터 방향
        self.power = 0 # 캐릭터 속도
        self.accel = 0 # 캐릭터 가속도
        self.explode = False # 캐릭터가 죽었는가?
        self.image = pygame.image.load(r"games\asteroid\ship.png")
        self.bang = pygame.image.load(r"games\asteroid\bang.png")
        
    def draw(self):
        # 캐릭터 그리기
        rotated = pygame.transform.rotate(self.image, self.theta)
        rect = rotated.get_rect()
        rect.center = self.rect.center
        SURFACE.blit(rotated, rect)
        if self.explode:
            SURFACE.blit(self.bang, rect)
    
    def tick(self):
        # 내 캐릭터 움직임
        self.power += self.accel
        self.power *= 0.94
        self.accel *= 0.94
        self.step[0] = cos(radians(self.theta)) * self.power
        self.step[1] = sin(radians(self.theta)) * -self.power
        self.move()
        

def key_event_handler(keymap, ship):
    # 키 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if not event.key in keymap:
                keymap.append(event.key)
        elif event.type == pygame.KEYUP:
            keymap.remove(event.key)
    
    if pygame.K_LEFT in keymap: # 왼쪽, 오른쪽은 방향
        ship.theta += 5 
    elif pygame.K_RIGHT in keymap:
        ship.theta -= 5
    elif pygame.K_UP in keymap: # 위, 아래는 속도
        ship.accel = min(5, ship.accel + 0.2)
    elif pygame.K_DOWN in keymap:
        ship.accel = max(-5, ship.accel - 0.2)

def main():
    # 메인 루틴
    sysfont = pygame.font.SysFont(None, 72)
    scorefont = pygame.font.SysFont(None, 36)
    message_clear = sysfont.render("!!CLEARED!!", True, (0, 255, 225))
    message_over = sysfont.render("GAME OVER!!", True, (0, 255, 225))
    message_rect = message_clear.get_rect()
    message_rect.center = (400, 400)
    
    keymap = []
    shots = []
    rocks = []
    ship = Ship()
    game_over = False
    score = 0
    back_x, back_y = 0, 0
    back_image = pygame.image.load(r"games\asteroid\bg.png")
    back_image = pygame.transform.scale2x(back_image)
    
    while len(shots) < 15:
        shots.append(Shot())
    
    while len(rocks) < 4:
        pos = randint(0, 800), randint(0, 800)
        rock = Rock(pos, 64)
        if not rock.rect.colliderect(ship.rect):
            rocks.append(rock)
    
    while True:
        key_event_handler(keymap, ship)
        
        if not game_over:
            ship.tick()
            
            # 운석 이동
            for rock in rocks:
                rock.tick()
                if rock.rect.colliderect(ship.rect): # 운석과 캐릭터가 충돌하면
                    ship.explode = True # 폭발 = True
                    game_over = True # 게임오버 = True
            
            # 총알을 이동
            fire = False
            for shot in shots:
                if shot.count < shot.max_count:
                    shot.tick()

                    # 총알, 운석 충돌 처리
                    hit = None # 처음은 총알에 맞은 운석이 없음
                    for rock in rocks:
                        if rock.rect.colliderect(shot.rect): # 운석과 총알이 닿으면
                            hit = rock # hit에 운석을 저장
                    if hit != None: # 맞은 운석이 있다면
                        score += hit.rect.width * 10 # 점수 추가
                        shot.count = shot.max_count # 총알 거리를 최대로 변환(운석과 닿으면 총알을 삭제하기 위함)
                        rocks.remove(hit) # 닿은 운석을 운석 리스트에서 삭제
                        if hit.rect.width > 16: # 운석 크기가 16보다 크면 
                            rocks.append(Rock(hit.rect.center, hit.rect.width/2)) #더 작은 운석 2개로 분할
                            rocks.append(Rock(hit.rect.center, hit.rect.width/2))
                        if len(rocks) == 0: # 남아있는 운석이 없으면
                            game_over = True # 게임오버
                
                elif not fire and pygame.K_SPACE in keymap: # 총알이 발사되지 않았고 스페이스 키를 눌렀다면
                    shot.count = 0
                    shot.rect.center = ship.rect.center
                    shot_x = shot.power * cos(radians(ship.theta))
                    shot_y = shot.power * -sin(radians(ship.theta))
                    shot.step = (shot_x, shot_y)
                    fire = True # 총알 발사
        
        # 배경 그리기
        back_x = (back_x + ship.step[0]/2) % 1600 # 배경 스크롤 무한(나누기 2는 원거리 배경 느리게 움직이는 효과)
        back_y = (back_y + ship.step[1]/2) % 1600 # background scrolling 기법
        SURFACE.fill((0, 0, 0))
        SURFACE.blit(back_image, (-back_x, -back_y), (0, 0, 3200, 3200))
        print(back_x + ship.step[0] / 2, back_y + ship.step[1] / 2)
        # 각종 객체 그리기
        ship.draw()
        for shot in shots:
            shot.draw()
        for rock in rocks:
            rock.draw()
        
        # 점수 나타내기
        score_str = str(score).zfill(6) # score 포함 숫자6개
        score_image = scorefont.render(score_str, True, (0, 255, 0))
        SURFACE.blit(score_image, (700, 10))
        
        # 메시지 나타내기
        if game_over: # 게임오버가 되었는데
            if len(rocks) == 0: # 남아있는 운석이 없다면
                SURFACE.blit(message_clear, message_rect.topleft) # 클리어 메세지
            else: # 운석이 남았다면
                SURFACE.blit(message_over, message_rect.topleft) # 게임오버 메세지
        
        pygame.display.update()
        FPSCLOCK.tick(20)

main()