import pygame
from menus import Menu

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
shipX = 200
shipY = 480

#Text Block
font = pygame.font.Font('freesansbold.ttf', 14)
textX = 500
textY = 10

#Print each line of text to the screen
def show_text_block(x, y, lineList):
    for idx, line in enumerate(lineList):
        textLine = font.render(line, True, (255, 255, 255))
        screen.blit(textLine, (x, (y+(idx*16))))

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

    #Render the ship
    ship()
    #Show the Main Menu
    show_text_block(textX,textY, Menu.MAIN)

    #Draw frame
    pygame.display.update()
