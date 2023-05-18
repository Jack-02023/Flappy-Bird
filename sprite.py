import pygame
from random import randint
from random import choice
from setting import *

class BG(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor, acc):
        super().__init__(groups)
        self.acc = acc
        bgImage = pygame.image.load('images/background.png').convert_alpha()

        fullHeight = bgImage.get_height() * scaleFactor
        fullWidth = bgImage.get_width() * scaleFactor

        fullSizeImage = pygame.transform.scale(bgImage, (fullWidth, fullHeight))
        self.image = pygame.Surface((fullWidth * 2, fullHeight))
        self.image.blit(fullSizeImage, (0, 0))
        self.image.blit(fullSizeImage, (fullWidth, 0))
        self.rect = self.image.get_rect(topleft = (0, 0))
        self.pos = pygame.math.Vector2(self.rect.topleft)


    def update(self, dt):
        self.pos.x -= (300 + self.acc) * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
class Ground(pygame.sprite.Sprite):
    def __init__(self, groups, scaleFactor, acc) -> None:
        super().__init__(groups)
        ground = pygame.image.load('images/ground.png').convert_alpha()
        self.image = pygame.transform.scale(ground, pygame.math.Vector2(ground.get_size()) * scaleFactor)

        self.rect = self.image.get_rect(bottomleft = (0, WINDOW_HEIGHT))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)
        self.spriteType = 'ground'
        self.acc = acc

    def update(self, dt):
        self.pos.x -= (360 + self.acc) * dt
        if self.rect.centerx <= 0:
            self.pos.x = 0
        self.rect.x = round(self.pos.x)
class Plane(pygame.sprite.Sprite):
    def __init__(self, group, scaleFactor, begin) -> None:
        super().__init__(group)
        self.importFrames(scaleFactor)
        self.frameIndex = 0
        self.image = self.frames[self.frameIndex]

        self.rect = self.image.get_rect(midleft = (WINDOW_WIDTH / 20, WINDOW_HEIGHT / 2))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.begin = begin
        self.spriteType = 'plane'
        self.gravity = 600
        self.direction = 0
        self.mask = pygame.mask.from_surface(self.image)

        self.jumpSound = pygame.mixer.Sound('jump.wav')
        self.jumpSound.set_volume(0.3)


    def importFrames(self, scaleFactor):
        self.frames = []

        for i in range(3):
            surf = pygame.image.load(f'images/red{i}.png').convert_alpha()
            scaledSurf = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scaleFactor / 2.5)
            self.frames.append(scaledSurf)
            
    def applyGravity(self, dt):
        if self.begin:
            self.direction += self.gravity * dt
            self.pos.y += self.direction * dt
            self.rect.y = round(self.pos.y)
    
    def jump(self):
        self.direction = -400
        self.jumpSound.play()

    def animate(self, dt):
        self.frameIndex += 15 * dt
        if self.frameIndex >= len(self.frames):
            self.frameIndex = 0
        self.image = self.frames[int(self.frameIndex)]

    def rotate(self):
        rotatedPlane = pygame.transform.rotozoom(self.image, -self.direction * 0.06, 1)
        self.image = rotatedPlane
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.applyGravity(dt)
        self.animate(dt)
        self.rotate()
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, group, scaleFactor, acc) -> None:
        super().__init__(group)
        self.acc = acc
        orientation = choice(('up', 'down'))
        surf = pygame.image.load(f'images/{choice((0, 1))}.png').convert_alpha()
        self.image = pygame.transform.scale(surf, pygame.math.Vector2(surf.get_size()) * scaleFactor)
        x = WINDOW_WIDTH + randint(40, 100)
        if orientation == 'up':
            y = WINDOW_HEIGHT + randint(10, 50)
            self.rect = self.image.get_rect(midbottom = (x, y))
        else:
            y = randint(-50, -10)
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect = self.image.get_rect(midtop = (x, y))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.mask = pygame.mask.from_surface(self.image)
        self.spriteType = 'obstacle'

    def update(self, dt):
        self.pos.x -= (360 + self.acc) * dt
        self.rect.x = round(self.pos.x)
        if self.rect.right <= -100:
            self.kill()
