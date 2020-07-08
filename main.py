import pygame
import random
from menus import Menu
from Ships import Ship

#CONSTANTS
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

#GLOBAL SESSION VARIABLES
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

#Wait
wait = False

#FUNCTION DEFINITIONS
def render_menu_block(x, y, current_menu):
    """Render the current_menu"""
    lineList = []
    if current_menu == "main":
        lineList = Menu.MAIN
    elif current_menu == "combat":
        global menu
        lineList = Menu.COMBAT
        menu = "main"
    elif current_menu == "ships":
        #Make a copy by value not by reference
        shipList = Menu.SHIPS[:]
        #Generate list of ship names
        #TODO:add a owned ships variable to Ship class and then add each ships name to the Ship list when it is created
        for i, ship in enumerate(ownedShips):
            shipList.append(str(i) + " => " + ship.name)
        lineList = shipList
    for idx, line in enumerate(lineList):
        textLine = font.render(line, True, WHITE)
        pygame.draw.line(screen,WHITE, (x,0), (x,S_HEIGHT))
        screen.blit(textLine, (x+FONT_SIZE, (y+(idx*FONT_SIZE))))

def render_combat_log(x, y, lineList):
    #TODO: limit to 12 lines including first
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

#GAME LOOPS
def naval_combat_round(first, second):
    """Helper that gets called inside naval_combat_loop each round and runs through 3 turns"""
    global shipSelected
    global shipImg
    turnNum = 1
    await_input = False
    while turnNum <= 3:
        if not await_input:
            combatLog.append("What would " + first.name + " like to do?")
            await_input = True
        else:
            for combatEvent in pygame.event.get():
                # Window is closed using the X in the top right
                if combatEvent.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Key is pressed
                elif combatEvent.type == pygame.KEYUP:
                    turnNum += 1
                    await_input = False
                    if combatEvent.key == pygame.K_UP:
                        combatLog.append("Full speed ahead!")
                        first.speedUp()
                        first.move()
                    elif combatEvent.key == pygame.K_DOWN:
                        combatLog.append("Half sail!")
                        first.slowDown()
                        first.move()
                    elif combatEvent.key == pygame.K_h:
                        combatLog.append("Hold position!")
                    elif combatEvent.key == pygame.K_p:
                        combatLog.append("Turn to port!")
                        first.turn("port")
                        shipImg = pygame.transform.rotate(shipImg, 90)
                    elif combatEvent.key == pygame.K_s:
                        combatLog.append("Turn to starboard!")
                        first.turn("star")
                        shipImg = pygame.transform.rotate(shipImg, -90)
                    elif combatEvent.key == pygame.K_j:
                        combatLog.append("Prepare to jibe!")
                        first.turn("jibe")
                        shipImg = pygame.transform.rotate(shipImg, 180)
                    elif combatEvent.key == pygame.K_f:
                        combatLog.append("Cannons ready!\n")
                        distance = 0
                        if first.facing == 0 or first.facing == 2:
                            distance = abs(first.location[1] - second.location[1])
                        else:
                            distance = abs(first.location[0] - second.location[0])
                        damage = -1
                        while damage == -1:
                            #side = input("Which side cannons do you want to fire?")
                            damage = first.fire(distance, "star", second)
                            combatLog.append(first.name + " dealt " + str(damage) + " damage to " + second.name + "!")
                        second.hullHealth -= damage
                    #Invalid entry
                    else:
                        await_input = True
                        turnNum -= 1

        # Set screen background to black
        screen.fill((0, 0, 0))
        # Render the ship
        render_ship()
        # Show the current menu
        render_menu_block(textX, textY, "combat")
        # Show the combat log
        render_combat_log(0, 10, combatLog)
        # Draw frame
        pygame.display.update()
    return

def naval_combat_loop(ship1, ship2):
    """The game loop where naval combat is conducted between the two ships"""
    global combatLog
    global shipSelected
    inCombat = True
    winning_ship = None
    roundNum = 1
    while inCombat:
        combatLog.append("ROUND " + str(roundNum) + "!")
        # Determine round initiative
        firstToGo = 1#random.randrange(1, 3)
        if firstToGo == 1:
            first = ship1
            second = ship2
        else:
            first = ship2
            second = ship1
        combatLog.append(first.name + " will go first this turn.")
        #Start round
        naval_combat_round(first, second)
        roundNum += 1

        #Set screen background to black
        screen.fill((0, 0, 0))
        #Render the ship
        render_ship()
        #Show the current menu
        render_menu_block(textX, textY, "combat")
        #Show the combat log
        render_combat_log(0, 10, combatLog)
        #Draw frame
        pygame.display.update()
    return winning_ship

#Main Game Loop
running = True
while running:
    for event in pygame.event.get():
        #Window is closed using the X in the top right
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
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
                    pygame.quit()
                    quit()
                elif event.key == pygame.K_s and len(ownedShips) > 0:
                    #Switch to the ships menu
                    menu = "ships"
                elif event.key == pygame.K_c and shipSelected:
                    menu = "combat"
                    naval_combat_loop(shipSelected, enemyShipSelected)
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
    render_menu_block(textX, textY, menu)
    #Draw frame
    pygame.display.update()
