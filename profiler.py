import cProfile

pr = cProfile.Profile()
pr.enable()
import game
pr.disable()
pr.print_stats()
