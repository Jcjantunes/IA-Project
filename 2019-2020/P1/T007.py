#87668 Joao Antunes Grupo 007
import math
import pickle
import time
from itertools import product

class Position:                           #cada posicao das 113 posicoes do mapa
    def __init__(self,value,transport):
        self.value = value                #numero da posicao (entre 1 a 113)
        self.transport = transport        #tipo de transporte para chegar a esta posicao 

class Detective:                          #posicao atual de cada um dos 3 agentes
    def __init__(self,init):
        self.current_position = Position(init,[])  

class Node:                               #estado do jogo depois de cada transicao dos agentes
    def __init__(self,tickets):
        self.detectives_list = [None,None,None] #lista de agentes no jogo
        self.tickets = tickets #quantidade de bilhetes disponivel
        self.g = 0             #custo
        self.h = 0             #heuristica
        self.parent = None     #Node pai
        self.childs_nodes = [] #Nodes filhos
        self.goal = None       #Destinos dos agentes

def calculate_goal_distance(coords_init, coords_dest):                 #Funcao para calcular a heuristica de cada node
    d = math.pow(coords_dest[0] - coords_init[0], 2) + math.pow(coords_dest[1] - coords_init[1],2)
    return math.sqrt(d)                                                #retorna a distancia euclidiana entre a posicao objetivo e a posicao atual 

