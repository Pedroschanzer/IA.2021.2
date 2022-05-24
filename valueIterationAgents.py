import mdp, util
import numpy as np

from learningAgents import ValueEstimationAgent


class ValueIterationAgent(ValueEstimationAgent):
    """
        * Please read learningAgents.py before reading this.*

        A ValueIterationAgent takes a Markov decision process
        (see mdp.py) on initialization and runs value iteration
        for a given number of iterations using the supplied
        discount factor.
    """

    def __init__(self, mdp, discount=0.9, iterations=100):
        """
          Your value iteration agent should take an mdp on
          construction, run the indicated number of iterations
          and then act according to the resulting policy.

          Some useful mdp methods you will use:
              mdp.getStates()
              mdp.getPossibleActions(state)
              mdp.getTransitionStatesAndProbs(state, action)
              mdp.getReward(state, action, nextState)
              mdp.isTerminal(state)
        """
        self.mdp = mdp
        self.discount = discount
        self.iterations = iterations
        self.values = util.Counter()  # A Counter is a dict with default 0

        # Write value iteration code here
        for _ in range(self.iterations):
            vals = self.values.copy()
            for state in mdp.getStates():
                if not(mdp.isTerminal(state)):
                    b_action = self.computeActionFromValues(state)
                    vals[state] = self.computeQValueFromValues(state, b_action)
            self.values = vals.copy()

    def getValue(self, state):
        """
          Return the value of the state (computed in __init__).
        """
        return self.values[state]

    def computeQValueFromValues(self, state, action):
        """
          Compute the Q-value of action in state from the
          value function stored in self.values.
        """
        if action in self.mdp.getPossibleActions(state):
            prob = self.mdp.getTransitionStatesAndProbs(state, action)
            value = sum([prob[i][1] * (self.mdp.getReward(state, action, prob[i][0]) + self.discount * self.values[prob[i][0]]) for i in range(len(prob))])
            return value
        else:
            return 0

    def computeActionFromValues(self, state):
        """
          The policy is the best action in the given state
          according to the values currently stored in self.values.

          You may break ties any way you see fit.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return None.
        """
        if self.mdp.getPossibleActions(state):
            pa = self.mdp.getPossibleActions(state)
            return pa[np.argmax([self.computeQValueFromValues(state, a) for a in pa])]
        else:
            return None

    def getPolicy(self, state):
        return self.computeActionFromValues(state)

    def getAction(self, state):
        "Returns the policy at the state (no exploration)."
        return self.computeActionFromValues(state)

    def getQValue(self, state, action):
        return self.computeQValueFromValues(state, action)