from __future__ import print_function
#Use priority queues from Python libraries, don't waste time implementing your own
from heapq import *
from math import sqrt
ACTIONS = [(0,-1),(-1,0),(0,1),(1,0)]

class Element:
    def __init__(self, key, value):
        self.key = key
        self.value = value
    def __eq__(self, other):
        return self.key == other.key
		
class Agent:
    def __init__(self, grid, start, goal, type):
        self.grid = grid
        self.previous = {}
        self.explored = []
        self.start = start 
        self.grid.nodes[start].start = True
        self.goal = goal
        self.grid.nodes[goal].goal = True
        self.new_plan(type)
    def new_plan(self, type):
        self.finished = False
        self.failed = False
        self.type = type
        if self.type == "dfs" :
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "bfs":
            self.frontier = [self.start]
            self.explored = []
        elif self.type == "ucs":
            self.frontier = []
			# Push the starting node to the priority queue with priority 0
            heappush(self.frontier, (0,self.start))
            self.explored = []
        elif self.type == "astar":
            self.frontier = []
            value = self.astar_heuristic((self.start)[0],(self.start)[1])
			# Push the starting node with its heuristic cost as priority in priority queue
            heappush(self.frontier, (value,self.start))
            self.explored = []
    def show_result(self):
        current = self.goal
        while not current == self.start:
            current = self.previous[current]
            self.grid.nodes[current].in_path = True #This turns the color of the node to red
	# A function to calcualte and print cost of path. We iterate using the previous of nodes and calcualte the cost using those nodes. 
    def show_pathlength(self):
        total_cost = 0
        current = self.goal
        while not current == self.start:
            #print('Cost of ', current, ' is ', self.grid.nodes[current].cost())
            total_cost = total_cost + self.grid.nodes[current].cost()
            current = self.previous[current]
        print('Total cost of path is: ', total_cost)
	#A function to find the heuristic cost of the given node
    def astar_heuristic(self,node_x, node_y):
        dx = abs(node_x - self.goal[0])
        dy = abs(node_y - self.goal[1])
        #return (dx+dy)
        #return 1 * (dx + dy) + (1 - 2 * 1) * min(dx, dy)
        return 1 * sqrt(dx * dx + dy * dy)
    def make_step(self):
        if self.type == "dfs":
            self.dfs_step()
        elif self.type == "bfs":
            self.bfs_step()
        elif self.type == "ucs":
            self.ucs_step()
        elif self.type == "astar":
            self.astar_step()
    def dfs_step(self):
        #...
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.pop()
        print("current node: ", current)
        #...
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.append(current)
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #...
        for node in children:
            #See what happens if you disable this check here
            if node in self.explored or node in self.frontier:
                print("explored before: ", node)
                continue
            #...
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #...
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #...
                    self.previous[node] = current
                    if node == self.goal:
                        self.finished = True
                        return
                    else:
                        #...
                        self.frontier.append(node)
                        #...
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
    def bfs_step(self):
        if not self.frontier:
            self.failed = True
            print("no path")
            return
        current = self.frontier.pop()
        print("current node: ", current)
        #Popping the frontier
        self.grid.nodes[current].checked = True
        self.grid.nodes[current].frontier = False
        self.explored.insert(0,current)
		#So we check for the children using ACTIONS array
        children = [(current[0]+a[0], current[1]+a[1]) for a in ACTIONS]
        #Iterating across all valid children
        for node in children:
            #If already in frontier, we do not update it for bfs or dfs
            if node in self.explored or node in self.frontier:
                print("explored before: ", node)
                continue
            #Because the child can go out of range, we first check for range
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                #If it is a puddle, we do not consider it
                if self.grid.nodes[node].puddle:
                    print("puddle at: ", node)
                else:
                    #Set previous so the path can be traced back
                    self.previous[node] = current
                    if node == self.goal:
					    #Found the goal
                        self.finished = True
                        return
                    else:
                        #Add to frontier
                        self.frontier.insert(0,node)
                        #Set frontier to true
                        self.grid.nodes[node].frontier = True
            else:
                print("out of range: ", node)
    def ucs_step(self):
        #[Hint] you can get the cost of a node by node.cost()
        if not self.frontier:
            self.failed = True
            print("no path")
            return
		#Popping the first from frontier
        current = heappop(self.frontier)
        #print(self.frontier)
        self.grid.nodes[current[1]].checked = True
        self.grid.nodes[current[1]].frontier = False
        self.explored.append(current[1])
		
        children = [(current[1][0]+a[0], current[1][1]+a[1]) for a in ACTIONS]
        #print(children)
        #Iterating through the children
        for node in children:
			#Checking for children in range
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                checker = False
                if node in self.explored:
                    #Already explored
                    continue
                elif node == self.goal:
				
                    self.previous[node] = current[1]
                    #Found goal
                    self.finished = True
                    return
                elif self.grid.nodes[node].puddle:
                    #print("puddle at: ", node)
                    continue					
                else:
                    #Checking if child already in frontier
                    for tuple in self.frontier:
                        if tuple[1] == node and (current[0]+self.grid.nodes[node].cost()) < tuple[0]:
                            #In frontier with higher cost, so remove the old one, add with new cost, and re-heapify
                            heappop(tuple)
                            self.previous[node] = current[1]
                            heappush(self.frontier, (current[0]+self.grid.nodes[node].cost(),node))
                            heapify(self.frontier)
                            checker = True
                        elif tuple[1] == node and (current[0]+self.grid.nodes[node].cost()) >= tuple[0]:
                            checker = True
                            continue
                    if checker is not True:
                        self.previous[node] = current[1]
                        heappush(self.frontier, (current[0]+self.grid.nodes[node].cost(),node))
                        self.grid.nodes[node].frontier = True		
    def astar_step(self):
        #[Hint] you need to declare a heuristic function for Astar
        if not self.frontier:
            self.failed = True
            print("no path")
            return
		#Popping the first from frontier
        current = heappop(self.frontier)
		
        #print(self.frontier)
        self.grid.nodes[current[1]].checked = True
        self.grid.nodes[current[1]].frontier = False
        self.explored.append(current[1])
		
        children = [(current[1][0]+a[0], current[1][1]+a[1]) for a in ACTIONS]
        #print(children)
        #Iterating through the children
        for node in children:
		    #Checking if children in range
            if node[0] in range(self.grid.row_range) and node[1] in range(self.grid.col_range):
                checker = False
                if node in self.explored:
                    #Already explored
                    continue
                elif node == self.goal:
                    self.previous[node] = current[1]
                    #Found goal
                    self.finished = True
                    return
                elif self.grid.nodes[node].puddle:
                    #puddle at node
                    continue					
                else:
                    #print('Going into last')
					
                    for tuple in self.frontier:
						#Case if the child is already in frontier and checking for G + H < the one in frontier
                        if tuple[1] == node and (self.grid.nodes[node].cost() + self.astar_heuristic(node[0],node[1])) < tuple[0]:
                            #In frontier with higher cost
                            heappop(tuple)
                            self.previous[node] = current[1]
                            heappush(self.frontier, ((self.grid.nodes[node].cost() + self.astar_heuristic(node[0],node[1])),node))
                            heapify(self.frontier)
                            checker = True
                            continue
                        elif tuple[1] == node and (self.grid.nodes[node].cost() + self.astar_heuristic(node[0],node[1])) >= tuple[0]:
                            checker = True
                            continue
					#If child is not in frontier
                    if checker is not True:
                        self.previous[node] = current[1]
                        heappush(self.frontier, ((self.grid.nodes[node].cost() + self.astar_heuristic(node[0],node[1])),node))
                        self.grid.nodes[node].frontier = True