from utils.graph import Graph
from simulation.utils.sim_nodes import BlockNode, Workspace, PublicPlace

TEST_CITY_1 = Graph()

block_1 = BlockNode(100, (0,0))
block_2 = BlockNode(100, (0,1))
block_3 = BlockNode(100, (1,0))
block_4 = BlockNode(100, (1,1))

workspace_1 = Workspace(10, 0)
workspace_2 = Workspace(10, 1)

public_1 = PublicPlace(5, 2)
public_2 = PublicPlace(5, 3)

TEST_CITY_1.add_node(block_1)
TEST_CITY_1.add_node(block_2)
TEST_CITY_1.add_node(block_3)
TEST_CITY_1.add_node(block_4)
TEST_CITY_1.add_node(workspace_1)
TEST_CITY_1.add_node(workspace_2)
TEST_CITY_1.add_node(public_1)
TEST_CITY_1.add_node(public_2)

cost_edge = 1
for i in range(2):
    for j in range(2):
        if i < 1:
            TEST_CITY_1.add_edge((i, j),(i+1, j), cost_edge) # Conectar nodos en la misma columna
        if j < 1:
            TEST_CITY_1.add_edge((i, j), (i, j+1), cost_edge) # Conectar nodos en la misma fila
            
        cost_edge+=1

TEST_CITY_1.add_edge((0, 0), 0, 0)
TEST_CITY_1.add_edge((1, 0), 1, 0)
TEST_CITY_1.add_edge((1, 1), 2, 0)
TEST_CITY_1.add_edge((1, 0), 3, 0)


