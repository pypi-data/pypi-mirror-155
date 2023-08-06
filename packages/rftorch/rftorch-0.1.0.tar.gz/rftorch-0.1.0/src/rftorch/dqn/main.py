import gym
import torch.nn as nn
import torch.nn.functional as F
import torch as T
import torch.optim as optim
from agent import DQN_agent
import numpy as np
from utils import plotLearning

class DeepQNetwork(nn.Module):
    def __init__(self, lr, input_dims, fc1_dims, fc2_dims, n_actions):
        super(DeepQNetwork, self).__init__()
        self.input_shape = input_dims
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims
        self.n_actions = n_actions

        self.fc1 = nn.Linear(*self.input_shape, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.fc3 = nn.Linear(self.fc2_dims, self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.loss = nn.MSELoss()
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        actions = self.fc3(x)

        return actions

if __name__ == '__main__':
    env = gym.make('LunarLander-v2')
    network = DeepQNetwork(lr=1e-3, input_dims=[8], fc1_dims=256, fc2_dims=256, n_actions=4)
    agent = DQN_agent(network)
    scores, eps_history = [], []
    n_games = 1000

    for i in range(n_games):
        score = 0
        done = False
        observation = env.reset()
        while not done:
            action = agent.epsilon_greedy(observation)
            observation_, reward, done, info = env.step(action)
            score += reward
            agent.memory.save_memory(observation, action, reward,
                                    observation_, done)
            agent.learn()
            observation = observation_
            #env.render()
        scores.append(score)
        eps_history.append(agent.epsilon)
        avg_score = np.mean(scores[-100:])

        print('episode: ', i, 'score %.2f' % score,
                'average score %.2f' % avg_score,
                'epsilon %.2f' % agent.epsilon)
    
    x = [i+1 for i in range(n_games)]
    plotLearning(x, scores, eps_history, 'graph.png')