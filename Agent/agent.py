from itertools import product, combinations

import random
from Environment.constants import *
from Agent.PathUtils import ShotestPath


class Agent:
    def __init__(self):
        self.hasGold = False
        self.safe_locations = []
        self.escape_plan = []
        self.next_location = (0,0)
        self.pit_prob = 0.2
        # belief state variables:
        self.stench_locations = []
        self.breeze_locations = []
        self.scream_heard = False
        self.next_steps_risks = []
        self.Wumpus_loc = None
        self.Wumpus_prob = {}
        self.has_arrow = True
        self.just_shot = False
        self.location_with_no_wumpus = []
        self.location_with_no_pit = []

    
    def next_action(self,percept,agent_orientation):
        
        next_possible_steps = self.find_neighbors([percept.agent_location])
        print("next_possible_steps: ",next_possible_steps)
        pit_prob = {}
        
        if percept.scream:
            print("Scream was heard")
            self.scream_heard = True
            self.Wumpus_prob = {}

        if self.just_shot and not self.scream_heard:
            self.just_shot = False
            # update safe location after shoot
            match agent_orientation:
                case "West":
                    self.location_with_no_wumpus.extend([(percept.agent_location[0],i) for i in range(percept.agent_location[1]+1,GRIDWIDTH)])
                case "East":
                    self.location_with_no_wumpus.extend([(percept.agent_location[0],i) for i in range(percept.agent_location[1])])
                case "South":
                    self.location_with_no_wumpus.extend([(i,percept.agent_location[1]) for i in range(percept.agent_location[0]+1,GRIDHEIGHT)])
                case "North":
                    self.location_with_no_wumpus.extend([(i,percept.agent_location[1]) for i in range(percept.agent_location[0])])

        if not percept.agent_location in self.safe_locations:
            self.safe_locations.append(percept.agent_location)
            self.location_with_no_wumpus.append(percept.agent_location)
            self.location_with_no_pit.append(percept.agent_location)

        if percept.stench and not self.Wumpus_loc and not self.scream_heard:
            self.stench_locations.append(percept.agent_location)
            self.calc_wumpus_prob()
            if self.should_shoot():
                self.has_arrow = False
                self.just_shot = True
                return "Shoot"
        else:
            self.location_with_no_wumpus.extend(next_possible_steps)
            self.location_with_no_wumpus = list(set(self.location_with_no_wumpus))
        
        if percept.breeze:
            self.breeze_locations.append(percept.agent_location)
            Pbreeze, possible_pits_combinations, Nmax = self.calc_breeze_prob()
            pit_prob = {}
            for next_possible_step in next_possible_steps:
                pit_prob[next_possible_step] = self.calc_pits_prob_in_loc(next_possible_step,Pbreeze,possible_pits_combinations,Nmax)
        else:
            self.location_with_no_pit.extend(next_possible_steps)
            self.location_with_no_pit = list(set(self.location_with_no_pit))

        if percept.glitter and not self.hasGold:
            self.hasGold = True
            graph = ShotestPath.safe_locations_to_graph(self.safe_locations)
            self.escape_plan = ShotestPath.bfs_escape_plan(graph,percept.agent_location,(0,0))
            print("That's the escape plan:")
            print(self.escape_plan)
            print("Safe locations:")
            print(self.safe_locations)
            return "Grab"
        
        if self.escape_plan:
            if percept.agent_location == (0,0):
                return "Climb"
            return ShotestPath.calc_next_step_escape(percept.agent_location,agent_orientation,self.escape_plan)

        if self.next_location != percept.agent_location:
            return ShotestPath.calc_next_step(percept.agent_location,agent_orientation,self.next_location)
        
        dying_prob = {}
        for next_possible_step in next_possible_steps:
            dying_prob[next_possible_step] = self.Wumpus_prob[next_possible_step] if next_possible_step in self.Wumpus_prob.keys() else 0
            dying_prob[next_possible_step] += pit_prob[next_possible_step] if next_possible_step in pit_prob.keys() else 0

        print("dying_prob:",dying_prob)
        print("min:",min(dying_prob.values()))
        if min(dying_prob.values()) > 0.5:
            graph = ShotestPath.safe_locations_to_graph(self.safe_locations)
            self.escape_plan = ShotestPath.bfs_escape_plan(graph,percept.agent_location,(0,0))
            print("Too risky - climbing out without gold")
            print("That's the escape plan:")
            print(self.escape_plan)
            print("Safe locations:")
            print(self.safe_locations)
            return ShotestPath.calc_next_step_escape(percept.agent_location,agent_orientation,self.escape_plan)

        next_possible_locations = [loc for loc,prob in dying_prob.items() if prob==0 and loc not in self.safe_locations]
        if next_possible_locations:
            self.next_location = random.choice(next_possible_locations) 
        else:
            zero_dying_prob_next_loc = [loc for loc,prob in dying_prob.items() if prob==0]
            if zero_dying_prob_next_loc:
                self.next_location = random.choice(zero_dying_prob_next_loc)
            else: 
                self.next_location = min(dying_prob, key=dying_prob.get)
        print("next_location:",self.next_location)
        return ShotestPath.calc_next_step(percept.agent_location,agent_orientation,self.next_location)
    
    
    def adjacentCells(self,locations):
        cells = []
        for location in locations:
            if (location[0] > 0) and (location[1] > 0):
                    cells.append((location[0]-1,location[1]))
            if (location[1] > 0) and (location[1] > 0):
                    cells.append((location[0],location[1]-1))
            if location[0] < GRIDWIDTH - 1:
                    cells.append((location[0]+1,location[1]))
            if location[1] < GRIDHEIGHT - 1:
                    cells.append((location[0],location[1]+1))
        return cells

    def find_neighbors(self,locations):
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

    def should_shoot(self):
        if not self.has_arrow:
            return False
        if min(self.Wumpus_prob.values()) > 0.3:
            return True
            
    def calc_wumpus_prob(self):
        possible_wumpus = set([(x,y) for x,y in list(product(range(GRIDWIDTH),range(GRIDHEIGHT))) if x or y ])
        print("stench_locations:",self.stench_locations)
        for stench_loc in self.stench_locations:
            possible_wumpus1 = self.adjacentCells([stench_loc])
            possible_wumpus1 = set(possible_wumpus1) - set(self.location_with_no_wumpus)
            possible_wumpus = possible_wumpus.intersection(possible_wumpus1)
        print("possible_wumpus:",possible_wumpus)
        self.Wumpus_prob = {loc: 1/(len(possible_wumpus)) for loc in possible_wumpus}
        print("Wumpus_prob:")
        print(self.Wumpus_prob)
        if 1 in self.Wumpus_prob.values() and not self.Wumpus_loc:
            print("Wumpus location Found!")
            self.Wumpus_loc = next(iter(self.Wumpus_prob))
            print(self.Wumpus_loc) 

    def calc_breeze_prob(self):
        possible_pits = set()
        print("breeze_locations:",self.breeze_locations)
        print("location_with_no_pit:", self.location_with_no_pit)
        for breeze_loc in self.breeze_locations:
            possible_pits1 = self.adjacentCells([breeze_loc])
            possible_pits1 = set(possible_pits1) - set(self.location_with_no_pit)
            possible_pits = possible_pits.union(possible_pits1)
        print("possible_pits",possible_pits)
        possible_pits_combinations = []
        Nmax = len(possible_pits)
        for i in range(Nmax):
            for pit_combination in combinations(list(possible_pits),i+1):
                print("check validation for pit_combination:",pit_combination)
                possible_breeze = self.adjacentCells(list(pit_combination))
                print("possible_breeze: {} for pit_combination".format(possible_breeze))
                print("self.breeze_locations",self.breeze_locations)
                if (set(self.breeze_locations) - set(possible_breeze)): # exsit breeze with no possible breeze
                    possible_pits_combinations.append(pit_combination)
        Pbreeze = 0
        print("possible_pits_combinations",possible_pits_combinations)
        for pit_combination in possible_pits_combinations:
            Pbreeze += self.pit_prob ** len(pit_combination) * (1-self.pit_prob) ** (Nmax-len(pit_combination))
        print("Pbreeze:", Pbreeze)
        return Pbreeze, possible_pits_combinations, Nmax  
    
    def calc_pits_prob_in_loc(self, next_possible_step,Pbreeze,possible_pits_combinations,Nmax):        
        print("calc prob for location:", next_possible_step)
        Pbreeze_inter_pitinloc = 0
        for pit_combination in possible_pits_combinations:
            if next_possible_step in pit_combination: # exsit breeze with no possible breeze
                Pbreeze_inter_pitinloc += self.pit_prob ** len(pit_combination) * (1-self.pit_prob) ** (Nmax-len(pit_combination))
        print("pit prob in {} is {}".format(next_possible_step,Pbreeze_inter_pitinloc/Pbreeze))
        return Pbreeze_inter_pitinloc/Pbreeze

    


    
