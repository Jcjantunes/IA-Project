#Grupo tg004: Maria Ines Morais - 83609, Joao Antunes - 87668

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 15 15:51:49 2018

@author: mlopes
"""

from itertools import product

class Node():
    def __init__(self, prob, parents = []):
        self.parents = parents
        self.prob = prob
    
    def computeProb(self, evid):
        p = []
        parents = self.parents
        prob = self.prob
        if (len(parents) == 0):
            p.append(1 - prob[0])
            p.append(prob[0])
        else:
            recursiveParents = parents.copy()
            calculateProb(prob,recursiveParents,evid,p)
        

        return p

def calculateProb(prob,parents,evid,p):
      
    if (len(parents) == 0):
        p.append(1 - prob)
        p.append(prob)
        return p
    
    if(evid[parents[0]]):
        parents.pop(0)
        return calculateProb(prob[1],parents,evid,p)
    else:
        parents.pop(0)
        return calculateProb(prob[0],parents,evid,p)
    

    
class BN():
    def __init__(self, gra, prob):
        self.graph = gra
        self.prob = prob

    def computePostProb(self, evid):
        empty_index_array = []
        p0_array = []
        p1_array = []        
        p0_post = 0
        p1_post = 0
        
        for index in range(len(evid)):
            if(evid[index] == []):
                empty_index_array.append(index)
            
            if(evid[index] == -1):
                switch_index = index
        
        all_combinations_array = list(product([0,1], repeat= len(empty_index_array)))
        
        for combination in all_combinations_array:
            new_evid_p0 = list(evid)
            new_evid_p1 = list(evid)
            combination_index = 0
            for index in empty_index_array:
                new_evid_p0[index] = combination[combination_index]
                new_evid_p1[index] = combination[combination_index]
                combination_index += 1
            new_evid_p0[switch_index] = 0
            p0_array.append(tuple(new_evid_p0))
            
            new_evid_p1[switch_index] = 1
            p1_array.append(tuple(new_evid_p1))
        
        for ev in p0_array:
            p0_post += self.computeJointProb(ev)
            
        for ev in p1_array:
            p1_post += self.computeJointProb(ev)
        
        
        return (p1_post)/(p1_post + p0_post)
        
        
    def computeJointProb(self, evid):
        joint_prob = 1
        node_index = 0
        prob = self.prob
        
        for ev in evid:
            if(ev):
                joint_prob *= prob[node_index].computeProb(evid)[1]
            else:
                joint_prob *= prob[node_index].computeProb(evid)[0]
            node_index += 1
        
        return joint_prob
