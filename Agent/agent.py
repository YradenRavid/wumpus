import random

class Agent:
    
    def next_action(percept):
        match random.randint(0,5):
            case 0: return "Forward"
            case 1: return "TrunLeft"
            case 2: return "TrunRight"
            case 3: return "Shoot"
            case 4: return "Grab"
            case 5: return "Climb"
    
