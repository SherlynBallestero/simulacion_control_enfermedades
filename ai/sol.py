import heapq
import math
import copy

class Puzzle:
    def __init__(self, board, goal, heuristic):
        self.board = board
        self.goal = goal
        self.heuristic = heuristic

    def __lt__(self, other): 
        
        return self.heuristic < other.heuristic
def find_element(board, element):
    # Iterate over the rows of the board
    for i in range(len(board)):
        # Iterate over the columns of the board
        for j in range(len(board[0])):
            # If the current element is the element we are looking for, return its position
            if board[i][j] == element:
                return (i, j)

    # If the element is not found, return None
    return None 
def manhattan_plus_linear_conflict(board,goal):
    # Calculate the manhattan distance
    manhattan_distance = 0
    linear_conflict=0
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != 0:
                goal_i,goal_j= find_element(goal, board[i][j])
                manhattan_distance += abs(i - goal_i) + abs(j - goal_j)  
                if goal_i!=i or goal_j!=j:
                    linear_conflict=linear_conflict+1
                    
                     
    return manhattan_distance + linear_conflict                   
def get_neighbors(board):
    new_board=copy.deepcopy(board)
    moves=[(0,-1),(-1,0),(1,0),(0,1)]
    answer=[]
    #board=!null 
    row_len=len(board)
    col_len=len(board[0])
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col]==0: 
                for move in moves:                
                    new_board=copy.deepcopy(board)
                    new_row=row+move[0]
                    new_col=col+move[1]
                    if new_row>=0 and new_row<row_len:
                       if new_col>=0 and new_col<col_len:
                            new_board[new_row][new_col]=0
                            new_board[row][col]=board[new_row][new_col]   
                            answer.append(new_board.copy())
                        
    return answer                                                    
def a_start(puzzle:Puzzle):
    if cheking(puzzle.board) is False:
        return -1
    #initialize the open and closed sets
    open_set=[]
    heapq.heappush(open_set,puzzle)
    #nodes visited
    closed_set=[]
    # While the open set is not empty
    while open_set:
    # Get the puzzle with the lowest heuristic value
        current_puzzle = heapq.heappop(open_set)
        
        # If the current puzzle is the goal, return the solution
        if current_puzzle.board == puzzle.goal:
            print(current_puzzle.board)
            #to_do: ver como hago para imprimir todos los cambios 
            return current_puzzle
        closed_set.append(current_puzzle.board)
        # Generate the possible moves
        moves=get_neighbors(current_puzzle.board)
        for move in moves:
                heuristic=manhattan_plus_linear_conflict(move,puzzle.goal)
             # Create a new puzzle with the move applied
                new_puzzle = Puzzle(move, puzzle.goal, heuristic)
               
            # If the new puzzle is not in the closed set
                if new_puzzle.board not in closed_set:
                    
                # Add the new puzzle to the open set
                    heapq.heappush(open_set, new_puzzle)
def inversions_count(board_list):
    number_inversions=0
    for element in range(len(board_list)):
        if board_list[element]==0:
            continue
        for pivot in range(element):
            
            if board_list[pivot]>board_list[element]:
                
                number_inversions=number_inversions+1
                
    return number_inversions            
def blank_position(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==0:
                return i                                  
def cheking(board):
    board_list=[]
    goal_list=[]
    for row in board:  
        board_list=board_list+row
    n=len(board[0])
    blank_pos=blank_position(board)
    inversions_number=inversions_count(board_list)
    if n%2 ==0:
        return (n-blank_pos)%2==0 and inversions_number%2!=0
    else:
        return inversions_number%2==0
    
    print(board_list)    
    return(inversions(board_list))    
    
                  
            
                


# tests
#whith one blank
goal0 = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]

#no solution..
start0 = [
    [2, 8, 3],
    [1, 6, 4],
    [7, 0, 5]
]
print("puzzle1")
puzzle1 = Puzzle( start0, goal0,manhattan_plus_linear_conflict(start0, goal0))
solution1 = a_start(puzzle1) 
print(solution1)
#solution expected...
start01=[
    [1, 2, 3],
    [4, 5, 6],
    [7, 0, 8]
]
print("puzzle2")
puzzle2 = Puzzle( start01, goal0,manhattan_plus_linear_conflict(start01, goal0))
solution2 = a_start(puzzle2) 
print(solution2)

start02=[
    [2, 3, 0],
    [1, 6, 5],
    [4, 8, 7]
]
print("puzzle3")
puzzle3 = Puzzle( start02, goal0,manhattan_plus_linear_conflict(start02, goal0))
solution3 = a_start(puzzle3) 
print(solution3)
#2 blanks
goal1 = [
    [0, 2, 3],
    [4, 5, 6],
    [7, 8, 0]
]
#soluction_expected
start10=[
    [0, 3, 2],
    [0, 5, 6],
    [4, 8, 7]
]
print("puzzle4")
puzzle4 = Puzzle( start10, goal1,manhattan_plus_linear_conflict(start10, goal1))
solution4 = a_start(puzzle4) 
print(solution4)


#other dimension...
goal2 = [
    [1, 2, 3,4],
    [5, 6,7,8],
    [9,10,11, 12],
    [13,14,15,0]
]
start20 = [
    [0, 2, 3,4],
    [5, 6,7,8],
    [9,10,11, 1],
    [13,14,15,12]
]
print("puzzle5")
puzzle5 = Puzzle( start20, goal2,manhattan_plus_linear_conflict(start20, goal2))
solution5 = a_start(puzzle5) 
print(solution5)






              
          
        
        
    