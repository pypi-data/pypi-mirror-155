import gym
import matplotlib.pyplot as plt
import torch.nn as nn
import torch as T
import torch.optim as optim
import torch.nn.functional as F
import numpy as np
from agent import Discrete_A2C_Agent
import matplotlib.pyplot as plt
from utils import plotLearning


class GenericNetwork(nn.Module):
    def __init__(self, lr, input_dims, n_actions, fc1_dims, fc2_dims):
        super(GenericNetwork, self).__init__()
        self.input_dims = input_dims
        self.n_actions = n_actions
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims

        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.v = nn.Linear(self.fc2_dims, 1)
        self.pi = nn.Linear(self.fc2_dims, self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, observation):
        x = F.relu(self.fc1(observation))
        x = F.relu(self.fc2(x))
        pi = F.softmax(self.pi(x))

        return pi

class CriticNetwork(nn.Module):
    def __init__(self, lr, input_dims, n_actions, fc1_dims, fc2_dims):
        super(CriticNetwork, self).__init__()
        self.input_dims = input_dims
        self.n_actions = n_actions
        self.fc1_dims = fc1_dims
        self.fc2_dims = fc2_dims

        self.fc1 = nn.Linear(*self.input_dims, self.fc1_dims)
        self.fc2 = nn.Linear(self.fc1_dims, self.fc2_dims)
        self.v = nn.Linear(self.fc2_dims, 1)
        self.pi = nn.Linear(self.fc2_dims, self.n_actions)

        self.optimizer = optim.Adam(self.parameters(), lr=lr)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, observation):
        x = F.relu(self.fc1(observation))
        x = F.relu(self.fc2(x))
        v = self.v(x)

        return v

if __name__ == '__main__':
    env = gym.make('CartPole-v0')
                    
    actor = GenericNetwork(lr=5e-5, input_dims=[4], fc1_dims=1024, 
                                fc2_dims=512, n_actions=2)
    critic = CriticNetwork(lr=5e-5, input_dims=[4], fc1_dims=1024, 
                                fc2_dims=512, n_actions=1)
    agent = Discrete_A2C_Agent(actor, critic)  
    
    score_history = []
    n_episodes = 2500

    for i in range(n_episodes):
        done = False
        score = 0
        observation = env.reset()
        while not done:
            action = agent.get_action(observation)
            observation_, reward, done, info = env.step(action)
            agent.learn(observation, reward, observation_, done)
            observation = observation_
            score += reward
        score_history.append(score)
        print('episode ', i, 'score %.1f' % score, 'average_score %1.f' % np.mean(score_history[-100:]))
        
    
    filename = 'lunar-lander-alpha001-128x128fc-newG.png'
    plotLearning(score_history, filename=filename, window=25)