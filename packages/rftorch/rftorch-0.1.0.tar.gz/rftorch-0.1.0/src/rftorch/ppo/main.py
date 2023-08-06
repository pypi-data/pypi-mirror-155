import gym
import torch.nn as nn
import torch.nn.functional as F
import torch as T
import torch.optim as optim
from torch.distributions.categorical import Categorical
from agent import Discrete_PPO_Agent
import numpy as np
from utils import plotLearning

class Actor_Network(nn.Module):
    def __init__(self, n_actions, input_dims, alpha, fc1_dims=256, fc2_dims=256):
        super(Actor_Network, self).__init__()
        self.actor = nn.Sequential(
            nn.Linear(*input_dims, fc1_dims),
            nn.ReLU(),
            nn.Linear(fc1_dims, fc2_dims),
            nn.ReLU(),
            nn.Linear(fc2_dims, n_actions),
            nn.Softmax(dim=-1)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        dist = self.actor(state)
        dist = Categorical(dist)

        return dist

class Critic_Network(nn.Module):
    def __init__(self, input_dims, alpha, fc1_dims=256, fc2_dims=256):
        super(Critic_Network, self).__init__()
        self.critic = nn.Sequential(
            nn.Linear(*input_dims, fc1_dims),
            nn.ReLU(),
            nn.Linear(fc1_dims, fc2_dims),
            nn.ReLU(),
            nn.Linear(fc2_dims, 1)
        )

        self.optimizer = optim.Adam(self.parameters(), lr=alpha)
        self.device = T.device('cuda:0' if T.cuda.is_available() else 'cpu')
        self.to(self.device)

    def forward(self, state):
        value = self.critic(state)

        return value

if __name__ == '__main__':
    env = gym.make('CartPole-v0')
    N = 20
    batch_size = 5
    n_epochs = 4
    alpha = 0.0001
    actor = Actor_Network(n_actions = env.action_space.n, input_dims=env.observation_space.shape, alpha=alpha)
    critic = Critic_Network(input_dims=env.observation_space.shape, alpha=alpha)
    agent = Discrete_PPO_Agent(actor, critic, batch_size=batch_size, n_epochs=n_epochs)
    n_games = 1000

    best_score = env.reward_range[0]
    score_history = []
    learn_iters = 0
    avg_score = 0
    n_steps = 0
    
    for i in range(n_games):
        score = 0
        done = False
        observation = env.reset()
        while not done:
            action, prob, val = agent.get_eval_action(observation)
            observation_, reward, done, info = env.step(action)
            n_steps += 1
            score += reward
            agent.memory.save_memory(observation, action, prob, val, reward, done)
            if n_steps % N == 0:
                agent.learn()
                learn_iters += 1
            observation = observation_
            #env.render()
        score_history.append(score)
        avg_score = np.mean(score_history[-100:])

        print('episode: ', i, 'score %.2f' % score,
                'average score %.2f' % avg_score,
                'time steps %.2f' % n_steps, 'learning steps', learn_iters)
    
    x = [i+1 for i in range(n_games)]
    plotLearning(score_history, 'graph.png', window=100)