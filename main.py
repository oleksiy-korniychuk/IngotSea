import pygame

#Init pygame
pygame.init()

#Create the screen
screen = pygame.display.set_mode((800,600))

#Title and Icon
pygame.display.set_caption("Ingot Sea")
icon = pygame.image.load('Images/IngotSeaLogoNoSkull.png')
pygame.display.set_icon(icon)

#Ship
shipImg = pygame.image.load('Images/Ship.png')
shipX = 370
shipY = 480

#Text Block
font = pygame.font.Font('freesansbold.ttf', 16)
textX = 10
textY = 10

def show_text_block(x, y, text):
    textBlock = font.render(text, True, (255, 255, 255))
    screen.blit(textBlock, (x, y))

def ship():
    screen.blit(shipImg, (shipX, shipY))

#Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #Set screen background to black
    screen.fill((0, 0, 0))

    ship()
    show_text_block(textX,textY,"Test Text")

    #Draw frame
    pygame.display.update()
