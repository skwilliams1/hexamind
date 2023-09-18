import networkx as nx
import random
import math

# Creating Graph 
def create_graph():
    Graph = nx.Graph()
    Graph.add_nodes_from(range(1,7))
    
    return Graph

AI_Graph = create_graph()
User_Graph = create_graph()

# Function to display the graph 
def display_graph(Graph):
    print("Current graph:")
    print(Graph.edges())
   

# calculating hueristic value of board 
def scoring_hueristic(Graph):

    score = 0
    open_edges = nx.edges(Graph)
    open_edges_list = list(open_edges)

    for open_edge in open_edges_list:

        v1_neighbors = list(nx.neighbors(Graph, open_edge[0]))
        v2_neighbors = list(nx.neighbors(Graph, open_edge[1]))

        print(v1_neighbors, v2_neighbors)

        # checking if vertexes share a neigbour thus existing in an open triangle
        shared = any(neighbour in v1_neighbors for neighbour in v2_neighbors)

        if shared == True:
            score = score - 10000

        # using the negative of the sum of the neighbour of each node because less neighbours among both nodes = better option
        score = score  - (len(v1_neighbors) + len(v2_neighbors))

        
    return score


def is_terminal(Graph, maximizingPlayer):

    return lost(Graph, maximizingPlayer) or nx.number_of_edges(Graph) == 15


def minimax(Graph, depth, maximizingPlayer):

    terminal = is_terminal(Graph, maximizingPlayer)

    if depth == 0 or terminal:
        # if move will cause end to game and is AI 
        if terminal: 
            if maximizingPlayer:
                return [1000000000000]
            elif not maximizingPlayer:
                return [-10000000000]
            else:
                return 0
        else:
            return [scoring_hueristic(Graph)]

    if maximizingPlayer:
        value = -math.inf
        open_edges = nx.non_edges(Graph)
        open_edges_list = list(open_edges)
        best_edge = random.choice(open_edges_list)
        for  open_edge in open_edges_list:
            graph_copy = Graph.copy(as_view = False)
            AI_graph_copy = AI_Graph.copy(as_view = False)
            make_move(True, open_edge[0], open_edge[1], graph_copy, AI_graph_copy )
            new_score = minimax(graph_copy, depth -1, False)[0]
            if new_score > value:
                value = new_score 
                best_edge = open_edge
            
            return [new_score, best_edge]
    else:
        value = math.inf
        open_edges = nx.non_edges(Graph)
        open_edges_list = list(open_edges)
        best_edge = random.choice(open_edges_list)
        for  open_edge in open_edges_list:
            graph_copy = Graph.copy(as_view = False)
            user_graph_copy = Graph.copy(as_view = False)
            make_move(False, open_edge[0], open_edge[1], graph_copy, user_graph_copy)
            new_score = minimax(graph_copy, depth -1, True)[0]
            if new_score < value:
                value = new_score 
                best_edge = open_edge
            
            return  [new_score, best_edge]




# Function to make a move
def make_move(AI, v1, v2, Graph, copy_player_graph = None):
    
    if copy_player_graph:
        copy_player_graph.add_edge(v1, v2)
        Graph.add_edge(v1, v2)
    else:
        # add vertex to common graph and respective player graph
        if AI == False:
            Graph.add_edge(v1, v2)
            User_Graph.add_edge(v1,v2)
        else:
            Graph.add_edge(v1, v2, linestyle='--')
            AI_Graph.add_edge(v1,v2)


# check if move is valid
def is_valid_move(v1, v2, Graph):

    if v1 < 1 or v1 > 6 or v2 < 1 or v2 > 6 or Graph.has_edge(v1, v2):
        print("Invalid Move!")
        return False
    else:
        return True


# prompt user for move and check if valid
def get_moves(Graph):
    
    while True:
        v1 = int(input("Enter the first vertex: "))
        v2 = int(input("Enter the second vertex: "))

        if is_valid_move(v1, v2, Graph):
            break 
        else:
            continue
    
    return (v1, v2)


# check if player has created a triangle 
def lost(Graph, player, AI_graph_copy = None, User_graph_copy = None):
  
    # if Graph.is_empty:
    #     return False
    # player = true = AI = weight = 2
    # player = false = user = weight = 1
    
    if AI_graph_copy or User_graph_copy:
        if AI_graph_copy:
            AI_triangles = nx.triangles(AI_graph_copy)
            if all(value == 0 for value in AI_triangles.values()):
                return False 
        else:
            user_triangles = nx.triangles(User_graph_copy)
            if all(value == 0 for value in user_triangles.values()):
                return False 
    
    else:
        if player:
            AI_triangles = nx.triangles(AI_Graph)
            if all(value == 0 for value in AI_triangles.values()):
                return False 
        else:
            user_triangles = nx.triangles(User_Graph)
            if all(value == 0 for value in user_triangles.values()):
                return False 
    
    return True


if __name__ == '__main__':

    print("Hexagon Game!")

    Graph = create_graph()
    
    user = int(input("Enter player number (1 or 2): "))
    
    # getting AI player number
    if user == 1:
        AI = 2
    else: 
        AI = 1
    
    player = 1
    while True:
        
        # user
        if player == user:

            v1, v2 = get_moves(Graph)

            make_move(False, v1, v2, Graph)
             # displaying result of move by player
            display_graph(Graph)  
            
            # check if move created triangle 
            if lost(Graph, False):
                print(f"Player {player} lost the game")
                break

            # updating player value
            if player == 1:
                player += 1
            else:
                player -= 1
            
     
       
        # AI 
        if player == AI:

            # Getting AI move from minimax function
            score, edge = minimax(Graph, 15, True)
            v1 = edge[0]
            v2 = edge[1]
            make_move (True, v1, v2, Graph)

             # displaying result of move by player
            display_graph(Graph)  

            # check if move created triangle
            if lost(Graph, True):
                print(f"Player {player} lost the game")
                break 

            # updating player value
            if player == 1:
                player += 1
            else:
                player -= 1
            
        
       
        # check if all edges are connected without creating triangle
        if nx.number_of_edges(Graph) == 15:
            
            print("Game ends in a tie!")
            break

    print("Thanks for playing!")
