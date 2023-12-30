class knownNode:
    def __init__(self, x, y, isPit, isWumpus, x_knowledge, y_knowledge):
        self.x = x
        self.y = y
        self.countVisit = 0
        # 0: unknown, 1: maybe, 2: yes, 3: no
        self.isPit = isPit
        self.isWumpus = isWumpus

        # 0: false, 1: true, -1: unknown
        self.isBreeze = -1
        self.isStench = -1

        # position to gain knowledge from
        self.x_knowledge = x_knowledge
        self.y_knowledge = y_knowledge

    def print_status(self):
        print(f"({self.get_status(self.isPit)}isPit ^ {self.get_status(self.isWumpus)}isWumpus)({self.x}, {self.y})")
        

    def get_status(self, value):
            status_map = {2: '', 3: '~'}
            return status_map.get(value, 'Unknown')
    
    # def get_pos(self):
    #     return self.x, self.y
    