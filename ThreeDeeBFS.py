"""Author:Dom Modica
The purpose of this program is to solve the problem described @ http://www.reddit.com/r/dailyprogrammer/comments/2o5tb7/2014123_challenge_191_intermediate_space_probe/
Essentially one is to create a 2D NxN matrix along with various obstacles denoted as gravity wells and asteroids and implement a BFS to find a path from S(start) to E(end)
This instance however solves it for a 3D NxNxN matrix.
"""

import math
import random
import pprint
from copy import copy,deepcopy


class Node: #Allows me to give each node in the NxNxN matrix properties such as value, posistion, and whether or not this particular node has been visited or not.
    def __init__(self, val, pos):
        self.val = val
        self.pos = pos
        self.visited = False
    def __repr__(self):
        return repr(self.pos)
    def __getitem__(self, index):
        return self.pos[index]
        

class Galaxy(): #Creates an instance of NxNxN matrix and populates it with asteroids and gravity wells
    def __init__(self,n,start,end):  # all the properties for the space graph are created her on a per 'instance' basis
        self.n=n
        self.size=n*n*n
        self.asteroidspop= math.floor(self.size*0.10)
        self.gravitywellspop=math.floor(self.size*0.10)
        self.matrix=[[["." for x in range (n)] for x in range(n)]for x in range(n)] #Let it be noted a "." represents a non-obstacle and non start or end node.
        self.start=start
        self.end=end
        self.starta,self.startb,self.startc=self.start[0],self.start[1],self.start[2]


    def createobstacles(self):
        starta,startb,startc=self.start[0],self.start[1],self.start[2]  #Unpack start and end tuples
        enda,endb,endc=self.end[0],self.end[1],self.end[2]
        self.matrix[starta][startb][startc]='S'  #sets start and end points on matrix
        self.matrix[enda][endb][endc]='E'
            
        for item in range(self.asteroidspop):                               #asteroid creation
            x,y,z=random.randint(0,self.n-1),random.randint(0,self.n-1),random.randint(0,self.n-1)
            while self.matrix[x][y][z] in ['A','S','E']:   #after a random coordinate is chosen it makes sure its not already a create obstacle if it is it rerolls that random
                x,y,z=random.randint(0,self.n-1),random.randint(0,self.n-1),random.randint(0,self.n-1)
            self.matrix[x][y][z]='A'
            
        for item in range(self.gravitywellspop): #gravity well creation
            x,y,z=random.randint(0,self.n-1),random.randint(0,self.n-1),random.randint(0,self.n-1) #same logic applies from before
            while self.matrix[x][y][z] in ['A','S','E','G']:
                x,y,z=random.randint(0,self.n-1),random.randint(0,self.n-1),random.randint(0,self.n-1)
            self.matrix[x][y][z]='G'

def custombfs(graph,start):
    
    todo=[[start]]
    if start.val == 'E':  #checks to see if start point is end point
        return [start]
    start.visited=True
    length=len(graph) #needs to be stored to aid in deciphering legal/illegal moves

    moves = [(-1, 0,0), (1,0,0), (0, -1,0), (0, 1,0),(0,0,1),(0,0,-1)]
    while todo:
        path = todo.pop(0) #deques first element in todo list
        node = path[-1]
        pos = node.pos   #gets the posistion for which we will apply all possible legal "moves"

        for move in moves:
            if not (0 <= pos[0] + move[0] < length and 0 <= pos[1] + move[1] < length and 0 <= pos[2]+move[2]<length): #cycles through moves list and decides whether legal or illegal
                continue
            neighbor = graph[pos[0] + move[0]] [pos[1] + move[1]][pos[2]+move[2]]
            if neighbor.val == 'E':
                return path + [neighbor]
            elif neighbor.val == '.' and not neighbor.visited:
                neighbor.visited = True
                todo.append(path+[neighbor])  # creates copy of list
            else:
                pass
    raise Exception('Path not found!')
    
def main():       
    Space=Galaxy(10,(0,0,0),(9,9,9)) #send in size,start,end coordinates (in that order)
    Space.createobstacles()
    tempmaster=deepcopy(Space.matrix) #ran into problems converting the space object to have the node "properties" so I had to make a deep copy of the object and work with that
        
    for q in range(Space.n):
        for r in range(Space.n):
            for z in range(Space.n):
                tempmaster[q][r][z]=Node(tempmaster[q][r][z],(q,r,z)) #converts all coordinates to nodes, is inefficient but works none the less

    solution=custombfs(tempmaster,tempmaster[Space.starta][Space.startb][Space.startc])
    print(solution) #prints solutions. in the even no solution is found custombfs with raise an exception and say path not found


if __name__=="__main__":
    main()
