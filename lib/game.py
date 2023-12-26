import pygame

import lib.battle
import lib.dialog
import lib.grid
import lib.input
import lib.sys

DELAY_TIME = round(1 / lib.sys.FRAME_RATE * 1000)

pygame.init()

class Game():
    def __init__(self):
        self.screen = pygame.display.set_mode((lib.sys.DISPLAY_WIDTH, lib.sys.DISPLAY_HEIGHT))
        self.input = lib.input.Input()
        self.dialogs = lib.dialog.DialogStack()
        self.battle: None | lib.battle.Battle = None
        self.running = False
        self.enableGrid = False
        lib.grid.init(self.screen)

    def startBattle(self, battle: lib.battle.Battle):
        self.battle = battle

    def run(self):
        self.running = True
        while self.running:
            ### --- Event Handling ----------------------------------------- ###

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            ### --- Player Input ------------------------------------------- ###

            # Input gets tick() first to distribute input to components early.
            # This causes input to be distributed to all components before they
            # have a chance to do their tick().
            for what in self.input.tick():
                if what is lib.input.DEBUG1:
                    self.enableGrid = not self.enableGrid
                # Give input to dialogs first because they are on top.
                if self.dialogs.isCapturingInput():
                    self.dialogs.giveInput(what)
                elif self.battle is not None:
                    self.battle.giveInput(what)

            ### --- Tick --------------------------------------------------- ###

            self.battle.tick()
            self.dialogs.tick()

            ### --- Rendering ---------------------------------------------- ###

            # This should be the first step of rendering.
            self.screen.fill((0x00, 0x00, 0x00))

            self.battle.render(self.screen)
            # Render dialogs last so they are on top.
            self.dialogs.render(self.screen)

            if self.enableGrid:
                lib.grid.draw(self.screen)

            # This should be the last step of rendering.
            pygame.display.flip()

            ### --- Enforce Frame Limit ------------------------------------ ###

            pygame.time.delay(DELAY_TIME) # XXX: I want to be as close to 60 frame Hz as possible and I don't think this does it because of the other game loop activities above.
