import random
import numpy as np
from collections import defaultdict

def util_2DtoMDP(matrix):
    '''
    2D Matrix to Markov Decision Process

    Parameters 
    ----------
    matrix : list
        matrix.shape == (rows, cols)
    '''
    matrix = np.asarray(matrix)
    rows = matrix.shape[0] 
    cols = matrix.shape[1]

    mdp = defaultdict(dict)
    mdp_reward = defaultdict(float)

    for x in range(rows):
        for y in range(cols):
            actions = {}

            if not x == 0: # can go up
                actions['up'] = {(x-1,y) : 1.0}
            if not x == rows - 1: # can go down
                actions['down'] = {(x+1,y) : 1.0}
            if not y == 0: # can go left
                actions['left'] = {(x, y-1) : 1.0 }
            if not y == cols - 1: # can go right
                actions['right'] = {(x,y+1) : 1.0}
            actions['stop'] = {(x,y) : 1.0}

            mdp[(x,y)] = actions

            mdp_reward[(x,y)] = matrix[x,y]
    
    return mdp, mdp_reward

class MarkovDecisionProcess:

    def __init__(self, env, rewards=(0,1)):
        """
        defines Markov Decision Process
        
        Parameters
        ----------
        env : set[state][action][transitions]
            {
                "A": {
                        "X": {"A":0.3, "B":0.7},
                        "Y": {"A":1.0}
                    },
                "B": {
                        "X": {"End":0.8, "B":0.2},
                        "Y": {"A":1.0}
                    },
                "End": {}
            }
        
        rewards : None or 0 or dict
            (from,to) => random init with int
            0 = > 0 init
            dict =>
            {
                "A": 5,
                "B": -10,
                "End": 100
            }
        """
        self.states = list(env.keys())
        self.actions = {}

        for state in self.states:
            self.actions[state] = list(env[state].keys())
        
        self.transitions = {}

        for state in self.states:
            for action in self.actions[state]:
                action_results = env[state][action]
                act = []
                for action_result_key in action_results.keys():
                    # (prob, change_state)
                    act.append((env[state][action][action_result_key], action_result_key))
                key_exist = state in self.transitions.keys()
                if not key_exist:
                    self.transitions[state] = {}
                self.transitions[state][action] = act

        if type(rewards) == type(()):
            self.reward = {}
            for state in self.states:
                self.reward[state] = random.random() * (rewards[1] - rewards[0]) - rewards[0]
        elif rewards == 0:
            for state in self.states:
                self.reward[state] = 0
        elif type(rewards) == type({}) or type(rewards) == type(defaultdict()):
            if not (set(rewards.keys()) == set(self.states)):
                raise ValueError('Wrong reward')
            self.reward = rewards
        else:
            raise ValueError('Wrong reward')

        self.terminals = []
        for state in self.states:
            if state not in self.transitions.keys():
                self.terminals.append(state)

    # must overide
    def get_reward(self, state):
        """
        get current reward

        Parameters
        ----------
        state : str or int
            State id

        Returns
        ----------
        float
            State's value
        """
        return self.reward[state]
    
    def get_transition(self, state, action):
        """
        calculate P(s'|s,a)

        Parameters
        ----------
        state : str or int
            State id
        action : str or int
            Action id
        
        Returns
        ----------
        list 
            [(probabilty, result-state)] pairs
        """
        if state not in self.transitions.keys():
            return [(0.0, state)]

        return self.transitions[state][action]
    
    def get_actions(self, state):
        """
        Set of action can be performed from this state

        Parameters
        ----------
        state : str or int
            State id
        
        Returns
        ----------
        list
            Action list
        """
        if self.actions[state] == []:
            return [None]
        return self.actions[state]

