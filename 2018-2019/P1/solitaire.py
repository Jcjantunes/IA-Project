#Grupo tg004: Maria Ines Morais n 83609, Joao Antunes n 87668 

from search import *
import copy

# TAI content
def c_peg ():
    return "O"
def c_empty ():
    return "_"
def c_blocked ():
    return "X"
def is_empty (e):
    return e == c_empty()
def is_peg (e):
    return e == c_peg()
def is_blocked (e):
    return e == c_blocked()

# TAI pos
# Tuplo (l, c)
def make_pos (l, c):
    return (l, c)
def pos_l (pos):
    return pos[0]
def pos_c (pos):
    return pos[1] 

# TAI move
# Lista [p_initial, p_final]
def make_move (i, f):
    return [i, f]
def move_initial (move):
    return move[0]
def move_final (move):
    return move[1]



# TAI board
def board_moves(board):   
    """recebe um tabuleiro (listas de listas) e devolve uma lista com todos os movimentos possiveis com o estado atual do tabuleiro"""
    
    movesLst = []
    out_of_bounds_lin = len(board) - 2                                                             # n linhas - 2 
    out_of_bounds_col = len(board[0]) - 2                                                          # n colunas - 2
    
    for i in range(len(board)):                                                                    
        lines = board[i]
        for j in range(len(lines)):                                                                               
            if(is_peg(lines[j])):                                                                  #verifica se a posicao atual e uma peca
                if(j > 1 and is_empty(lines[j-2]) and is_peg(lines[j-1])):                         #verifica movimentos possiveis na horizontal para a esquerda
                    movesLst.append(make_move(make_pos(i,j),make_pos(i,j-2)))           
                
                if(j < out_of_bounds_col and is_empty(lines[j+2]) and is_peg(lines[j+1])):         #verifica movimentos possiveis na horizontal para a direita
                    movesLst.append(make_move(make_pos(i,j),make_pos(i,j+2)))
                
                if(i > 1 and is_empty(board[i-2][j]) and is_peg(board[i-1][j])):                   #verifica movimentos possiveis na vertical para cima
                    movesLst.append(make_move(make_pos(i,j),make_pos(i-2,j)))   
                
                if(i < out_of_bounds_lin and is_empty(board[i+2][j]) and is_peg(board[i+1][j])):   #verifica movimentos possiveis na vertical para baixo
                    movesLst.append(make_move(make_pos(i,j),make_pos(i+2,j)))              

    return movesLst



def board_perform_move(board,move): 
    """move a peca da posicao inicial para a posicao destino removendo a peca que se encontrava entre estas duas posicoes"""
    
    boardAux = copy.deepcopy(board)                                                             
    boardAux[pos_l(move_initial(move))][pos_c(move_initial(move))] = c_empty()                   #posicao inicial fica vazia 
    boardAux[pos_l(move_final(move))][pos_c(move_final(move))] = c_peg()                         #posicao final fica com uma peca
    
    if(pos_l(move_initial(move)) == pos_l(move_final(move))):                                    
        if(pos_c(move_final(move)) < pos_c(move_initial(move))):                                 #caso: peca movida horizontalmente para a esquerda
            boardAux[pos_l(move_final(move))][pos_c(move_final(move))+1] = c_empty()               
        
        else:
            boardAux[pos_l(move_final(move))][pos_c(move_final(move))-1] = c_empty()             #caso: peca movida horizontalmente para a direita      
    
    else:
        if(pos_l(move_final(move)) < pos_l(move_initial(move))):                                 #caso: peca movida horizontalmente para cima
            boardAux[pos_l(move_final(move))+1][pos_c(move_final(move))] = c_empty()              
        else:
            boardAux[pos_l(move_final(move))-1][pos_c(move_final(move))] = c_empty()             #caso: peca movida horizontalmente para baixo
    
    return boardAux


def is_goal_test(board):
    """recebe um tabuleiro e verifica se o tabuleiro e um tabuleiro de estado objetivo ou nao, ou seja,
    conta o numero de pecas do tabuleiro dado se o numero de pecas for maior que 1 retorna false"""
    peg_count = 0
    for i in range(len(board)):
        lines = board[i]
        for j in range(len(lines)):
            if(is_peg(lines[j])):
                peg_count += 1
            if(peg_count > 1):
                return False
    return True


def calculate_heuristic(board):
    """recebe um tabuleiro e devolve a soma do numero de pecas mais o numero de pecas nao moviveis"""  
    peg_count = 0
    not_movable_peg_count = 0
    
    out_of_bounds_lin = len(board) - 2                          # n linhas - 2 
    out_of_bounds_col = len(board[0]) - 2                       # n colunas - 2                        
    
    for i in range(len(board)):                                 
        lines = board[i]
        for j in range(len(lines)):                            
            if(is_peg(lines[j])):
                peg_count += 1                                  #incrementa contador de pecas
                                                                                                            #verificar pecas nao moviveis
                if not ((j > 1 and is_empty(lines[j-2]) and is_peg(lines[j-1])) or                        #nao e possivel mover para a esquerda   
                        (j < out_of_bounds_col and is_empty(lines[j+2]) and is_peg(lines[j+1])) or        #nao e possivel mover para a direita
                        (i < out_of_bounds_lin and is_empty(board[i+2][j]) and is_peg(board[i+1][j])) or    #nao e possivel mover para baixo
                        (i > 1 and is_empty(board[i-2][j]) and is_peg(board[i-1][j]))):                     #nao e possivel mover para cima
                    not_movable_peg_count += 1                                                              #incrementa contador de pecas nao moviveis
                    
    
    return peg_count + not_movable_peg_count



def calculate_peg_count(board):            
    """recebe um tabuleiro e devolve o numero de pecas desse tabuleiro"""
    peg_count = 0
    for i in range(len(board)):
        lines = board[i]
        for j in range(len(lines)):
            if(is_peg(lines[j])):
                peg_count += 1    
    return peg_count



# TAI Sol_state
class sol_state:
    __slots__ = ["board","peg_count"]
    def __init__(self, board):
        self.board = board                                      
        self.peg_count = calculate_peg_count(board)
        
    def __lt__(self, sol_state):                                 
        return sol_state.peg_count < self.peg_count        
    
    


#TAI Problem
class solitaire(Problem):
    """Modela o problema Solitaire como um problema de satisfacao. 
       A solucao nao pode ter mais do que uma peca no tabuleiro."""     
    
    __slots__ = ['initial']
    
    def __init__(self, board):
        """ especifica estado inicial"""
        self.initial = sol_state(board)
    
    def actions(self, state):
        """retorna as accoes possiveis de executar num dado estado"""
        return board_moves(state.board)

    def result(self, state, action):
        """retorna o estado resultante de executar a dada accao ao dado estado"""        
        return sol_state(board_perform_move(state.board,action))
        
    def goal_test(self, state):
        """recebe um estado e retorna true se o dado estado for um estado objectivo."""
        return is_goal_test(state.board)
    
    def path_cost(self, c, state1, action, state2):
        """retorna o custo da transicao do estado 1 para o estado 2 via a accao aplicada """       
        return c+1
        
    def h(self, node):
        return calculate_heuristic(node.state.board)