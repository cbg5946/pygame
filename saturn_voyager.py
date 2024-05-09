from random import randint
import pygame

pygame.init()
SURFACE = pygame.display.set_mode((800, 800))
FPSCLOCK = pygame.time.Clock()

def main():
    game_over = False # 게임오버
    score = 0 # 점수
    speed = 25 # 속도
    stars = [] # 운석 저장
    keymap = [] # 키가 입력되어 있는지 나타내는 리스트
    ship = [0, 0] # 케릭터
    scope_image = pygame.image.load(r'games\saturn_voyager\scope.png')
    rock_image = pygame.image.load(r'games\saturn_voyager\rock.png')
    scorefont = pygame.font.SysFont(None, 36) # 점수 글꼴
    sysfont = pygame.font.SysFont(None, 72) # 게임오버 글꼴
    message_over = sysfont.render("GAMEOVER!!", True, (0, 255, 225)) # 게임오버 메세지 생성
    message_rect = message_over.get_rect() # 게임오버 좌표 받아옴
    message_rect.center = (400, 400) # 게임오버 센터 좌표 입력
    
    while len(stars) < 200: # 운석 200개 생성
        stars.append({"pos" : [randint(-1600, 1600), # pos : 운석좌표(x, y, z)
                               randint(-1600, 1600),
                               randint(0, 4095)],
                      "theta" : randint(0, 360)}) # 회전각(0 ~ 360도)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if not event.key in keymap:
                    keymap.append(event.key)
            elif event.type == pygame.KEYUP:
                keymap.remove(event.key)
        
        # 프레임별 처리
        if not game_over:
            score += 1
            if score % 10 == 0: # 점수가 10의 배수일 때마다
                speed += 1 # 속도 1씩 추가
            
            if pygame.K_LEFT in keymap:
                ship[0] -= 30
            elif pygame.K_RIGHT in keymap:
                ship[0] += 30
            elif pygame.K_UP in keymap:
                ship[1] -= 30
            elif pygame.K_DOWN in keymap:
                ship[1] += 30
            
            ship[0] = max(-800, min(800, ship[0])) # x좌표 -800 ~ 800 고정
            ship[1] = max(-800, min(800, ship[1])) # y좌표 -800 ~ 800 고정
            
            for star in stars:
                star["pos"][2] -= speed # 운석 z좌표를 speed만큼 줄임
                if star["pos"][2] < 64: # 운석 z좌표가 64보다 작다 -> xy평면(케릭터xy좌표 위치)에 도달
                    if abs(star["pos"][0] - ship[0]) < 50 and abs(star["pos"][1] - ship[1]) < 50:
                        game_over = True # (운석 x, y 좌표 - 케릭터 x, y 좌표) 모두 50미만(충돌) -> 게임오버
                    star["pos"] = [randint(-1600, 1600), randint(-1600, 1600), 4095] # 충돌 하지 않을 시 다시 z좌표 4095에 운석 배치
        
        # 그리기
        SURFACE.fill((0, 0, 0))
        stars = sorted(stars, key=lambda x : x["pos"][2], reverse=True) # 먼 운석을 먼저 그릴 수 있도록 정렬
        
        for star in stars:
            zpos = star["pos"][2]
            xpos = ((star["pos"][0] - ship[0] << 9) / zpos + 400) # +400은 화면 중앙에 배치하기 위함
            ypos = ((star["pos"][1] - ship[1] << 9) / zpos + 400)
            size = (50 << 9) / zpos
            rotated = pygame.transform.rotozoom(rock_image, star["theta"], size/145)
            SURFACE.blit(rotated, (xpos, ypos))
        
        SURFACE.blit(scope_image, (0, 0))
        
        if game_over:
            SURFACE.blit(message_over, message_rect)
            pygame.mixer.music.stop()
            
        score_str = str(score).zfill(6)
        score_image = scorefont.render(score_str, True, (0, 255, 0))
        SURFACE.blit(score_image, (700, 50))
        
        pygame.display.update()
        FPSCLOCK.tick(20)

main()