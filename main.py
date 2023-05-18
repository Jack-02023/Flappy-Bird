import pygame, sys, time
from setting import *
from sprite import BG, Ground, Plane, Obstacle
from pygame import mixer
class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption('Flappy Bird Clone')
        background = pygame.mixer.Sound('cat_background.mp3')
        background.set_volume(0.75)
        background.play(loops = -1)
        self.displaySurface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.active = False
        self.startTime = 0
        self.acc = 0
        self.lastAcc = 0
        self.dieSound = pygame.mixer.Sound('sfx_die.mp3')
        self.RUN = pygame.mixer.Sound('RUN.mp3')
        self.begin = False

        pygame.mouse.set_visible(0)

        self.allSprite = pygame.sprite.Group()
        self.collisionSprite = pygame.sprite.Group()

        bgHeight = pygame.image.load('images/background.png').get_height()
        self.scaleFactor = WINDOW_HEIGHT / bgHeight

        BG(self.allSprite, self.scaleFactor, self.acc)
        Ground([self.allSprite, self.collisionSprite], self.scaleFactor, self.acc)
        self.plane = Plane(self.allSprite, self.scaleFactor * 1.3, self.begin)

        #Timer
        self.obstacleTimer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacleTimer, 1400)

        self.font = pygame.font.Font('BD_Cartoon_Shout.ttf', 30)
        self.score = 0

        #menu
        self.menuSurf = pygame.image.load('images/menu.png').convert_alpha()
        self.menuRect = self.menuSurf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

    #collision
    def collision(self):
        if pygame.sprite.spritecollide(self.plane, self.collisionSprite, False, pygame.sprite.collide_mask) or self.plane.rect.top <= -100:
            for sprite in self.collisionSprite.sprites():
                if sprite.spriteType == 'obstacle':
                    self.dieSound.play()
                    sprite.kill() 
            self.active = False
            self.plane.kill()

    def won(self):
        for sprite in self.collisionSprite.sprites():
            if sprite.spriteType == 'obstacle':
                sprite.kill() 
            self.plane.kill()
        winSurf = self.font.render("Happy Mother's day", True, (64, 64, 64))
        winRect = winSurf.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 1.3))
        self.displaySurface.blit(winSurf, winRect)

    def updateScore(self):
        if self.active:
            self.score = pygame.time.get_ticks() - self.startTime
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menuRect.height / 1.3)
        scoreSurf = self.font.render(f'{self.score // 1000}', True, (64, 64, 64))
        scoreRect = scoreSurf.get_rect(center = (WINDOW_WIDTH / 2, y))
        self.displaySurface.blit(scoreSurf, scoreRect)
        if self.score // 1000 != self.lastAcc and self.acc < 20:
            self.lastAcc = self.score // 1000
            self.acc += 1 
        if self.score // 1000 >= 50:
            self.active = False
            self.won()

    def run(self):
        lastTime = time.time()
        while True:
            dt = time.time() - lastTime
            lastTime = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE: 
                    if self.active and self.begin:
                        self.plane.jump()
                    else:
                        if not self.begin: 
                            self.plane.kill()
                            self.begin = True
                        self.active = True
                        self.plane = Plane(self.allSprite, self.scaleFactor * 1.3, self.begin)
                        self.startTime = pygame.time.get_ticks()
                        self.acc = 0
                        self.RUN.play()
                if event.type == self.obstacleTimer and self.active:
                    Obstacle([self.allSprite, self.collisionSprite], self.scaleFactor * 1.2, self.acc)
            self.displaySurface.fill('black')
            self.allSprite.update(dt)
            self.allSprite.draw(self.displaySurface)
            self.updateScore()

            if self.active:
                self.collision()
            else:
                self.displaySurface.blit(self.menuSurf, self.menuRect)
            pygame.display.update()
            self.clock.tick(FRAMERATE)

if __name__ == '__main__':
    game = Game()
    game.run()