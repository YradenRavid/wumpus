from Environment import EnvironmentState
from Agent import Agent

def RunGame():
    env = EnvironmentState()
    env.Visualization()
    while not env.terminated: 
        action = Agent.next_action()
        print("Action: ", action)
        perc = env.applyAction(action)
        env.Visualization()
        print("perc: ", perc)
        total_reward += perc.reward
        print("Total Reward: ", total_reward)
        
if __name__ == "__main__":
    RunGame()