from Environment import EnvironmentState, Percept
from Agent import Agent

def RunGame():
    env = EnvironmentState()
    print("Board Intilization:")
    env.Visualization()
    perc = Percept(env.agent.location, env.perceptions)
    print("Percept: ", perc)
    agent = Agent()
    total_reward = 0
    while not env.terminated: 
        print("curr orientation: ",env.agent.orientation.curr_orientation)
        action = agent.next_action(percept=perc,agent_orientation=env.agent.orientation.curr_orientation)
        print("Action: ", action)
        perc = env.ApplyAction(action)
        env.Visualization()
        print("Percept: ", perc)
        total_reward += perc.reward
        print("Total Reward: ", total_reward)
    return total_reward
        
if __name__ == "__main__":
    total_reward = 0
    for i in range(1000):
        total_reward+= RunGame()
    print("Average Score:", total_reward/1000)