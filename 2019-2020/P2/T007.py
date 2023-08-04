#87668 Joao Antunes Grupo 007
import random
import numpy 
import math

# LearningAgent to implement
# no knowledeg about the environment can be used
# the code should work even with another environment
class LearningAgent:
        # init
        # nS maximum number of states
        # nA maximum number of action per state
        def __init__(self,nS,nA):
                self.nS = nS
                self.nA = nA
                
                self.gamma = 0.9
                self.Q = numpy.zeros((self.nS, self.nA))
                self.learning_rate = 0.1
                
                self.epsilon = 1
                self.number_of_selections = numpy.zeros((self.nS, self.nA))
                self.n = 0
                self.actions = self.initialize_actions(self.nS)
        
        #Used to initialize the actions of every state
        #nS - nS maximum number of states
        #returns
        #action_list - list of empty lists to each state
        def initialize_actions(self,nS):
                action_list = []
                for i in range(nS):
                        action_list.append([])
                        
                return action_list        

        # Select one action, used when learning  
        # st - is the current state        
        # aa - is the set of possible actions
        # for a given state they are always given in the same order
        # returns
        # a - the index to the action in aa
        def selectactiontolearn(self,st,aa):                
                #e-greedy + UCB 1
                if random.random() < self.epsilon:
                        a = random.randint(0, len(aa) - 1)
                else:
                        Q_value = -math.inf
                        for i in range(len(aa)):
                                if self.Q[st - 1][i] > Q_value:
                                        Q_value = self.Q[st - 1][i]
                                        a = i
                                        
                a_aux = a               
                max_upper_bound = 0
                for i in range(0, len(aa)):
                        if self.number_of_selections[st-1][i] > 0:
                                upper_bound = self.Q[st-1][i] + math.sqrt((2*math.log(self.n))/(self.number_of_selections[st-1][i]))
                        else:
                                upper_bound = math.inf                        
        
                        if upper_bound > max_upper_bound:
                                max_upper_bound = upper_bound
                                a = i
        
                self.number_of_selections[st-1][a] += 1               
                self.n += 1              
                
                if a == a_aux:
                        self.epsilon = max(self.epsilon*0.95, 0.1)
                              
                self.actions[st-1] = aa
                
                return a

        # Select one action, used when evaluating
        # st - is the current state        
        # aa - is the set of possible actions
        # for a given state they are always given in the same order
        # returns
        # a - the index to the action in aa
        def selectactiontoexecute(self,st,aa):
                Q_value = -math.inf
                for i in range(len(aa)):
                        if self.Q[st - 1][i] > Q_value:
                                Q_value = self.Q[st - 1][i]
                                a = i                
                return a


        # this function is called after every action
        # ost - original state
        # nst - next state
        # a - the index to the action taken
        # r - reward obtained
        def learn(self,ost,nst,a,r):               
                Q_value = -math.inf
                if len(self.actions[nst-1]) > 0:
                        for i in range(len(self.actions[nst-1])):                                
                                if self.Q[nst - 1][i] > Q_value:
                                        Q_value = self.Q[nst - 1][i]
                                        na = i
                else:
                        na = 0
                        
                self.Q[ost - 1][a] = self.Q[ost - 1][a] + self.learning_rate*(r + self.gamma*self.Q[nst - 1][na] - self.Q[ost - 1][a])

                return