import random
from itertools import combinations
from Environment import AgentState

GRIDWIDTH = 4
GRIDHEIGHT = 4

class EnvironmentState:

    def __init__(self,gridWidth=GRIDWIDTH,gridHeight=GRIDHEIGHT,pitProb=0.2,
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
        self.goldLocation = self.set_single_location()
        self.perceptions = Perceptions(self)

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
            return Percept(self.agent.location, self.perceptions, isTerminated=True,reward= 0)
        match action:
            
            case "Forward": 
                old_location = self.agent.location
                self.agent.forward(self.gridWidth,self.gridHeight)
                isDead = (self.agent.location == self.wumpusLocation) & self.wumpusAlive
                isDead = isDead or (self.agent.location == any(self.pitLocations))
                self.agent.isAlive = not isDead
                return Percept(self.agent.location, self.perceptions,bump= old_location == self.agent.location,isTerminated=isDead,reward= -1 if self.agent.isAlive else -1001)
            
            case "TrunLeft": 
                self.agent.turn_left()
                return Percept(self.agent.location, self.perceptions,reward= -1)
            
            case "TrunRight": 
                self.agent.turn_right()
                return Percept(self.agent.location, self.perceptions,reward= -1)
            
            case "Shoot":
                if not self.wumpusAlive:
                    return Percept(self.agent.location, self.perceptions,reward= -1)
                else:
                    self.wumpusAlive = ~(self.wumpusInLineOfFire & self.agent.hasArrow) &  self.wumpusAlive
                if self.agent.hasArrow:
                    self.agent.hasArrow = False
                    return Percept(self.agent.location, self.perceptions, scream= False if self.wumpusAlive else True ,reward= -11)
                else:
                    return Percept(self.agent.location, self.perceptions, reward= -1)
            
            case "Grab": 
                self.agent.hasGold = self.agent.location == self.goldLocation
                return Percept(self.agent.location, self.perceptions, reward= -1)
            
            case "Climb": 
                inStartLocation = self.agent.location == (0,0)
                success = self.agent.hasGold & inStartLocation
                isTerminated = success | (self.allowClimbWithoutGold & inStartLocation)
                return Percept(self.agent.location, self.perceptions, isTerminated=isTerminated, reward= 999 if success else -1)
    
    def wumpusInLineOfFire(self):
        match self.agent.orientation.curr_orientation:
            case "West":
                return (self.agent.location[0] > self.wumpusLocation[0]) & (self.agent.location[1] == self.wumpusLocation[1])
            case "East":
                return (self.agent.location[0] < self.wumpusLocation[0]) & (self.agent.location[1] == self.wumpusLocation[1])
            case "South":
                return (self.agent.location[0] == self.wumpusLocation[0]) & (self.agent.location[1] > self.wumpusLocation[1])
            case "South":
                return (self.agent.location[0] == self.wumpusLocation[0]) & (self.agent.location[1] < self.wumpusLocation[1])

class Perceptions:
    def __init__(self, env):
        self.env = env
        
    @staticmethod
    def adjacentCells(locations):
        cells = []
        for location in locations:
            if location[0] > 0:
                cells.append((location[0]-1,location[1]))
            if location[1] > 0:
                cells.append((location[0],location[1]-1))
            if location[0] < GRIDWIDTH - 1:
                cells.append((location[0]+1,location[1]))
            if location[1] < GRIDHEIGHT - 1:
                cells.append((location[0],location[1]+1))
        return cells

    def isStench(self, agent_location):
        if any(Perceptions.adjacentCells([self.env.wumpusLocation])) == agent_location:
            return True
        return False
    
    def isBreeze(self,agent_location):
        if any(Perceptions.adjacentCells(self.env.pitLocations)) == agent_location:
            return True
        return False

    def isGlitter(self,agent_location):
        if agent_location == self.env.goldLocation:
            return True
        return False


class Percept:
    def __init__(self, agent_location, perceptions ,bump=False, scream=False,isTerminated=False, reward= -1):
        self.stench = perceptions.isStench(agent_location)
        self.breeze = perceptions.isBreeze(agent_location)
        self.glitter = perceptions.isGlitter(agent_location)
        self.bump = bump
        self.scream = scream
        self.isTerminated = isTerminated 
        self.reward = reward


        

class Visualization:
    pass