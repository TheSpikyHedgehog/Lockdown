"""
@Author: TheSpikyHedgehog
2023

Gist:
You are trapped in a nuclear power plant
ESCAPE MODE:
    Try to escape before nuclear meltdown

DISABLE MODE:
    Try to disable the nuclear meltdown
"""
import pygame
import sys


# Init pygame
try:
    pygame.init()
except Exception as exc:
    print(f"Couldn't initialize pygame. Continuing without it. Err: {exc}")

WIDTH = 600
HEIGHT = 400
walls = []
keys = []
root = pygame.display.set_mode((600, 400), pygame.DOUBLEBUF | pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption("Lockdown. (by TheSpikyHedgehog)")
pygame.display.set_icon(pygame.image.load("assets/images/logo.png").convert())
sprites = []

offsetx = -12
offsety = 150

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        super().__init__()
        self.x = x
        self.y = y
        # Image and rect not included for now.
        self.images = [
            pygame.image.load("assets/images/player_down.png").convert_alpha(),
            pygame.image.load("assets/images/player_up.png").convert_alpha(),
            pygame.image.load("assets/images/player_right.png").convert_alpha(),
            pygame.image.load("assets/images/player_left.png").convert_alpha()
        ]
        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.vel = 0.5

    def draw(self):
        root.blit(self.image, self.rect)


    def handle_inputs(self):
        keys = pygame.key.get_pressed()
        global offsetx, offsety
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                offsetx -= self.vel
                self.image = self.images[3]
                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        if self.rect.left < wall.rect.right:
                            offsetx += self.vel + 2

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                offsetx += self.vel
                self.image = self.images[2]
                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        if self.rect.right > wall.rect.left:
                            offsetx -= self.vel

        if keys[pygame.K_UP] or keys[pygame.K_w]:
                offsety -= self.vel
                self.image = self.images[1]
                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        if self.rect.top < wall.rect.bottom:
                            offsety += self.vel + 2
        
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                offsety += self.vel
                self.image = self.images[0]
                for wall in walls:
                    if self.rect.colliderect(wall.rect):
                        if self.rect.bottom > wall.rect.top:
                            offsety -= self.vel + 2
        self.rect.x = WIDTH / 2
        self.rect.y = HEIGHT / 2

class Inventory(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.slots = {}
        self.key = pygame.image.load("assets/images/key_slot.png").convert_alpha()
        for index in range(4):
            self.slots[index] = None
        self.active_slot = 0 
    
    def draw(self):
        pygame.draw.rect(root, "gray", pygame.Rect(240,350,160,40))
        xoffset = 10
        yoffset = 10
        for i in range(len(self.slots)):
            if self.slots[i] == None:
                pass
            elif self.slots[i] == "Key":
                root.blit(self.key, (240 + (xoffset + 40*i), 350 + yoffset))
            else:
                pass
            
            if i == self.active_slot:
                pygame.draw.rect(root, "white", pygame.Rect(240 + (i*40), 350, 40, 40), 3)
            else:
                pygame.draw.rect(root, "#232b2b", pygame.Rect(240 + (i*40), 350, 40, 40), 3)

FLOOR = 0   
WALL = 1
EMPTY = 2
KEY = 3

textures = {
    FLOOR : pygame.image.load("assets/images/floor.png").convert(),
    WALL : pygame.image.load("assets/images/wall_forward.png").convert(),
    KEY : pygame.image.load("assets/images/key.png").convert_alpha(),
	EMPTY : None
}

lvl = [
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, FLOOR, FLOOR, WALL, WALL, WALL, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL, FLOOR, FLOOR, WALL, WALL, WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, FLOOR, FLOOR, WALL, WALL, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL, WALL],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, FLOOR, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, WALL, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY, EMPTY],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
    [],
]

class Wall(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = textures[WALL]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pos
    def draw(self):
        root.blit(self.image, self.rect)
        self.rect.x = self.pos[0] - offsetx
        self.rect.y = self.pos[1] - offsety

class Key(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.image.load("assets/images/key.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.pos = pos
        
    def draw(self):
        root.blit(self.image, self.rect)
        self.rect.x = self.pos[0] - offsetx
        self.rect.y = self.pos[1] - offsety

    def pick_up(self, inv, key_group):
        self.kill()
        key_group.remove(self)
        for slot in inv.slots:
            if inv.slots[slot] == None:
                inv.slots[slot] = "Key"
                return
            else:
                continue


def load_others():
    global walls, keys
    for row in range(len(lvl)):
        for column in range(len(lvl[row])):
            if list(textures.keys())[list(textures.values()).index(textures[lvl[row][column]])] == WALL:
                wall = Wall(pos=(column*30, row*30))
                walls.append(wall)
            if list(textures.keys())[list(textures.values()).index(textures[lvl[row][column]])] == KEY:
                key = Key(pos=(column*30, row*30))
                keys.append(key)
            else:
                continue

def load_levels(lvl):
    for row in range(len(lvl)):
        for column in range(len(lvl[row])):
            if list(textures.keys())[list(textures.values()).index(textures[lvl[row][column]])] == FLOOR:
                root.blit(textures[lvl[row][column]], (column*30 - offsetx, row*30 - offsety))
            elif list(textures.keys())[list(textures.values()).index(textures[lvl[row][column]])] == WALL:
                continue
            elif list(textures.keys())[list(textures.values()).index(textures[lvl[row][column]])] == EMPTY:
                pass
            elif list(textures.keys())[list(textures.values()).index(textures[lvl[row][column]])] == KEY:
                root.blit(textures[FLOOR], (column*30 - offsetx, row*30 - offsety))
            else:
               root.blit(textures[lvl[row][column]], (column*30 - offsetx, row*30 - offsety))
			   
def game():
    load_others()
    p = Player(300,300)
    inv = Inventory()
    while True:
        root.fill("BLACK")
        load_levels(lvl)
        for wall in walls:
            wall.draw()
        for key in keys:
            key.draw()
            
			# Use key.pick_up when player touch key
            if p.rect.colliderect(key.rect):
                key.pick_up(inv, keys)
        p.draw()
        p.handle_inputs()
        inv.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    inv.active_slot = 0
                elif event.key == pygame.K_2:
                    inv.active_slot = 1
                elif event.key == pygame.K_3:
                    inv.active_slot = 2
                elif event.key == pygame.K_4:
                    inv.active_slot = 3

                else:
                    pass
        pygame.display.update()


def main_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

# TODO:
# Create main menu screen
if __name__ == "__main__":
    game()
