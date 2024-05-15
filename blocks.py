import math, random, pygame
from pygame import QUIT, KEYDOWN, K_LEFT, K_RIGHT, Rect

pygame.init()
pygame.key.set_repeat(5, 10)
SURFACE = pygame.display.set_mode((600, 800))
FPSCLOCK = pygame.time.Clock()
BLOCKS = []

class Block:
    # 블록, 공, 패들 객체
    def __init__(self, color, rect, speed=0):
        self.col = color
        self.rect = rect
        self.speed = speed
        self.dir = random.randint(-45, 45) + 270 # 시작할 때 공의 방향이 아래쪽
        
    def move(self):
        # 공 움직임
        self.rect.centerx += math.cos(math.radians(self.dir))*self.speed
        self.rect.centery -= math.sin(math.radians(self.dir))*self.speed
    
    def draw(self):
        # 블록, 공, 패드 그리기
        if self.speed == 0:
            pygame.draw.rect(SURFACE, self.col, self.rect)
        else:
            pygame.draw.ellipse(SURFACE, self.col, self.rect)
            
PADDLE = Block((242, 242, 0), pygame.Rect(300, 700, 100, 30))
BALL = Block((242, 242, 0), pygame.Rect(300, 400, 20, 20), 10)

def tick():
    # 프레임별 처리   
    global BLOCKS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN: # 방향키 입력
            if event.key == pygame.K_LEFT:
                PADDLE.rect.centerx -= 10
            elif event.key == pygame.K_RIGHT:
                PADDLE.rect.centerx += 10
        elif event.type == pygame.MOUSEMOTION: # 마우스 위치 입력
            mouse_x, mouse_y = pygame.mouse.get_pos() 
            PADDLE.rect.centerx = mouse_x
    if BALL.rect.centery < 1000:
        BALL.move()
    
    # 블록 충돌?
    prevlen = len(BLOCKS)
    BLOCKS = [x for x in BLOCKS if not x.rect.colliderect(BALL.rect)]
    if len(BLOCKS) != prevlen:
        BALL.dir *= -1
    
    # 패들과 충돌?
    if PADDLE.rect.colliderect(BALL.rect):
        BALL.dir = 90 + ((PADDLE.rect.centerx - BALL.rect.centerx)/PADDLE.rect.width)*80
        
    # 벽과 충돌?
    if BALL.rect.centerx < 0 or BALL.rect.centerx > 600:
        BALL.dir = 180 - BALL.dir
    if BALL.rect.centery < 0:
        BALL.dir = -1*BALL.dir
        BALL.speed = 15

def main():
    myfont = pygame.font.SysFont(None, 80)
    mess_clear = myfont.render("Cleared!", True, (255, 255, 0))
    mess_over = myfont.render("Game Over!", True, (255, 255, 0))
    fps = 45
    colors = [(255, 0, 0), (255, 165, 0), (242, 242, 0), (0, 128, 0), (128, 0, 128), (0, 0, 250)]
    
    for ypos, color in enumerate(colors, start = 0):
        for xpos in range(0, 5):
            BLOCKS.append(Block(color, pygame.Rect(xpos*100 + 60, ypos*50 + 40, 80, 30)))
    
    while True:
        tick()
        
        SURFACE.fill((0, 0, 0))
        BALL.draw()
        PADDLE.draw()
        for block in BLOCKS:
            block.draw()
        
        if len(BLOCKS) == 0:
            SURFACE.blit(mess_clear, (200, 400))
        if BALL.rect.centery > 800 and len(BLOCKS) > 0:
            SURFACE.blit(mess_over, (150, 400))
        
        pygame.display.update()
        FPSCLOCK.tick(fps)

main()
    