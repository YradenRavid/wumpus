
class Orientation:
    def __new__(cls,curr_orientation, *args, **kwargs):
        print("Creating instance")
        return super(Orientation, cls).__new__(cls, *args, **kwargs)

    def __init__(self, curr_orientation, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.possible_orientations = ["East","North","West","South"]
        self.curr_orientation = curr_orientation
        
    def turn_left(self):
        self.orintation_ind = self.possible_orientations.index(self.curr_orientation)
        left_ind = (self.orintation_ind + 1) % len(self.possible_orientations)
        self.curr_orientation = self.possible_orientations[left_ind]

    def turn_right(self):
        self.orintation_ind = self.possible_orientations.index(self.curr_orientation)
        right_ind = (self.orintation_ind - 1) % len(self.possible_orientations)
        self.curr_orientation = self.possible_orientations[right_ind]


class AgentState:
    def __new__(cls):
        print("Creating instance")
        return super(AgentState, cls).__new__(cls)

    def __init__(self,location=(0,0), orientation = Orientation("East"), hasGold = False, hasArrow= True, isAlive = True):
        self.reset(location, orientation, hasGold, hasArrow, isAlive)
    
    def reset(self,location, orientation, hasGold, hasArrow, isAlive):
        self.location = location
        self.orientation = orientation
        self.hasGold = hasGold
        self.hasArrow = hasArrow
        self.isAlive = isAlive

    def turn_left(self):
        self.orientation.turn_left()

    def turn_right(self):
        self.orientation.turn_right()

    def forward(self,gridWidth,gridHeight):
        match self.orientation.curr_orientation:
            case "East":
                self.location = (self.location[0], min(gridWidth - 1, self.location[1] + 1))
            case "West":
                self.location = (self.location[0], max(0, self.location[1] - 1))
            case "South":
                self.location = (max(0, self.location[0] - 1), self.location[1])
            case "North":
                self.location = (min(gridHeight - 1, self.location[0] + 1), self.location[1])
    


     

        



