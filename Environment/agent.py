
class Orientation:
    def __init__(self,curr_orientation):
        self.possible_orientations = ["East","North","West","South"]
        self.curr_orientation = curr_orientation
        self.orintation_ind = self.possible_orientations.index(curr_orientation)

    def turn_left(self):
        left_ind = (self.orintation_ind + 1) % len(self.possible_orientations)
        self.curr_orientation = self.possible_orientations[left_ind]

    def turn_left(self):
        right_ind = (self.orintation_ind - 1) % len(self.possible_orientations)
        self.curr_orientation = self.possible_orientations[right_ind]


class AgentActions:
    def __init__(self,location=(0,0), orientation = Orientation("East"), hasGold = False, hasArrow= True, isAlive = True):
        self.location = location
        self.orientation = orientation,
        self.hasGold = hasGold
        self.hasArrow = hasArrow
        self.isAlive = isAlive

    def trun_left(self):
        self.orientation = self.orientation.turn_left()

    def trun_right(self):
        self.orientation = self.orientation.turn_right()

    def forward(self,gridWidth,gridHeight):
        match self.orientation.curr_orientation:
            case "East":
                self.location = (min(gridWidth - 1, self.location[0] + 1), self.location[1])
            case "West":
                self.location = (max(0, self.location[0] - 1), self.location[1])
            case "South":
                self.location = (self.location[0], max(0, self.location[1] - 1))
            case "North":
                self.location = (self.location[0], min(gridHeight - 1, self.location[1] + 1))
    

     

        



