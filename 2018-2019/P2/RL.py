#Grupo tg004: Maria Ines Morais - 83609, Joao Antunes - 87668

# -*- coding: utf-8 -*-
"""
Created on Mon Oct 16 20:31:54 2017

@author: mlopes
"""
import numpy as np
import random

from tempfile import TemporaryFile
outfile = TemporaryFile()
	
class finiteMDP:

    def __init__(self, nS, nA, gamma, P=[], R=[], absorv=[]):
        self.nS = nS                            #numero de estados/numero de linhas
        self.nA = nA                            #numero de acoes/numero de colunas 
        self.gamma = gamma                      
        self.Q = np.zeros((self.nS,self.nA))
        self.P = P
        self.R = R
        self.absorv = absorv
            
    def runPolicy(self, n, x0,  poltype = 'greedy', polpar=[]):
        #nao alterar
        traj = np.zeros((n,4))
        x = x0
        J = 0
        for ii in range(0,n):
            a = self.policy(x,poltype,polpar)
            r = self.R[x,a]
            y = np.nonzero(np.random.multinomial( 1, self.P[x,a,:]))[0][0]
            traj[ii,:] = np.array([x, a, y, r])
            J = J + r * self.gamma**ii
            if self.absorv[x]:
                y = x0
            x = y
        
        return J,traj


    def VI(self):
        #nao alterar
        nQ = np.zeros((self.nS,self.nA))
        while True:
            self.V = np.max(self.Q,axis=1) 
            for a in range(0,self.nA):
                nQ[:,a] = self.R[:,a] + self.gamma * np.dot(self.P[:,a,:],self.V)
            err = np.linalg.norm(self.Q-nQ)
            self.Q = np.copy(nQ)
            if err<1e-7:
                break
            
        #update policy
        self.V = np.max(self.Q,axis=1) 
        #correct for 2 equal actions
        self.Pol = np.argmax(self.Q, axis=1)
                    
        return self.Q,  self.Q2pol(self.Q)

            
    def traces2Q(self, trace):
        self.Q = np.zeros((self.nS,self.nA))
        learning_rate = 0.1
        new_Q = np.zeros((self.nS,self.nA))
        while True:
            for traj in trace:
                new_Q[int(traj[0]),int(traj[1])] = new_Q[int(traj[0]),int(traj[1])] + learning_rate*(traj[3] + self.gamma*max(new_Q[int(traj[2]),:]) - new_Q[int(traj[0]),int(traj[1])])

            learning_rate = max(learning_rate*0.95, 0.02)
            err = np.linalg.norm(self.Q-new_Q)
            self.Q = np.copy(new_Q)            

            if err<1e-2:
                break        
        return self.Q
    
    def policy(self, x, poltype = 'exploration', par = []):
        
        if poltype == 'exploitation':   #politica otima
            par_line = par[x]
            a = np.argmax(par_line)

            
        elif poltype == 'exploration':   #politica aleatoria
            a = random.randint(0, self.nA-1)

                
        return a
    
    def Q2pol(self, Q, eta=5):           
        return np.exp(eta*Q)/np.dot(np.exp(eta*Q),np.array([[1,1],[1,1]]))


            