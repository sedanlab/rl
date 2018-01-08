from collections import defaultdict
import random

class DecisionMaker:
    def __init__(self, env):
        """
        init DecisionMaker

        Parameters
        ----------
        env : Model

        """
        self.env = env

    def _expected_utility(self, a, s, U):
        """The expected utility of doing a in state s, according to the MDP and U."""
        return sum([p * U[s1] for (p, s1) in self.env.get_transition(s, a)])

    def _best_policy(self, value_U, option=max):
        pi = {}
        
        for s in self.env.states:
            pi[s] = option(self.env.get_actions(s), key=lambda a: self._expected_utility(a, s, value_U))
        return pi

    def ValueIteration(self, discount, epoch=10, threshold=None, max_iteration=999999):
        if not 0 < discount <= 1:
            raise ValueError('discount must (0,1]')
       
        # option of epoch or threshold
        if threshold == None:
            pass
        else:
            epoch = True

        value_U = {s : 0 for s in self.env.states}
        iter = 0
        while epoch and iter < max_iteration:
            value_U_t = value_U.copy()
            delta = 0
            for state in self.env.states:
                
                lists = [sum([p * value_U_t[s1] for (p, s1) in self.env.get_transition(state, action)]) for action in self.env.get_actions(state)]
            
                #print(lists)
                value_U[state] = self.env.get_reward(state) + discount * max(lists)
                delta = max(delta, abs(value_U[state] - value_U_t[state]))
            
            if (threshold != None) and (delta < threshold):
                return value_U, self._best_policy(value_U)

            epoch = True if type(epoch) == type(True) else epoch-1
            iter += 1
        
        return value_U, self._best_policy(value_U)

    def _f(self, u, n, Ne, Rplus):
        """ Exploration function. Returns fixed Rplus until
        agent has visited state, action a Ne number of times.
        Same as ADP agent in book."""
        if n < Ne:
            return Rplus
        else:
            return u
    
    #### _f -> by epsilon greedy explore random

    def QLearning(self, initial_state, discount, Rplus, Ne, alpha=None, epoch=10):
        if initial_state not in self.env.states:
            raise ValueError('initial_state must be in environment')
        
        current_state = initial_state

        Q = defaultdict(float)
        Nsa = defaultdict(float)
        s = a = r = None

        if alpha is None:
            alpha = lambda n: 1./(1+n)

        while epoch:

            current_reward = self.env.get_reward(current_state)

            if s in self.env.terminals: # if s is terminal
                Q[s, None] = current_reward
            
            if s is not None:
                Nsa[s, a] += 1
                Q[s, a] += alpha(Nsa[s,a]) * (r + discount * max(Q[current_state, a1] for a1 in self.env.get_actions(current_state)) - Q[s, a])

            if s in self.env.terminals: # if s is terminal
                s = a = r = None
            else:
                s, r = current_state, current_reward
                a = max(self.env.get_actions(current_state), key=lambda current_reward: self._f(Q[current_state, current_reward], Nsa[current_state, current_reward], Ne, Rplus))
            next_action = a

            if next_action is None:
                current_state = initial_state

            else:
                x = random.uniform(0, 1)
                cumulative_prob = 0.0
                for prob_state in self.env.get_transition(current_state, next_action):
                    prob, state = prob_state
                    cumulative_prob += prob
                    if x < cumulative_prob:
                        break

                current_state = state

            epoch = True if type(epoch) == type(True) else epoch-1
        
        U = defaultdict(lambda: -1000.) # Very Large Negative Value for Comparison see below.

        for state_action, value in Q.items():
            state, _ = state_action
            if U[state] < value:
                U[state] = value

        return Q, U, self._best_policy(U,option=min)