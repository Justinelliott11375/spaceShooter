import pygame
import random
import os

WIDTH = 600
HEIGHT = 800
FPS = 60
playerSpeed = 15

# Colors

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# assets
gameFolder = os.path.dirname(__file__)
imageFolder = os.path.join(gameFolder, "images")
soundFolder = os.path.join(gameFolder, "sound")

# initialize stuff
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Blaster")
clock = pygame.time.Clock()
fontName = pygame.font.match_font('arial')

def drawText(surface, text, size, x, y):
    font = pygame.font.Font(fontName, size)
    textSurface = font.render(text, True, WHITE)
    textRect = textSurface.get_rect()
    textRect.midtop = (x,y)
    surface.blit(textSurface, textRect)

def drawLives(surface, x, y, image):
        imageRect = image.get_rect()
        imageRect.x = x
        imageRect.y = y
        surface.blit(image, imageRect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(playerImage, (60,70))
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH/2
        self.rect.bottom = HEIGHT * .95
        self.speedx = 0
        self.shootDelay = 150
        self.lastShot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hiddenTimer = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        keyState = pygame.key.get_pressed()
        if keyState[pygame.K_LEFT]:
            self.speedx = -playerSpeed
        if keyState[pygame.K_RIGHT]:
            self.speedx = playerSpeed
        if keyState[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        # unhide if hidden
        if self.hidden and pygame.time.get_ticks() - self.hiddenTimer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH/2
            self.rect.bottom = HEIGHT * .95

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.lastShot > self.shootDelay:
            self.lastShot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            allSprites.add(bullet)
            bullets.add(bullet)
            shootSound.play()
    def hide(self):
        # hides player between lives
        self.hidden = True
        self.hiddenTimer = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT * 300)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletImage
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -12
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = alienImage
        self.rect = self.image.get_rect()
        self.radius = 22
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = random.randrange(-100,-40)
        self.speedy = random.randrange(5,11)
        self.speedx = random.randrange(-2,2)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -70 or self.rect.right > WIDTH + 70:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.bottom = random.randrange(-100,-40)
            self.speedy = random.randrange(1,6)


def showGameOverScreen(playerScore):
    screen.blit(backGroundImage, backGroundImage_rect)
    drawText(screen, "Game Over", 64, WIDTH/2, HEIGHT/4)
    drawText(screen, "Your Score: " + str(playerScore), 48, WIDTH/2, HEIGHT/2.5)
    drawText(screen, "Press any key to play again!", 32, WIDTH/2, HEIGHT * .75)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                waiting = False
                gameOver = False

def showGameStartScreen():
    screen.blit(backGroundImage, backGroundImage_rect)
    drawText(screen, "SPACE SHOOTER", 64, WIDTH/2, HEIGHT/4)
    drawText(screen, "Left/Right arrow keys to move", 48, WIDTH/2, HEIGHT/2.5)
    drawText(screen, "Space to shoot(hold for full auto!)", 48, WIDTH/2, HEIGHT/2)
    drawText(screen, "Press any key to start", 32, WIDTH/2, HEIGHT * .75)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# load graphics

playerImage = pygame.image.load(os.path.join(imageFolder, "shooterShip1.png")).convert_alpha()
playerLivesImage = pygame.transform.scale(playerImage, (21,25)).convert_alpha()
backGroundImage = pygame.image.load(os.path.join(imageFolder, "shooterBackground6.png")).convert()
backGroundImage_rect = backGroundImage.get_rect()
bulletImage = pygame.image.load(os.path.join(imageFolder, "beams.png")).convert_alpha()
alienImage = pygame.image.load(os.path.join(imageFolder, "ufoImage1.png")).convert_alpha()

# load sound

shootSound = pygame.mixer.Sound(os.path.join(soundFolder, "laserShoot2.wav"))
explosionSound = pygame.mixer.Sound(os.path.join(soundFolder, "explosionSound1.wav"))

# Game loop
gameOver = False
running = True
gameStart = False
while running:
    if not gameStart:
        showGameStartScreen()
        gameStart = True

        allSprites = pygame.sprite.Group()
        mobGroup = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        allSprites.add(player)


        for i in range(12):
            newMob = Mob()
            allSprites.add(newMob)
            mobGroup.add(newMob)

        #initial score
        score = 0
        #inital lives
        lives = 3

    if gameOver:
        showGameOverScreen(score)
        gameOver = False

        allSprites = pygame.sprite.Group()
        mobGroup = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        allSprites.add(player)


        for i in range(12):
            newMob = Mob()
            allSprites.add(newMob)
            mobGroup.add(newMob)

        #initial score
        score = 0
        #inital lives
        lives = 3
    # maintain framerate
    clock.tick(FPS)
    # handle events
    for event in pygame.event.get():
        # checking for window close
        if event.type == pygame.QUIT:
            running = False

    # update
    allSprites.update()

    #check for player colliding with mobs
    playerCollisions = pygame.sprite.spritecollide(player, mobGroup, True, pygame.sprite.collide_circle)
    for hit in playerCollisions:
        explosionSound.play()
        player.hide()
        player.lives -= 1

    #lives mechanic
    if player.lives == 0:
        gameOver = True
    #check for bullets colliding with mobs
    bulletCollisions = pygame.sprite.groupcollide(mobGroup, bullets, True, True)
    for hit in bulletCollisions:
        score += 20
        mob = Mob()
        allSprites.add(mob)
        mobGroup.add(mob)
        explosionSound.play()
    # render/draw
    screen.fill(BLACK)
    screen.blit(backGroundImage, backGroundImage_rect)
    allSprites.draw(screen)
    # draw and keep track of score on screen
    drawText(screen, "Score: " + str(score), 40, WIDTH * .125, HEIGHT * .96)
    drawLives(screen, WIDTH - 100, HEIGHT * .96, playerLivesImage)
    drawText(screen, "x " + str(player.lives - 1), 35, WIDTH * .91, HEIGHT * .96)

    # remember to flip display AFTER drawing
    pygame.display.flip()

pygame.quit()
