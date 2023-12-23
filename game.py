""" ---  --- """
# XXX: Maybe there's another way to do this?
import os
# For setting the window position.
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
""" ---  --- """

""" ---  --- """
# XXX: Pre-emptive initialization so it's ready for lib.text. Maybe do it early in there instead?
import pygame
pygame.init()
""" ---  --- """

import pygame
import time

import lib.cursor
import lib.dialog
import lib.grid
import lib.input
import lib.sys
import lib.text

pygame.init()

screen = pygame.display.set_mode((1024, 768))
input = lib.input.Input()

lib.grid.init(screen)

d = lib.dialog.Dialog((0, 0, 20, 5)).setText('Hello, good madam.')
enemyList = lib.dialog.Dialog(lib.dialog.posEnemyList())
playerList = lib.dialog.Dialog(lib.dialog.posPlayerList()).setText(
    ' Jimmy\n Frank\n Alice \n Kate'
)
selector = lib.cursor.CursorSelector(4)

# False, None - when transitioning to none, True
enablegrid = False
running = True
while running:
    ### --- Event Handling ------------------------------------------------- ###

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    for what in input.tick():
        selector.giveInput(what)

    ### --- Rendering ------------------------------------------------------ ###

    screen.fill((0x00, 0x00, 0x00))

    # XXX: Test items
    d.render(screen)
    enemyList.render(screen)
    playerList.render(screen)
    selector.render(screen, lib.dialog.posPlayerList()[0:2])

    if enablegrid:
        lib.grid.draw(screen)

    pygame.display.flip()

    ### --- Enforce Frame Limit -------------------------------------------- ###

    time.sleep(1 / lib.sys.FRAME_RATE)

pygame.quit()
