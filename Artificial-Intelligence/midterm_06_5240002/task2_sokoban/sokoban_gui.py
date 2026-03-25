import pygame

TILE_SIZE = 60

_images_loaded = False
player_img = None
box_on_goal_img = None
wall_img = None
floor_img = None
box_img = None


def load_images():
    global _images_loaded, player_img, box_on_goal_img, wall_img, floor_img, box_img
    if _images_loaded:
        return
    player_img = pygame.transform.scale(pygame.image.load("images/player.png"), (TILE_SIZE, TILE_SIZE))
    box_on_goal_img = pygame.transform.scale(pygame.image.load("images/box_on_goal.png"), (TILE_SIZE, TILE_SIZE))
    wall_img = pygame.transform.scale(pygame.image.load("images/wall.png"), (TILE_SIZE, TILE_SIZE))
    floor_img = pygame.transform.scale(pygame.image.load("images/floor.png"), (TILE_SIZE, TILE_SIZE))
    box_img = pygame.transform.scale(pygame.image.load("images/box.png"), (TILE_SIZE, TILE_SIZE))
    _images_loaded = True


def draw_grid(screen, grid, player, boxes, goals):
    load_images()
    for y,row in enumerate(grid):
        for x,cell in enumerate(row):
            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE)
            if cell=='%':
                screen.blit(wall_img, rect)
            else:
                screen.blit(floor_img, rect)
            if (x,y) in goals and (x,y) not in boxes:
                pygame.draw.circle(screen, "#1AC491", rect.center, TILE_SIZE//6)
    for bx,by in boxes:
        rect = pygame.Rect(bx*TILE_SIZE, by*TILE_SIZE, TILE_SIZE, TILE_SIZE)
        if (bx,by) in goals:
            screen.blit(box_on_goal_img, rect)
        else:
            screen.blit(box_img, rect)
    px,py = player
    rect = pygame.Rect(px*TILE_SIZE, py*TILE_SIZE, TILE_SIZE, TILE_SIZE)
    screen.blit(player_img, rect)