from gym import Env
from gym.spaces import Tuple,Discrete, Box
import numpy as np
from subset import subset
from random import randint

class Cardenv(Env):
    def __init__(self):
        self.action_space = Discrete(2)
        self.observation_space = np.zeros((6,2))
        self.state = np.zeros((6,2)) # initial
        self.user_hand = np.zeros((3,2)) # initial
        self.guess = 0

    def step(self, action):
        bank = np.concatenate([self.state[0:3, :],self.user_hand],1)
        claim_parameters = np.array(self.state[3:,0]) # 3x1
        claim_parameters = claim_parameters.astype(int)
        num_cards_in_claim = claim_parameters[2]
        card_value = claim_parameters[1]
        num_or_suit = claim_parameters[0]-1
        claim = card_value*np.ones((num_cards_in_claim,1))
        bank_copy = bank

        # account for 2's
        for i in range(len(claim)):
            if claim[i] not in bank_copy[:,num_or_suit] and (2 in bank_copy[:,0]):
                two_index = np.where(bank_copy[:,0]==2)
                bank_copy[two_index[0],num_or_suit] = claim[i]

        claim_validity = subset(bank_copy[:,num_or_suit],claim)
        reward = 1*(action == claim_validity)-1*(action != claim_validity)

        done = True # end game after one return
        info = {} # placeholder

        # set self.action as output
        self.guess = action
        return self.state, reward, done, info

    def reset(self):
        return self.state

# env = cardenv()
# env.state = np.array([3,3,5,3,3,0,0,0,0]) # example hand and double claim
# print(env.step(1))
# print(env.observation_space.sample())
