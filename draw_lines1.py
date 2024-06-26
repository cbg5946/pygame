from math import sin, cos, radians
import pygame
from pygame.locals import QUIT

pygame.init()
SURFACE = pygame.display.set_mode((400, 300))
FPSCLOCK = pygame.time.Clock()

def main():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
        SURFACE.fill((0, 0, 0))
        
        pointlist0, pointlist1 = [], []
        for theta in range(0, 720, 144):
            rad = radians(theta)
            pointlist0.append((cos(rad)*100 + 100, sin(rad)*100 + 150))
            pointlist1.append((cos(rad)*100 + 300, sin(rad)*100 + 150))
            
        pygame.draw.lines(SURFACE, 'red', True, pointlist0, 5)
        pygame.draw.aalines(SURFACE, (255, 255, 255), True, pointlist1, 0)
        
        pygame.display.update()
        FPSCLOCK.tick(1)

main()