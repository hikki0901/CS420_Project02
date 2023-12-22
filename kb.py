class knownNode:
    def __init__(self, x, y, isPit, isWumpus):
        self.x = x
        self.y = y
        # 0: unknown, 1: maybe, 2: yes, 3: no
        self.isPit = isPit
        self.isWumpus = isWumpus
    