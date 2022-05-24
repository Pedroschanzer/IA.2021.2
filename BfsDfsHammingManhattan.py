from collections import deque
from queue import PriorityQueue
import time

#=============================================================================
#TRABALHO 1 - IA =============================================================
#=============================================================================
# by: Pedro Schanzer, Rodrigo N. Wuerdig, Vitor Hugo F. Maciel
#=============================================================================

class Nodo:
    """
    Implemente a classe Nodo com os atributos descritos na funcao init
    """
    def __init__(self, estado=None, pai=None, acao=None, custo=None):
        """
        Inicializa o nodo com os atributos recebidos
        :param estado:str, representacao do estado do 8-puzzle
        :param pai:Nodo, referencia ao nodo pai, (None no caso do nó raiz)
        :param acao:str, acao a partir do pai que leva a este nodo (None no caso do nó raiz)
        :param custo:int, custo do caminho da raiz até este nó
        """
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo

    def __eq__(self, other):
        return self.estado == other.estado

    def __ne__(self, other):
        return self.estado != other.estado

    def __repr__(self):
        return self.estado

    def __str__(self):
        return self.estado

    def __lt__(self, other):
        return self.estado < other.estado

    def __hash__(self):
        return hash(self.estado)

    def root_path(self):
        node = self
        path = []

        
        while node.pai:
            path.insert(0, node.acao)
            node = node.pai
        return path


def swap(c, i, j):
    c = list(c)
    c[i], c[j] = c[j], c[i]
    return ''.join(c)


def sucessor(estado):
    """
    Recebe um estado (string) e retorna uma lista de tuplas (ação,estado atingido)
    para cada ação possível no estado recebido.
    Tanto a ação quanto o estado atingido são strings também.
    :param estado:
    :return:
    """
    left_boundary = [0,3,6]
    right_boundary = [2,5,8]
    upper_boundary = [0,1,2]
    bottom_boundary = [6,7,8]

    tuple_list = []
    if(estado.find("_") not in left_boundary):
        new_state = swap(estado, estado.find("_"), estado.find("_")-1)
        tuple_list.append(("esquerda",new_state))
    if(estado.find("_") not in right_boundary):
        new_state = swap(estado, estado.find("_"), estado.find("_")+1)
        tuple_list.append(("direita",new_state))
    if(estado.find("_") not in upper_boundary):
        new_state = swap(estado, estado.find("_"), estado.find("_")-3)
        tuple_list.append(("acima",new_state))
    if(estado.find("_") not in bottom_boundary):
        new_state = swap(estado, estado.find("_"), estado.find("_")+3)
        tuple_list.append(("abaixo",new_state))
    
    return tuple_list


def expande(nodo):
    """
    Recebe um nodo (objeto da classe Nodo) e retorna um iterable de nodos.
    Cada nodo do iterable é contém um estado sucessor do nó recebido.
    :param nodo: objeto da classe Nodo
    :return:
    """
    succeeding_l = []
    for _n in sucessor(nodo.estado):
        node = Nodo(_n[1], nodo, _n[0], nodo.custo + 1)
        succeeding_l.append(node)
    return succeeding_l


def bfs(estado):
    """
    Recebe um estado (string), executa a busca em LARGURA e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    #============================================================
    boundary = deque([Nodo(estado=estado, custo=0)])
    explored = set()
    counter=0
    start = time.time()
    #============================================================
    while True:
        if not boundary:
            return None
        current_state = boundary.popleft()
        if str(current_state.estado) == "12345678_":
            end = time.time()
            print(f'[bfs]    Nos expandidos:{counter} time:{end-start} cost:{current_state.custo}')
            return current_state.root_path()
        elif current_state not in explored:
            explored.add(current_state)
            counter+=1
            for _child in expande(current_state):
                boundary.append(_child)


def dfs(estado):
    """
    Recebe um estado (string), executa a busca em PROFUNDIDADE e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    #============================================================
    explored = set()
    boundary = [Nodo(estado=estado, custo=0)]
    counter = 0
    start=time.time()
    #============================================================
    current_state=boundary[0]
    while True:
        if not boundary: return None
        current_state = boundary.pop()
        if current_state.estado == "12345678_":
            end = time.time()
            print(f'[dfs]    Nos expandidos:{counter} time:{end-start} cost:{current_state.custo}')
            return current_state.root_path()
        elif current_state not in explored:
            explored.add(current_state)
            counter+=1
            for _child in expande(current_state): #iterate through succeeding states and append them to the boundary
                boundary.append(_child)


def generate_h_hamming(estado):
    h_hamming = 0
    for _iter in range(0, len(estado)):
        _iter_state = estado[_iter]
        if _iter_state == "_": pass
        elif _iter != int(_iter_state) + 1: h_hamming += 1
    return h_hamming


class priority_queue(PriorityQueue):
    def __bool__(self):
        return True if self.qsize() > 0 else False


def astar_hamming(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Hamming e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    #============================================================
    counter=0
    boundary = priority_queue()
    root = Nodo(estado=estado, custo=0)
    boundary.put((root.custo, root))
    explored = set()
    start=time.time()
    #============================================================
    while boundary:
        current_node = boundary.get()[1]
        if str(current_node.estado) == "12345678_": 
            end=time.time()
            print(f'[Astar Hamming]    Nos expandidos:{counter} time:{end-start} cost: {current_node.custo}')
            return current_node.root_path()
        if current_node not in explored:
            explored.add(current_node)
            counter+=1
            for _child in expande(current_node): #iterate through succeeding states and append them to the boundary
                boundary.put((_child.custo + generate_h_hamming(_child.estado), _child))
    return None

def manhattan_distance(a, b):
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def generate_h_manhattan(estado):
    h_manhattan = 0
    for _iter in range(0, len(estado)):
        state = estado[_iter]
        if state == "_": pass
        elif _iter != int(state) + 1:
            current = [_iter / 3,_iter % 3]
            correct = [int(state) / 3,int(state) % 3]
            h_manhattan += manhattan_distance(current,correct)
    return h_manhattan


def astar_manhattan(estado):
    """
    Recebe um estado (string), executa a busca A* com h(n) = soma das distâncias de Manhattan e
    retorna uma lista de ações que leva do
    estado recebido até o objetivo ("12345678_").
    Caso não haja solução a partir do estado recebido, retorna None
    :param estado: str
    :return:
    """
    #============================================================
    root = Nodo(estado=estado, custo=0)
    boundary = priority_queue()
    explored = set()
    boundary.put((root.custo, root))
    counter=0
    start=time.time()
    #============================================================
    while boundary:
        current_node = boundary.get()[1]
        if str(current_node.estado) == "12345678_": 
            end=time.time()
            print(f'[Astar Manhattan]    Nos expandidos:{counter} time:{end-start} cost:{current_node.custo}')
            return current_node.root_path()
        if current_node not in explored:
            children = expande(current_node)
            explored.add(current_node)
            counter+=1
            for _child in children: #iterate through succeeding states and append them to the boundary
                boundary.put((_child.custo + generate_h_manhattan(_child.estado), _child))
    return None