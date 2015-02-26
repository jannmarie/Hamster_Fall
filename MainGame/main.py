import pygame, random, sys
from pygame.locals import *

WINDOWWIDTH = 800
WINDOWHEIGHT = 600
TEXTCOLOR = (255, 255, 255)
BACKGROUNDCOLOR = (0, 175, 175)
FPS = 40
badcloud_minsize = 10
badcloud_maxsize = 40
badcloud_minspeed = 1
badcloud_maxspeed = 8
addnew_badcloud = 6
hamsterspeed = 5

def terminate():
    pygame.quit()
    sys.exit()

def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE: # pressing escape quits
                    terminate()
                return

def hamsterHasHitBadclouds(hamsterRect, cloud_group):
    for b in cloud_group:
        if hamsterRect.colliderect(b['rect']):
            return True
    return False

def drawText(text, font, surface, x, y):
    textobj = font.render(text, 1, TEXTCOLOR)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    

# set up pygame, the window, and the mouse cursor
pygame.init()
mainClock = pygame.time.Clock()
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Hamsterfall')
pygame.mouse.set_visible(False)

# set up fonts
font = pygame.font.SysFont(None, 48)

# set up sounds
gameOverSound = pygame.mixer.Sound('gameover.wav')
pygame.mixer.music.load('background.mid')

# set up images
hamsterImage = pygame.image.load('hamy.png')
hamsterRect = hamsterImage.get_rect()
badcloudsImage = pygame.image.load('cloud.png')

# show the "Start" screen
drawText('Hamsterfall', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
drawText('Press a key to start.', font, windowSurface, (WINDOWWIDTH / 3) - 30, (WINDOWHEIGHT / 3) + 50)
pygame.display.update()
waitForPlayerToPressKey()


topScore = 0
while True:
    # set up the start of the game
    cloud_group = []
    score = 0
    hamsterRect.topleft = (WINDOWWIDTH / 2, 100)
    moveLeft = moveRight = moveUp = moveDown = False
    reverseCheat = slowCheat = False
    badcloudsAddCounter = 0
    pygame.mixer.music.play(-1, 0.0)

    while True: # the game loop runs while the game part is playing
        score += 1 # increase score

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == ord('z'):
                    reverseCheat = True
                if event.key == ord('x'):
                    slowCheat = True
                if event.key == K_LEFT or event.key == ord('a'):
                    moveRight = False
                    moveLeft = True
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveLeft = False
                    moveRight = True
                if event.key == K_UP or event.key == ord('w'):
                    moveDown = False
                    moveUp = True
                if event.key == K_DOWN or event.key == ord('s'):
                    moveUp = False
                    moveDown = True

            if event.type == KEYUP:
                if event.key == ord('z'):
                    reverseCheat = False
                    score = 0
                if event.key == ord('x'):
                    slowCheat = False
                    score = 0
                if event.key == K_ESCAPE:
                        terminate()

                if event.key == K_LEFT or event.key == ord('a'):
                    moveLeft = False
                if event.key == K_RIGHT or event.key == ord('d'):
                    moveRight = False
                if event.key == K_UP or event.key == ord('w'):
                    moveUp = False
                if event.key == K_DOWN or event.key == ord('s'):
                    moveDown = False

           # if event.type == MOUSEMOTION:
                # If the mouse moves, move the player where the cursor is.
              #  hamsterRect.move_ip(event.pos[0] - hamsterRect.centerx, event.pos[1] - hamsterRect.centery)

        # Add new badclouds at the top of the screen, if needed.
        if not reverseCheat and not slowCheat:
            badcloudsAddCounter += 1
            
        if badcloudsAddCounter == addnew_badcloud:
            badcloudsAddCounter = 0
            badclouds_size = random.randint(badcloud_minsize, badcloud_maxsize)
            new_badclouds = {'rect': pygame.Rect(random.randint(0, WINDOWWIDTH-badclouds_size), WINDOWHEIGHT, badclouds_size, badclouds_size), #left,top,width,height
                        'speed': random.randint(badcloud_minspeed, badcloud_maxspeed),
                        'surface':pygame.transform.scale(badcloudsImage, (badclouds_size, badclouds_size)),
                        }

            cloud_group.append(new_badclouds)

        # Move the hamster around.
        if moveLeft and hamsterRect.left > 0:
            hamsterRect.move_ip(-1 * hamsterspeed, 0)
        if moveRight and hamsterRect.right < WINDOWWIDTH:
            hamsterRect.move_ip(hamsterspeed, 0)
        if moveUp and hamsterRect.top > 0:
            hamsterRect.move_ip(0, -1 * hamsterspeed)
        if moveDown and hamsterRect.bottom < WINDOWHEIGHT:
            hamsterRect.move_ip(0, hamsterspeed)

        # Move the mouse cursor to match the player.
   #     pygame.mouse.set_pos(playerRect.centerx, playerRect.centery)

        # Move the badclouds up.
        for b in cloud_group:
            if not reverseCheat and not slowCheat:
                b['rect'].move_ip(0, -5)
            elif reverseCheat:
                b['rect'].move_ip(0, b['speed'])
            elif slowCheat:
                b['rect'].move_ip(0, 1)

         # Delete badclouds that have fallen past the bottom.
        for b in cloud_group[:]:
            if b['rect'].top > WINDOWHEIGHT:
                cloud_group.remove(b)

        # Draw the game world on the window.
        windowSurface.fill(BACKGROUNDCOLOR)

        # Draw the score and top score.
        drawText('Score: %s' % (score), font, windowSurface, 10, 0)
        drawText('Top Score: %s' % (topScore), font, windowSurface, 10, 40)

        # Draw the hamster rectangle
        windowSurface.blit(hamsterImage, hamsterRect)

        # Draw each bad cloud
        for b in cloud_group:
            windowSurface.blit(b['surface'], b['rect'])

        pygame.display.update()

        # Check if any of the bad clouds have hit the hamster.
        if hamsterHasHitBadclouds(hamsterRect, cloud_group):
            if score > topScore:
                topScore = score # set new top score
            break

        mainClock.tick(FPS)

    # Stop the game and show the "Game Over" screen.
    pygame.mixer.music.stop()
    gameOverSound.play()

    drawText('GAME OVER', font, windowSurface, (WINDOWWIDTH / 3), (WINDOWHEIGHT / 3))
    drawText('Press a key to play again.', font, windowSurface, (WINDOWWIDTH / 3) - 80, (WINDOWHEIGHT / 3) + 50)
    pygame.display.update()
    waitForPlayerToPressKey()

    gameOverSound.stop()
