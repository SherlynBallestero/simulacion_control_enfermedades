# from utils.graph import Graph
from simulation.enviroment.sim_nodes import BlockNode, Workspace, PublicPlace
from simulation.enviroment.map import Terrain
import random

TEST_CITY_1 = Terrain()

for x in range(10):
    for y in range(10):
        TEST_CITY_1.add_block((x, y), 100)
        
cost_edge = 1
for i in range(10):
    for j in range(10):
        if i < 9:
            node1 = TEST_CITY_1[(i,j)]
            node2 = TEST_CITY_1[(i+1, j)]
            TEST_CITY_1.add_edge(node1[0].id, node2[0].id) # Conectar nodos en la misma columna
        if j < 9:
            node1 = TEST_CITY_1[(i,j)]
            node2 = TEST_CITY_1[(i, j+1)]
            TEST_CITY_1.add_edge(node1[0].id, node2[0].id) # Conectar nodos en la misma fila
            
        cost_edge+=1

for _ in range(50):
    house_addr = random.choice(list(TEST_CITY_1.nodes_by_addrs.keys()))
    TEST_CITY_1.add_house(house_addr, random.randint(1, 5))

TEST_CITY_1.add_bus_stop((1,0), 30)
TEST_CITY_1.add_hospital((2,3), 50)
TEST_CITY_1.add_recreational((3,1),20)
TEST_CITY_1.add_work((4,8),10)

TEST_CITY_1.add_bus_stop((0,1), 25) 
TEST_CITY_1.add_hospital((3,2), 40) 
TEST_CITY_1.add_recreational((4,0), 15) 
TEST_CITY_1.add_work((2,4), 12)

TEST_CITY_1.add_bus_stop((1,1), 35) 
TEST_CITY_1.add_hospital((2,2), 55) 
TEST_CITY_1.add_recreational((3,0), 25) 
TEST_CITY_1.add_work((4,9), 15) 

TEST_CITY_1.add_bus_stop((0,2), 20)
TEST_CITY_1.add_hospital((3,3), 45)
TEST_CITY_1.add_recreational((4,1), 10)
TEST_CITY_1.add_work((2,5), 15)


