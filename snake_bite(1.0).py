import random, pygame

pygame.init()
SURFACE = pygame.display.set_mode((600, 600))
FPSCLOCK = pygame.time.Clock()

FOODS = []
SNAKE = []

(W, H) = (40, 40)

def add_food(): # 임의의 장소에 먹이 배치
    while True:
        pos = (random.randint(0, (W-3)//3), random.randint(0, (H-3)//3))
        if pos in FOODS or pos in SNAKE: # 이미 먹이가 있거나 스네이크가 있는 곳이면
            continue # 다시 탐색
        FOODS.append(pos)
        print("먹이", pos)
        break

def move_food(pos): # 먹이를 다른 장소로 이동
    i = FOODS.index(pos) # 뱀이 먹이를 먹는 위치의 index(순서)를 i 변수에 할당
    del FOODS[i] # 삭제
    add_food() # 새로운 위치에 먹이 생성

def paint(message): # 화면 그리기
    SURFACE.fill((0, 0, 0))
    for idx in range(40):
        pygame.draw.line(SURFACE, (32, 32, 32), (idx*15, 0), (idx*15, 600)) # 가로줄
        pygame.draw.line(SURFACE, (32, 32, 32), (0, idx*15), (600, idx*15)) # 세로줄
    
    for food in FOODS: # 먹이 생성
        pygame.draw.ellipse(SURFACE, (0, 255, 0), pygame.Rect(food[0]*45, food[1]*45, 45, 45))
    
    for body in SNAKE: # 뱀 몸통 생성
        pygame.draw.rect(SURFACE, (0, 255, 255), pygame.Rect(body[0]*15, body[1]*15, 45, 45))
    
    
    if message != None:
        SURFACE.blit(message, (150, 300))
    pygame.display.update()

def main():
    myfont = pygame.font.SysFont(None, 80)
    key = pygame.K_DOWN
    message = None
    game_over = False
    SNAKE.append((int(W//2), int(H//2))) # 시작은 중앙에서
    for _ in range(10):
        add_food()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                key = event.key
        
        if not game_over:
            if key == pygame.K_LEFT:
                head = (SNAKE[0][0] - 1, SNAKE[0][1])
            elif key == pygame.K_RIGHT:
                head = (SNAKE[0][0] + 1, SNAKE[0][1])
            elif key == pygame.K_UP:
                head = (SNAKE[0][0], SNAKE[0][1] - 1)
            elif key == pygame.K_DOWN:
                head = (SNAKE[0][0], SNAKE[0][1] + 1)
            print(head)
            
            if head in SNAKE or head[0] < 0 or head[0] >= W or head[1] < 0 or head[1] >= H: # 머리가 몸통에 부딫히거나 벽에 닿으면
                message = myfont.render("GAME OVER!", True, (255, 255, 0)) # 게임오버
                game_over = True
            
            SNAKE.insert(0, head)
            x = head[0]//3
            y = head[1]//3
            if (x, y) in FOODS:
                move_food((x, y))
            else:
                SNAKE.pop()
        
        paint(message)
        FPSCLOCK.tick(25)
main()