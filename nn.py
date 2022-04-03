# This script trains for a number of epochs on randomly generated cards.
import numpy as np
from random import randint
import gym

from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory

from env import Cardenv


class Baby():
    def __init__(self):
        # states = env.observation_space.shape()
        self.states = 6
        # actions = env.action_space.n()
        self.actions = 2
        self.model = self.build_model()
        self.agent = self.build_agent()
        self.agent.compile(Adam(lr=1e-3), metrics=['mae']) #mean absolute error

    def build_model(self):
        model = Sequential()
        model.add(Flatten(input_shape=(1,self.states,2)))
        model.add(Dense(24, activation = 'relu')) # input state vector
        model.add(Dense(24, activation = 'relu'))
        model.add(Dense(self.actions, activation = 'linear')) #2 output
        return(model)

    def build_agent(self):
        policy = EpsGreedyQPolicy()
        memory = SequentialMemory(limit=50000, window_length=1)
        dqn = DQNAgent(model=self.model, nb_actions=self.actions, memory=memory, nb_steps_warmup=10,
        target_model_update=1e-2, policy=policy)
        return dqn

def make_and_verify_guess(user_hand, agent_hand, claim, dqn):
    env = Cardenv()
    # incrementally train model given some user input
    env.user_hand = user_hand
    env.state[0:3,:] = agent_hand
    env.state[3:,0] = claim  # placeholder: call function to generate user input for claim

    # play one round
    scores = dqn.test(env, nb_episodes=1, visualize=False, verbose = 0)
    guess =  bool(env.guess)

    # learn
    dqn.fit(env, nb_steps= 1, visualize=False, verbose=0) # nb_steps was 5000
    # print('right or wrong: ', scores.history['episode_reward'])

    return dqn, guess
