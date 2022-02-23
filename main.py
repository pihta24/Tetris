from copy import deepcopy

import pygame
from utils import generate_square, generate_board

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Тетрис')
    size = width, height = 501, 501
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    
    board, FULL_LINE = generate_board(10, 20)
    active = generate_square(board)
    moved = False
    running = True
    t = 0
    v = 200
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                    active.move(-1)
                elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                    active.move(1)
                    
        if t >= v:
            t %= v
            if not active.move(0, 1):
                if not moved:
                    running = False
                active.active = False
                moved = False
                active = generate_square(board)
            else:
                moved = True
                
        while FULL_LINE in board.generate_figures_map(active):
            y = board.generate_figures_map(active).index(FULL_LINE)
            coords = [[x, y] for x in range(board.width)]
            figures_to_del = []
            for i in board.figures:
                n_coords = deepcopy(i.coords)
                for j in i.coords:
                    if j in coords:
                        coords.remove(j)
                        n_coords.remove(j)
                i.coords = n_coords
                if not i.coords:
                    figures_to_del.append(i)
            for i in figures_to_del:
                board.figures.remove(i)
        for i in board.figures:
            if not i.active:
                while i.move(0, 1):
                    pass
                
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()
        
        t += clock.tick()
    pygame.quit()