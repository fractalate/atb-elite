""" ---  --- """
# XXX: Maybe there's another way to do this?
# XXX: I'd also like to put the window at the position it was in for the last
#      run, but it seems like this requires usage of some unrelated libraries
#      and might not be easy to make it cross platform. The basic idea I would
#      want to implement is to save the window position at shutdown, then
#      restore it at startup only if the window would be fully in the display.
#      Otherwise start at (0, 0).
import os
# For setting the window position when starting up. This needs to be done
# before pygame.display.set_mode().
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0, 0)
""" ---  --- """

""" ---  --- """
# XXX: Pre-emptive initialization so it's ready for lib.text. Maybe do it early
#      in there instead?
import pygame
pygame.init()
""" ---  --- """

import pygame

import lib.cursor
import lib.dialog
import lib.grid
import lib.input
import lib.sys
import lib.text

DELAY_TIME = round(1 / lib.sys.FRAME_RATE * 1000)

pygame.init()

screen = pygame.display.set_mode((lib.sys.DISPLAY_WIDTH, lib.sys.DISPLAY_HEIGHT))
lib.grid.init(screen)

input = lib.input.Input()
dialogs = lib.dialog.DialogStack()

def openDialog0():
    options = ['one', 'two', 'three', 'four']
    dialog0 = lib.dialog.DialogPromptSelection('Choose thing.\nThings:', options, (2, 2, 24, 5))

    def onClose():
        dialogs.remove(dialog0)

    def onConfirm():
        showMessage('You selected ' + options[dialog0.selector.position], onClose=onClose)

    dialog0.addInputHandler('Confirm', onConfirm)

    dialogs.push(dialog0)

def showMessage(text: str, onClose = None):
    d = lib.dialog.Dialog((5, 5, 20, 3))
    d.setText(text)
    def onConfirm():
        dialogs.remove(d)
        if onClose is not None:
            onClose()
    d.addInputHandler('Confirm', onConfirm)
    dialogs.push(d)

enemyList = lib.dialog.Dialog(lib.dialog.posEnemyList())
playerList = lib.dialog.Dialog(lib.dialog.posPlayerList()).setText(
    ' Jimmy\n Frank\n Alice \n Kate'
)

enablegrid = False # XXX: Here for debugging.
running = True
while running:
    ### --- Event Handling ------------------------------------------------- ###

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ### --- Player Input --------------------------------------------------- ###

    # Input gets tick() first to distribute input to components early. This
    # causes input to be distributed to all components before they have a chance
    # to do their tick().
    for what in input.tick():
        if dialogs.isCapturingInput():
            dialogs.giveInput(what)
        elif what == 'Confirm':
            openDialog0()
        elif what == 'Cancel':
            enablegrid = not enablegrid # XXX: Here for debugging.

    ### --- Tick ----------------------------------------------------------- ###

    dialogs.tick()

    ### --- Rendering ------------------------------------------------------ ###

    screen.fill((0x00, 0x00, 0x00))
    dialogs.render(screen)

    # TODO: Make these lists official somewhere.
    enemyList.render(screen)
    playerList.render(screen)

    if enablegrid:
        lib.grid.draw(screen) # XXX: Here for debugging.

    # This should be the last step of rendering.
    pygame.display.flip()

    ### --- Enforce Frame Limit -------------------------------------------- ###

    pygame.time.delay(DELAY_TIME)

pygame.quit()
