import random
from itertools import product
from Environment import AgentState
from Environment.constants import *

class EnvironmentState:
    def __new__(cls):
         print("Creating instance")
         return super(EnvironmentState, cls).__new__(cls)
    
    def __init__(self,pitProb=0.2,allowClimbWithoutGold=True,terminated=False,wumpusAlive=True):
        self.reset(pitProb,allowClimbWithoutGold,terminated,wumpusAlive)
    
    def reset(self,pitProb,allowClimbWithoutGold,terminated,wumpusAlive):
        self.pitProb = pitProb
        self.allowClimbWithoutGold = allowClimbWithoutGold
        self.agent = AgentState()
        self.pitLocations = self.set_pits_locations()
        print("self.pitLocations",self.pitLocations)
        self.terminated = terminated
        self.wumpusLocation = self.set_single_location()
        print("self.wumpusLocation", self.wumpusLocation)
        self.wumpusAlive = wumpusAlive
        self.goldLocation = self.set_single_location()
        print("self.goldLocation", self.goldLocation)
        self.perceptions = Perceptions(self)

    def set_pits_locations(self):
        pit_locations = []
        for i,j in list(product(range(GRIDWIDTH),range(GRIDHEIGHT))):
            if i == 0 and j == 0:
                continue
            if random.random() < self.pitProb:
                pit_locations.append((i,j))
        return pit_locations

    def set_single_location(self):
        randinteger = random.randint(1,GRIDWIDTH*GRIDHEIGHT-1)
        x_location = int(randinteger / GRIDWIDTH)
        y_location = randinteger % GRIDHEIGHT
        return (x_location,y_location)
    
    def ApplyAction(self, action):
        
        if self.agent.hasGold:
            self.goldLocation = self.agent.location

        if self.terminated:
            return Percept(self.agent.location, self.perceptions, isTerminated=True,reward= 0)
        match action:
            
            case "Forward": 
                old_location = self.agent.location
                self.agent.forward(GRIDWIDTH,GRIDHEIGHT)
                if self.agent.hasGold:
                    self.goldLocation = self.agent.location
                isDead = (self.agent.location == self.wumpusLocation) and self.wumpusAlive
                isDead = isDead or (self.agent.location in self.pitLocations)
                self.agent.isAlive = not isDead
                self.terminated = isDead
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
                    self.wumpusAlive = not(self.wumpusInLineOfFire() and self.agent.hasArrow) and self.wumpusAlive
                    if not self.wumpusAlive:
                        print("Wumpus just killed!")
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
                success = self.agent.hasGold and inStartLocation
                if success:
                    print("You Won!")
                self.terminated = success or (self.allowClimbWithoutGold and inStartLocation)
                return Percept(self.agent.location, self.perceptions, isTerminated=self.terminated, reward= 999 if success else -1)
    
    def wumpusInLineOfFire(self):
        match self.agent.orientation.curr_orientation:
            case "West":
                return (self.agent.location[0] == self.wumpusLocation[0]) and (self.agent.location[1] > self.wumpusLocation[1])
            case "East":
                return (self.agent.location[0] == self.wumpusLocation[0]) and (self.agent.location[1] < self.wumpusLocation[1])
            case "South":
                return (self.agent.location[0] > self.wumpusLocation[0]) and (self.agent.location[1] == self.wumpusLocation[1])
            case "North":
                return (self.agent.location[0] < self.wumpusLocation[0]) and (self.agent.location[1] == self.wumpusLocation[1])

    def Visualization(self):
        wumpusSymbol = "W" if self.wumpusAlive else "w"
        gameboard_string = ""
        for row in reversed(range(GRIDHEIGHT)):
            for col in range(0,GRIDWIDTH):
                if self.agent.location == (row,col):
                    gameboard_string+="A"
                else:
                    gameboard_string+=" "
                if (row,col) in self.pitLocations:
                    gameboard_string+="P"
                else:
                    gameboard_string+=" "
                if self.goldLocation == (row,col):
                    gameboard_string+="G"
                else:
                    gameboard_string+=" "
                if self.wumpusLocation == (row,col):
                    gameboard_string+=wumpusSymbol
                else:
                    gameboard_string+=" "
                gameboard_string+="|"
            gameboard_string+="\n"
        return gameboard_string

class Perceptions:
    def __new__(cls, env, *args, **kwargs):
         print("Creating instance")
         return super(Perceptions, cls).__new__(cls, *args, **kwargs)

    def __init__(self, env, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.reset(env)
    
    def reset(self,env):
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
        if agent_location in Perceptions.adjacentCells([self.env.wumpusLocation]):
            return True
        return False
    
    def isBreeze(self,agent_location):
        if agent_location in Perceptions.adjacentCells(self.env.pitLocations):
            return True
        return False

    def isGlitter(self,agent_location):
        if agent_location == self.env.goldLocation:
            return True
        return False


class Percept:
    def __init__(self, agent_location, perceptions ,bump=False, scream=False,isTerminated=False, reward= 0):
        self.stench = perceptions.isStench(agent_location)
        self.breeze = perceptions.isBreeze(agent_location)
        self.glitter = perceptions.isGlitter(agent_location)
        self.bump = bump
        self.scream = scream
        self.isTerminated = isTerminated 
        self.reward = reward
        self.agent_location = agent_location

    def __str__(self):
        return "stench: {}, breeze: {}, glitter: {}, bump: {}, scream: {}, isTerminated: {}, reward: {}".format(self.stench,self.breeze,self.glitter,self.bump,self.scream,self.isTerminated,self.reward)


        

