from random import randint
from math import hypot
import pygame

class House:
    # 집 객체
    def __init__(self, xpos):
        self.rect = pygame.Rect(xpos, 550, 40, 40)
        self.exploded = False
        strip = pygame.image.load(r"games\missile_command\strip.png")
        self.images = (pygame.Surface((20, 20), pygame.SRCALPHA), pygame.Surface((20, 20), pygame.SRCALPHA))
        self.images[0].blit(strip, (0, 0), pygame.Rect(0, 0, 20, 20))
        self.images[1].blit(strip, (0, 0), pygame.Rect(20, 0, 20, 20))

    def draw(self):
        if self.exploded:
            SURFACE.blit(self.images[1], self.rect.topleft)
        else:
            SURFACE.blit(self.images[0], self.rect.topleft)

class Missile:
    def __init__(self):
        self.max_count = 500
        self.interval = 1000
        self.pos = [0, 0]
        self.cpos = [0, 0]
        self.firetime = 0
        self.radius = 0
        self.reload(0)
    
    def reload(self, time_count):
        # 미사일 재초기화(낙하 후, 폭발 후)
        house_x = randint(0, 12) * 60 + 20
        self.pos = (randint(0, 800), house_x)
        self.interval = int(self.interval*0.9)
        self.firetime = randint(0, self.interval) + time_count
        self.cpos = [0, 0]
        self.radius = 0
    
    def tick(self, time_count, shoot, houses):
        # 미사일 상태 갱신
        is_hit = False
        elapsed = time_count - self.firetime
        if elapsed < 0:
            return
        
        if self.radius > 0: # 폭발 중
            self.radius += 1
            if self.radius > 100:
                self.reload(time_count)
        else:
            self.cpos[0] = (self.pos[1] - self.pos[0])*elapsed / self.max_count + self.pos[0]
            self.cpos[1] = 575 * elapsed / self.max_count
            
            # 떨어졌나?
            
            diff = hypot(shoot.shot_pos[0] - self.cpos[0], shoot.shot_pos[1] - self.cpos[1])
            if diff < shoot.radius:
                is_hit = True
                self.radius = 1 # 폭발 시작
                
            # 지면에 충돌
            if elapsed > self.max_count:
                self.radius = 1 # 폭발 시작
                for house in houses:
                    if hypot(self.cpos[0] - house.rect.center[0], self.cpos[1] - house.rect.center[1]) < 30:
                        house.exploded = True
            
        return is_hit
    
    def draw(self):
        # 미사일 그리기
        pygame.draw.line(SURFACE, (0, 255, 255), (self.pos[0], 0), self.cpos)
        if self.radius > 0:
            rad = self.radius if self.radius < 50 else 100 - self.radius
            pos = (int(self.cpos[0]), int(self.cpos[1]))
            pygame.draw.circle(SURFACE, (0, 255, 255), pos, rad)

class Shoot:
    # 스스로 폭발하는 빔 객체
    def __init__(self):
        self.scope = (400, 300)
        self.image = pygame.image.load(r"games\missile_command\scope.png")
        self.count = 0
        self.fire = False
        self.radius = 0
        self.shot_pos = [0, 0]
        
    def tick(self):
        # 폭발 중 빔의 위치, 상태를 갱신
        if self.fire:
            self.count += 1
            if 100 <= self.count < 200:
                self.radius += 1
            elif 200 <= self.count < 300:
                self.radius -= 1
            elif self.count >= 300:
                self.fire = False
                self.count = 0
    
    def draw(self):
        # 빔 그리기
        rect = self.image.get_rect()
        rect.center = self.scope
        SURFACE.blit(self.image, rect)
        if not self.fire:
            return
        if self.radius == 0 and self.count < 100:
            ratio = self.count / 100
            ypos = 600 - (600 - self.shot_pos[1])*ratio
            x_left = int((self.shot_pos[0]) * ratio)
            x_right = int((800 - (800 - self.shot_pos[0])*ratio))
            

SURFACE = pygame.display.set_mode((400, 300))
FPSCLOCK = pygame.time.Clock()
def main():
    
    house = House(500)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            
    
    while True:
        SURFACE.fill((0, 0, 0))
        pygame.display.update()
        FPSCLOCK.tick(20)

main()