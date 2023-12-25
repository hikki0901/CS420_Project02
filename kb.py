class knownNode:
    def __init__(self, x, y, isPit, isWumpus):
        self.x = x
        self.y = y
        self.countVisit = 0
        # 0: unknown, 1: maybe, 2: yes, 3: no
        self.isPit = isPit
        self.isWumpus = isWumpus

        # 0: false, 1: true, -1: unknown
        self.isBreeze = -1
        self.isStench = -1
    
    # def get_pos(self):
    #     return self.x, self.y
    