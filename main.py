import pygame
import random
from menus import Menu
from Ships import Ship

#CONSTS
WHITE = (255, 255, 255)
S_WIDTH = 800
S_HEIGHT = 600
FONT_SIZE = 14

#Init pygame
pygame.init()

#Create the screen
screen = pygame.display.set_mode((S_WIDTH, S_HEIGHT))

#Title and Icon
pygame.display.set_caption("Ingot Sea")
icon = pygame.image.load('Images/IngotSeaLogoNoSkull.png')
pygame.display.set_icon(icon)

#Ship
shipSelected = None
enemyShipSelected = Ship("Enemy Ship", 5) #TODO: Remove hard coding
ownedShips = []
shipImg = pygame.image.load('Images/Ship.png')
shipX = int(S_WIDTH/3)
shipY = 480

#Combat
combatLog = ["Combat Log:"]

#Text Block
menu = "main"
font = pygame.font.Font('freesansbold.ttf', FONT_SIZE)
textX = int(2*S_WIDTH/3)
textY = 10

#Print each line of text to the screen
def render_menu_block(x, y, lineList):
    for idx, line in enumerate(lineList):
        textLine = font.render(line, True, WHITE)
        pygame.draw.line(screen,WHITE, (x,0), (x,S_HEIGHT))
        screen.blit(textLine, (x+FONT_SIZE, (y+(idx*FONT_SIZE))))

def render_combat_log(x, y, lineList):
    for idx, line in enumerate(lineList):
        textLine = font.render(line, True, WHITE)
        pygame.draw.line(screen, WHITE, (x, int(S_HEIGHT / 3)), (int(2 * S_WIDTH / 3), int(S_HEIGHT / 3)))
        screen.blit(textLine, (x+FONT_SIZE, (y + (idx * FONT_SIZE))))

def render_ship():
    screen.blit(shipImg, (shipX-int(shipImg.get_size()[0]/2), shipY))
    shipNameText = font.render(shipSelected.name, True, WHITE)
    fw, fh = font.size(shipSelected.name)
    #Center the name on the middle of the first third of the screen above the ship
    screen.blit(shipNameText, (int(S_WIDTH/3)-int(fw/2), shipY - FONT_SIZE))

def navalCombatLoop(Ship1, Ship2):
    inCombat = True
    roundNum = 1
    while inCombat:
        combatLog.append("ROUND " + str(roundNum) + "!")
        # Determine round initiative
        firstToGo = random.randrange(1,3)
        if firstToGo == 1:
            firstShip = Ship1
            secondShip = Ship2
        else:
            firstShip = Ship2
            secondShip = Ship1
        combatLog.append(firstShip.name + " will go first this turn.")
        turnNum = 1
        while turnNum <= 3:
            print(str(combatLog))
            render_combat_log(0, 10, combatLog)
            # First Ship
            combatLog.append("What would " + firstShip.name + " like to do?")
            for event in pygame.event.get():
                # Window is closed using the X in the top right
                if event.type == pygame.QUIT:
                    pygame.quit()
                # Key is pressed
                elif event.type == pygame.KEYUP:
                    turnNum += 1
                    if event.key == pygame.K_UP:
                        combatLog.append("Full speed ahead!")
                        firstShip.speedUp()
                        firstShip.move()
                    elif event.key == pygame.K_DOWN:
                        combatLog.append("Half sail!")
                        firstShip.slowDown()
                        firstShip.move()
                    elif event.key == pygame.K_h:
                        combatLog.append("Hold position!")
                    elif event.key == pygame.K_p:
                        combatLog.append("Turn to port!")
                        firstShip.turn("port")
                    elif event.key == pygame.K_s:
                        combatLog.append("Turn to starboard!")
                        firstShip.turn("star")
                    elif event.key == pygame.K_j:
                        combatLog.append("Prepare to jibe!")
                        firstShip.turn("jibe")
                    elif event.key == pygame.K_f:
                        combatLog.append("Cannons ready!\n")
                        distance = 0
                        if firstShip.facing == 0 or firstShip.facing == 2:
                            distance = abs(firstShip.location[1] - secondShip.location[1])
                        else:
                            distance = abs(firstShip.location[0] - secondShip.location[0])
                        damage = -1
                        while damage == -1:
                            #side = input("Which side cannons do you want to fire?")
                            damage = firstShip.fire(distance, "star", secondShip)
                            combatLog.append(firstShip.name + " dealt " + str(damage) + " damage to " + secondShip.name + "!")
                        secondShip.hullHealth -= damage
            # Second Ship
            combatLog.append("What would " + secondShip.name + " like to do?")
            # Check if one of the ships has sunk
            if not firstShip.isAfloat():
                combatLog.append(firstShip.name + " has disappeared beneath the waves.")
                inCombat = False
            elif not secondShip.isAfloat():
                combatLog.append(secondShip.name + " has disappeared beneath the waves.\n")
                inCombat = False
                # Set screen background to black
                screen.fill((0, 0, 0))

                # Render the ship
                if shipSelected:
                    render_ship()
                # Render the combat menu
                navalCombatLoop(shipSelected, enemyShipSelected)
                # Draw frame
                pygame.display.update()
        roundNum += 1

#Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        #Window is closed using the X in the top right
        if event.type == pygame.QUIT:
            running = False
        #Key is pressed
        elif event.type == pygame.KEYUP:
            #Main Menu options
            if menu == "main":
                if event.key == pygame.K_n:
                        name = "Morta Verde"
                        crew = 5
                        s1 = Ship(name, crew)
                        ownedShips.append(s1)
                        shipSelected = s1
                elif event.key == pygame.K_e:
                    running = False
                elif event.key == pygame.K_s and len(ownedShips) > 0:
                    #Switch to the ships menu
                    menu = "ships"
                elif event.key == pygame.K_c and shipSelected:
                    menu = "combat"
            if menu == "ships":
                #Convert ascii int to actual number (d48 is 0, d49 is 1, etc.)
                shipNumber = int(event.key) - 48
                if 0 <= shipNumber < len(ownedShips):
                    shipSelected = ownedShips[shipNumber]
                    menu = "main"

    #Set screen background to black
    screen.fill((0, 0, 0))

    #Render the ship
    if shipSelected:
        render_ship()
    #Show the current menu
    if menu == "main":
        render_menu_block(textX, textY, Menu.MAIN)
    elif menu == "combat":
        navalCombatLoop(shipSelected, enemyShipSelected)
        menu == "main"
    elif menu == "ships":
        #Make a copy by value not by reference
        shipList = Menu.SHIPS[:]
        #Generate list of ship names
        for i, ship in enumerate(ownedShips):
            shipList.append(str(i) + " => " + ship.name)
        render_menu_block(textX, textY, shipList)

    #Draw frame
    pygame.display.update()