class SearchProblem:
    def __init__(self, goal, model, auxheur = []):
        self.goal = goal
        self.model = model
        self.auxheur = auxheur    

    def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf], anyorder = False): #A* search
        open_nodes = []              #lista de nos ainda nao testados (priority queue)                                   
        closed_nodes = []            #lista de nos testados (expandidos)
        
        if anyorder == False:      #Se a ordem dos objetivos nao importar
            current_node = Node(tickets) #Node atual
    
            i=0
            for i in range(len(init)):
                current_node.detectives_list[i] = Detective(init[i])
                current_node.h += calculate_goal_distance(self.auxheur[current_node.detectives_list[i].current_position.value-1], self.auxheur[self.goal[i]-1])
            current_node.goal = self.goal  
            open_nodes.append(current_node)
        else:
            all_goal_combinations = list(product(self.goal, repeat= 3))
            goal_combinations = []
        
            for combination in all_goal_combinations:
                if len(set(combination)) == len(combination):
                    goal_combinations.append(combination)
        
            for goal in goal_combinations:
                node = Node(tickets)
                i=0
                for i in range(len(init)):
                    node.detectives_list[i] = Detective(init[i])
                    node.h += calculate_goal_distance(self.auxheur[node.detectives_list[i].current_position.value-1], self.auxheur[goal[i]-1])
                node.goal = goal
                open_nodes.append(node)            

        if len(init) == 1:  #se for apenas um agente
            while len(open_nodes) > 0:
                current_node = min(open_nodes, key=lambda node: node.g + node.h)

                if current_node.detectives_list[0].current_position.value == current_node.goal[0]: #se o agente ja chegou ao objetivo
                    agent_path = []
                    while current_node.parent:
                        agent_path_aux = [[current_node.detectives_list[0].current_position.transport], [current_node.detectives_list[0].current_position.value]]
                        agent_path.append(agent_path_aux)
                        current_node = current_node.parent

                    agent_path_aux = [current_node.detectives_list[0].current_position.transport, [current_node.detectives_list[0].current_position.value]]
                    agent_path.append(agent_path_aux)
                    return agent_path[::-1]  

                open_nodes.remove(current_node)
                closed_nodes.append(current_node)                
                
                limitexp -= 1
                
                if current_node.detectives_list[0].current_position.transport != []:
                    current_node.tickets[current_node.detectives_list[0].current_position.transport] -= 1        
                
                if current_node.g + 1 <= limitdepth and limitexp > 0:
                    for childs in self.model[current_node.detectives_list[0].current_position.value]:
                        if current_node.tickets[childs[0]] > 0:
                            child_node = Node([current_node.tickets[0],current_node.tickets[1], current_node.tickets[2]])
                            child_node.detectives_list[0] = Detective(childs[1])
                            child_node.detectives_list[0].current_position.transport = childs[0]
                            current_node.childs_nodes.append(child_node)

                for child_node in current_node.childs_nodes:
                    if child_node.detectives_list[0].current_position.value != []:
                        if child_node in closed_nodes:
                            continue
                        if child_node in open_nodes:
                            new_g = current_node.g + 1
                            if new_g < child_node.g:
                                child_node.g = new_g
                                child_node.parent = current_node
                        else:
                            child_node.g = current_node.g + 1
                            child_node.h = calculate_goal_distance(self.auxheur[child_node.detectives_list[0].current_position.value-1], self.auxheur[current_node.goal[0]-1])                            
                            child_node.parent = current_node
                            child_node.goal = current_node.goal
                            open_nodes.append(child_node)        

        else: #se forem 3 agentes  
            while len(open_nodes) > 0:
                current_node = min(open_nodes, key=lambda node: node.g + node.h)
                
                if anyorder == False:      #Se a ordem dos objetivos nao importar
                    if current_node.detectives_list[0].current_position.value == current_node.goal[0] and current_node.detectives_list[1].current_position.value == current_node.goal[1] and current_node.detectives_list[2].current_position.value == current_node.goal[2]:
                        agent_path = []
                        while current_node.parent:
                            agent_path_aux = [[current_node.detectives_list[0].current_position.transport,
                                 current_node.detectives_list[1].current_position.transport, 
                                 current_node.detectives_list[2].current_position.transport], [current_node.detectives_list[0].current_position.value,
                                                                                               current_node.detectives_list[1].current_position.value,
                                                                                               current_node.detectives_list[2].current_position.value]]
                            agent_path.append(agent_path_aux)
                            current_node = current_node.parent
    
                        agent_path_aux = [current_node.detectives_list[0].current_position.transport, [current_node.detectives_list[0].current_position.value,
                                                                                           current_node.detectives_list[1].current_position.value,
                                                                                           current_node.detectives_list[2].current_position.value]]
                        agent_path.append(agent_path_aux)
                        return agent_path[::-1]
                else:
                    if (current_node.detectives_list[0].current_position.value in current_node.goal) and (current_node.detectives_list[1].current_position.value in current_node.goal) and (current_node.detectives_list[2].current_position.value in current_node.goal):
                        agent_path = []
                        while current_node.parent:
                            agent_path_aux = [[current_node.detectives_list[0].current_position.transport,
                                                               current_node.detectives_list[1].current_position.transport, 
                                                 current_node.detectives_list[2].current_position.transport], [current_node.detectives_list[0].current_position.value,
                                                                                                               current_node.detectives_list[1].current_position.value,
                                                                                                               current_node.detectives_list[2].current_position.value]]
                            agent_path.append(agent_path_aux)
                            current_node = current_node.parent
                
                        agent_path_aux = [current_node.detectives_list[0].current_position.transport, [current_node.detectives_list[0].current_position.value,
                                                                                                                       current_node.detectives_list[1].current_position.value,
                                                                                                           current_node.detectives_list[2].current_position.value]]
                        agent_path.append(agent_path_aux)
                        return agent_path[::-1]                    
                                       
                i=0
                for i in range(3):
                    if anyorder == False:
                        while current_node.detectives_list[i].current_position.value == current_node.goal[i]:  
                            if i == 0:
                                detective_index1 = 1
                                detective_index2 = 2
                            elif i == 1:
                                detective_index1 = 0
                                detective_index2 = 2
                            else:
                                detective_index1 = 0
                                detective_index2 = 1                                    
                
                            goal1_flag = 0
                            goal2_flag = 0
                
                            for childs in self.model[current_node.detectives_list[detective_index1].current_position.value]:
                                if childs[1] == current_node.goal[detective_index1]:
                                    goal1_flag = 1              
                
                            for childs in self.model[current_node.detectives_list[detective_index2].current_position.value]:
                                if childs[1] == current_node.goal[detective_index2]:
                                    goal2_flag = 1
                
                            if goal1_flag and goal2_flag:
                                detective1_current_position = current_node.detectives_list[detective_index1].current_position.value
                                detective2_current_position = current_node.detectives_list[detective_index2].current_position.value
                                open_nodes.remove(current_node)
                                closed_nodes.append(current_node)                                                        
                
                                while True:
                                    current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                    if detective1_current_position == current_node.detectives_list[detective_index1].current_position.value and detective2_current_position == current_node.detectives_list[detective_index2].current_position.value:                  
                                        break
                                    else:
                                        open_nodes.remove(current_node)
                                        closed_nodes.append(current_node)                                                   
                
                                while True:
                                    current_positions_value_list = [current_node.detectives_list[0].current_position.value,current_node.detectives_list[1].current_position.value,current_node.detectives_list[2].current_position.value]
                                    if not(len(set(current_positions_value_list)) == len(current_positions_value_list)):
                                        open_nodes.remove(current_node)
                                        closed_nodes.append(current_node)                                
                                        current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                        break_while_flag = 0
                                        current_positions_value_list = [current_node.detectives_list[0].current_position.value,current_node.detectives_list[1].current_position.value,current_node.detectives_list[2].current_position.value]                      
                                    else:
                                        break_while_flag = 1
                                    
                                    if current_node.detectives_list[0].current_position.transport != []:
                                        detectives_list = [current_node.detectives_list[0],current_node.detectives_list[1],current_node.detectives_list[2]]
                                        transports_list = [detectives_list[0].current_position.transport, detectives_list[1].current_position.transport, detectives_list[2].current_position.transport]
                                        while True:
                                            flag0 = 0
                                            flag1 = 0
                                            flag2 = 0
                                            flag3 = 0
                                            flag4 = 0
                    
                                            if not(len(set(transports_list)) == len(transports_list)):
                                                if len(set(transports_list)) == 1:
                                                    if current_node.tickets[detectives_list[0].current_position.transport] - 3 <= 0:
                                                        open_nodes.remove(current_node)
                                                        closed_nodes.append(current_node)                                        
                                                        current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                                        detectives_list = [current_node.detectives_list[0],current_node.detectives_list[1],current_node.detectives_list[2]]
                                                        transports_list = [detectives_list[0].current_position.transport, detectives_list[1].current_position.transport, detectives_list[2].current_position.transport]                    
                                                    else:
                                                        flag0 = 1
                    
                                                if len(set(transports_list)) == 2:
                                                    compare_detectives = []
                                                    for detective_1 in detectives_list:
                                                        for detective_2 in detectives_list:
                                                            if detective_1 != detective_2:
                                                                if detective_1.current_position.transport == detective_2.current_position.transport:
                                                                    duplicate_transport = detective_1.current_position.transport
                                                                    compare_detectives.append(detective_1)
                                                                    compare_detectives.append(detective_2)
                                                                    break_flag = 1
                                                                    break
                                                                else:
                                                                    break_flag = 0
                                                        if break_flag == 1:
                                                            break
                    
                                                    for detective_3 in detectives_list:
                                                        if detective_3 not in compare_detectives:
                                                            not_duplicated_transport = detective_3.current_position.transport
                    
                                                    if current_node.tickets[duplicate_transport] - 2 <= 0 or current_node.tickets[not_duplicated_transport] - 1 <= 0:
                                                        open_nodes.remove(current_node)
                                                        closed_nodes.append(current_node)                                        
                                                        current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                                        detectives_list = [current_node.detectives_list[0],current_node.detectives_list[1],current_node.detectives_list[2]]
                                                        transports_list = [detectives_list[0].current_position.transport, detectives_list[1].current_position.transport, detectives_list[2].current_position.transport]                    
                                                    else:
                                                        flag1 = 1
                    
                                            else:
                                                j = 0
                                                for j in range(3):
                                                    if current_node.tickets[detectives_list[j].current_position.transport] - 1 <= 0:
                                                        open_nodes.remove(current_node)
                                                        closed_nodes.append(current_node)                                    
                                                        current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                                        detectives_list = [current_node.detectives_list[0],current_node.detectives_list[1],current_node.detectives_list[2]]
                                                        transports_list = [detectives_list[0].current_position.transport, detectives_list[1].current_position.transport, detectives_list[2].current_position.transport]                  
                                                    
                                                    else:
                                                        if j == 0:
                                                            flag2 = 1
                                                        elif j == 1:
                                                            flag3 = 1
                                                        else:
                                                            flag4 = 1
                                                        
                                            if flag0 == 1 or flag1 == 1 or (flag2 == 1 and flag3 == 1 and flag4 == 1):
                                                break_while_flag2 = 1
                                                break
                                            else:
                                                break_while_flag2 = 0
                                        
                                    if break_while_flag == 1 and break_while_flag2 == 1:
                                        break
                            else:
                                break
                    else:
                        while current_node.detectives_list[i].current_position.value in current_node.goal:  
                            if i == 0:
                                detective_index1 = 1
                                detective_index2 = 2
                            elif i == 1:
                                detective_index1 = 0
                                detective_index2 = 2
                            else:
                                detective_index1 = 0
                                detective_index2 = 1                                    
                
                            goal1_flag = 0
                            goal2_flag = 0
                
                            for childs in self.model[current_node.detectives_list[detective_index1].current_position.value]:
                                if childs[1] in current_node.goal:
                                    goal1_flag = 1              
                
                            for childs in self.model[current_node.detectives_list[detective_index2].current_position.value]:
                                if childs[1] in current_node.goal:
                                    goal2_flag = 1
                
                            if goal1_flag and goal2_flag:
                                detective1_current_position = current_node.detectives_list[detective_index1].current_position.value
                                detective2_current_position = current_node.detectives_list[detective_index2].current_position.value
                                open_nodes.remove(current_node)
                                closed_nodes.append(current_node)                                                        
                
                                while True:
                                    current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                    if detective1_current_position == current_node.detectives_list[detective_index1].current_position.value and detective2_current_position == current_node.detectives_list[detective_index2].current_position.value:                  
                                        break
                                    else:
                                        open_nodes.remove(current_node)
                                        closed_nodes.append(current_node)                                                   
                
                                while True:
                                    current_positions_value_list = [current_node.detectives_list[0].current_position.value,current_node.detectives_list[1].current_position.value,current_node.detectives_list[2].current_position.value]
                                    if not(len(set(current_positions_value_list)) == len(current_positions_value_list)):
                                        open_nodes.remove(current_node)
                                        closed_nodes.append(current_node)                                
                                        current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                        break_while_flag = 0
                                        current_positions_value_list = [current_node.detectives_list[0].current_position.value,current_node.detectives_list[1].current_position.value,current_node.detectives_list[2].current_position.value]                      
                                    else:
                                        break_while_flag = 1
                                    
                                    if current_node.detectives_list[0].current_position.transport != []:
                                        detectives_list = [current_node.detectives_list[0],current_node.detectives_list[1],current_node.detectives_list[2]]
                                        transports_list = [detectives_list[0].current_position.transport, detectives_list[1].current_position.transport, detectives_list[2].current_position.transport]
                                        while True:
                                            flag0 = 0
                                            flag1 = 0
                                            flag2 = 0
                                            flag3 = 0
                                            flag4 = 0
                    
                                            if not(len(set(transports_list)) == len(transports_list)):
                                                if len(set(transports_list)) == 1:
                                                    if current_node.tickets[detectives_list[0].current_position.transport] - 3 <= 0:
                                                        open_nodes.remove(current_node)
                                                        closed_nodes.append(current_node)                                        
                                                        current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                                        detectives_list = [current_node.detectives_list[0],current_node.detectives_list[1],current_node.detectives_list[2]]
                                                        transports_list = [detectives_list[0].current_position.transport, detectives_list[1].current_position.transport, detectives_list[2].current_position.transport]                    
                                                    else:
                                                        flag0 = 1
                    
                                                if len(set(transports_list)) == 2:
                                                    compare_detectives = []
                                                    for detective_1 in detectives_list:
                                                        for detective_2 in detectives_list:
                                                            if detective_1 != detective_2:
                                                                if detective_1.current_position.transport == detective_2.current_position.transport:
                                                                    duplicate_transport = detective_1.current_position.transport
                                                                    compare_detectives.append(detective_1)
                                                                    compare_detectives.append(detective_2)
                                                                    break_flag = 1
                                                                    break
                                                                else:
                                                                    break_flag = 0
                                                        if break_flag == 1:
                                                            break
                    
                                                    for detective_3 in detectives_list:
                                                        if detective_3 not in compare_detectives:
                                                            not_duplicated_transport = detective_3.current_position.transport
                    
                                                    if current_node.tickets[duplicate_transport] - 2 <= 0 or current_node.tickets[not_duplicated_transport] - 1 <= 0:
                                                        open_nodes.remove(current_node)
                                                        closed_nodes.append(current_node)                                        
                                                        current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                                        detectives_list = [current_node.detectives_list[0],current_node.detectives_list[1],current_node.detectives_list[2]]
                                                        transports_list = [detectives_list[0].current_position.transport, detectives_list[1].current_position.transport, detectives_list[2].current_position.transport]                    
                                                    else:
                                                        flag1 = 1
                    
                                            else:
                                                j = 0
                                                for j in range(3):
                                                    if current_node.tickets[detectives_list[j].current_position.transport] - 1 <= 0:
                                                        open_nodes.remove(current_node)
                                                        closed_nodes.append(current_node)                                    
                                                        current_node = min(open_nodes, key=lambda node: node.g + node.h)
                                                        detectives_list = [current_node.detectives_list[0],current_node.detectives_list[1],current_node.detectives_list[2]]
                                                        transports_list = [detectives_list[0].current_position.transport, detectives_list[1].current_position.transport, detectives_list[2].current_position.transport]                  
                                                    
                                                    else:
                                                        if j == 0:
                                                            flag2 = 1
                                                        elif j == 1:
                                                            flag3 = 1
                                                        else:
                                                            flag4 = 1
                                                        
                                            if flag0 == 1 or flag1 == 1 or (flag2 == 1 and flag3 == 1 and flag4 == 1):
                                                break_while_flag2 = 1
                                                break
                                            else:
                                                break_while_flag2 = 0
                                        
                                    if break_while_flag == 1 and break_while_flag2 == 1:
                                        break
                            else:
                                break                                        
                    
                open_nodes.remove(current_node)
                closed_nodes.append(current_node)       
     
                limitexp -= 1
     
                if current_node.detectives_list[0].current_position.transport != []:
                    current_node.tickets[current_node.detectives_list[0].current_position.transport] -= 1
                    current_node.tickets[current_node.detectives_list[1].current_position.transport] -= 1
                    current_node.tickets[current_node.detectives_list[2].current_position.transport] -= 1
                
                if current_node.g + 1 <= limitdepth and limitexp > 0:
                    for childs0 in self.model[current_node.detectives_list[0].current_position.value]:
                        for childs1 in self.model[current_node.detectives_list[1].current_position.value]:
                            for childs2 in self.model[current_node.detectives_list[2].current_position.value]:
                                positions_list = [childs0[1],childs1[1],childs2[1]]
                                if len(set(positions_list)) == len(positions_list):
                                    transports_list = [childs0[0],childs1[0],childs2[0]]
                                    if not(len(set(transports_list)) == len(transports_list)):
                                        append_child_flag0 = 0
                                        append_child_flag1 = 0
                                        append_child_flag2 = 0
                                        append_child_flag3 = 0
                                        append_child_flag4 = 0
                                        
                                        if len(set(transports_list)) == 1:
                                            if current_node.tickets[childs0[0]] - 3 > 0:
                                                append_child_flag0 = 1
                                            else:
                                                append_child_flag0 = 0
    
                                        if len(set(transports_list)) == 2:
                                            i = 0
                                            j = 0 
                                            for i in range(len(transports_list)):
                                                for j in range(len(transports_list)):
                                                    if i != j:
                                                        if transports_list[i] == transports_list[j]:
                                                            duplicate_transport = transports_list[i]
                                                            break_flag = 1
                                                            break
                                                        else:
                                                            break_flag = 0
                                                if break_flag == 1:
                                                    break
    
                                            for transport in transports_list:
                                                if transport != duplicate_transport:
                                                    not_duplicated_transport = transport
                                                    break
    
                                            if current_node.tickets[duplicate_transport] - 2 > 0 and current_node.tickets[not_duplicated_transport] - 1 > 0:
                                                append_child_flag1 = 1
                                            else:
                                                append_child_flag1 = 0
                                    else:
                                        if current_node.tickets[childs0[0]] - 1 > 0:
                                            append_child_flag2 = 1
                                        else:
                                            append_child_flag2 = 0
    
                                        if current_node.tickets[childs1[0]] - 1 > 0:
                                            append_child_flag3 = 1
                                        else:
                                            append_child_flag3 = 0
    
                                        if current_node.tickets[childs2[0]] - 1 > 0:
                                            append_child_flag4 = 1
                                        else:
                                            append_child_flag4 = 0
    
                                    if append_child_flag0 == 1 or append_child_flag1 == 1 or (append_child_flag2 == 1 and append_child_flag3 == 1 and append_child_flag4 == 1):
                                        child_node = Node([current_node.tickets[0],current_node.tickets[1], current_node.tickets[2]])
                                        child_node.detectives_list[0] = Detective(childs0[1])
                                        child_node.detectives_list[0].current_position.transport = childs0[0]
    
                                        child_node.detectives_list[1] = Detective(childs1[1])
                                        child_node.detectives_list[1].current_position.transport = childs1[0]
    
                                        child_node.detectives_list[2] = Detective(childs2[1])
                                        child_node.detectives_list[2].current_position.transport = childs2[0]              
    
                                        current_node.childs_nodes.append(child_node)                    
                            
                for child_node in current_node.childs_nodes:
                    if child_node.detectives_list[0].current_position.value != []:
                        if child_node in closed_nodes:
                            continue
                        if child_node in open_nodes:
                            new_g = current_node.g + 1
                            if new_g < child_node.g:
                                child_node.g = new_g
                                child_node.parent = current_node
                        else:
                            child_node.g = current_node.g + 1
                            i = 0
                            for i in range(3):
                                child_node.h += calculate_goal_distance(self.auxheur[child_node.detectives_list[i].current_position.value-1], self.auxheur[current_node.goal[i]-1])
            
                            child_node.parent = current_node
                            child_node.goal = current_node.goal
                            open_nodes.append(child_node)                    