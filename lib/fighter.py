class Fighter():
    def __init__(self):
        self.hp = 0
        self.hp_max = 0
        self.spd = 0

def SampleFighter():
    f = Fighter()
    f.hp_max = f.hp = 100
    f.spd = 20
    return f
