from Environment import EnvironmentState, Percept
from Agent import Agent

def RunGame():
    env = EnvironmentState()
    print("Board Intilization:")
    env.Visualization()
    perc = Percept(env.agent.location, env.perceptions)
    total_reward = 0
    while not env.terminated: 
        print("curr orientation: ",env.agent.orientation.curr_orientation)
        action = Agent.next_action(percept=perc,agent_orientation=env.agent.orientation.curr_orientation)
        print("Action: ", action)
        perc = env.ApplyAction(action)
        env.Visualization()
        print("Percept: ", perc)
        total_reward += perc.reward
        print("Total Reward: ", total_reward)
        
if __name__ == "__main__":
    RunGame()