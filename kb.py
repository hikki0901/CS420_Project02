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
        print(f"Node at ({self.x}, {self.y}):")
        print(f"isPit: {self.get_status(self.isPit)}")
        print(f"isWumpus: {self.get_status(self.isWumpus)}")
        

    def get_status(self, value):
            status_map = {0: 'Unknown', 1: 'Maybe', 2: 'Yes', 3: 'No', -1: 'Unknown'}
            return status_map.get(value, 'Unknown')
    
    # def get_pos(self):
    #     return self.x, self.y
    