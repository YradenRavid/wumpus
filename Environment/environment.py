import random
from itertools import combinations
from agent import AgentState

class EnvironmentState:

    def __init__(self,gridWidth=4,gridHeight=4,pitProb=0.2,
                    allowClimbWithoutGold=False,agent=AgentState(),terminated=False,wumpusAlive=True):
        self.gridWidth = gridWidth
        self.gridHeight = gridHeight
        self.pitProb = pitProb
        self.allowClimbWithoutGold = allowClimbWithoutGold,
        self.agent = agent
        self.pitLocations = self.set_pits_locations()
        self.terminated = terminated
        self.wumpusLocation = self.set_single_location()
        self.wumpusAlive = wumpusAlive
        self.goldLocatio = self.set_single_location()

    def set_pits_locations(self):
        pit_locations = []
        for i,j in list(combinations(range(self.gridWidth),range(self.gridHeight))):
            if i == 0 and j == 0:
                continue
            if random.random() < self.pitProb:
                pit_locations.append((i,j))
        return pit_locations

    def set_single_location(self):
        randinteger = random(1,self.gridWidth*self.gridHeight+1)
        x_location = randinteger / self.gridWidth
        y_location = randinteger % self.gridHeight
        return (x_location,y_location)
    
    def ApplyAction(self, action):
        if self.terminated:
            return Percept(isTerminated=True,reward= 0)
        match action:
            case "Forward": 
                return 
            case 1: return "TrunLeft"
            case 2: return "TrunRight"
            case 3: return "Shoot"
            case 4: return "Grab"
            case 5: return "Climb"

class Percept:
    def __init__(self, stench=False, breeze=False, glitter=False, bump=False, 
                    scream=False,isTerminated=False, reward= -1):
        self.stench = stench, 
        self.breeze = breeze, 
        self.glitter = glitter
        self.bump = bump, 
        self.scream = scream, 
        self.isTerminated = isTerminated 
        self.reward = reward


        

class Visualization:
    pass